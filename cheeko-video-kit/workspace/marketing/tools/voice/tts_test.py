"""Test MiniMax Speech 2.8 (Tencent TokenHub) and Qwen-Audio 3.0 TTS (Alibaba) across Indian languages.

Usage:
    set MINIMAX_API_KEY=sk-...
    set QWEN_API_KEY=sk-ws-...
    py tts_test.py                                   # all models, all languages
    py tts_test.py --model qwen-flash --lang hi ta --voice <voice_id>
Outputs mp3 files to ./out/
"""
import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
import uuid

import websocket  # pip install websocket-client

URL = os.environ.get("MINIMAX_TTS_URL") or "https://tokenhub.tencentmaas.com/v1/wand/minimax-tts/sync_tts"
# Qwen-Audio TTS is WebSocket-only (DashScope SpeechSynthesizer protocol)
QWEN_WS = os.environ.get("QWEN_WS") or "wss://ws-tx2ql1zgwzv0sg1c.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"
MODELS = {
    "turbo": "minimax-speech-2.8-turbo",
    "hd": "minimax-speech-2.8-hd",
    "qwen-flash": "qwen-audio-3.0-tts-flash",
    "qwen-plus": "qwen-audio-3.0-tts-plus",
}
# Per-language voices, picked as friendly female voices for a kids companion.
# MiniMax has native system voices only for Hindi; the other Indic languages use a multilingual voice.
# Qwen-Audio 3.0 officially supports no Indic language; longanhuan (multilingual female) is best effort.
M_IN = "hindi_female_2_v1"          # "Tranquil Woman", native Hindi
M_MULTI = "English_Kind-heartedGirl"
Q_MULTI = "longanhuan_v3.6"
Q_EN = "loongnorahu"                # English, Female 25, "Lively & Spirited"
VOICES = {
    "hi": {"minimax": M_IN, "qwen": Q_MULTI},
    "mr": {"minimax": M_IN, "qwen": Q_MULTI},  # Devanagari script, Indian accent beats an English one
    "ta": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "te": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "kn": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "ml": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "bn": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "gu": {"minimax": M_MULTI, "qwen": Q_MULTI},
    "en": {"minimax": "English_PlayfulGirl", "qwen": Q_EN},
}
# MiniMax language_boost: only these are accepted (Telugu/Kannada/Malayalam/Bengali/Marathi/Gujarati -> "invalid params")
BOOST = {"hi": "Hindi", "ta": "Tamil", "en": "English"}

# --- Expressive markup each engine actually understands (verified 2026-09-25) ---------------------------
# Qwen reads any UNKNOWN [tag] aloud ("[banana] hello" -> "Banana hello"); MiniMax has no text mood tags at
# all — mood is the voice_setting.emotion parameter. So TTS input is sanitised: aliases mapped, unknowns cut.
MINIMAX_EMOTIONS = {"happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent"}
MINIMAX_SOUNDS = {"laughs", "chuckle", "coughs", "clear-throat", "groans", "breath", "pant", "inhale", "exhale",
                  "gasps", "sniffs", "sighs", "snorts", "burps", "lip-smacking", "humming", "hissing", "emm", "sneezes"}
QWEN_CONTROL = {"sad", "amazed", "deep and loud shouting", "trembling", "angry", "excited", "sarcastic", "curious",
                "like dracula", "bored", "tired", "scornful", "shouting", "asmr", "panicked", "mischievously",
                "empathetic", "whispers", "reluctantly", "crying", "serious", "very slowly", "very fast"}
QWEN_SOUNDS = {"gasp", "sighing", "clears throat", "giggles", "laughing", "cough", "snorts"}
# what LLMs tend to write -> what the engine knows
TO_MINIMAX = {"giggles": "laughs", "giggle": "laughs", "laugh": "laughs", "laughing": "laughs", "chuckles": "chuckle",
              "gasp": "gasps", "sigh": "sighs", "sighing": "sighs", "cough": "coughs", "clears throat": "clear-throat"}
TO_QWEN = {"happy": "excited", "surprised": "amazed", "whisper": "whispers", "laughs": "laughing", "laugh": "laughing",
           "giggle": "giggles", "chuckle": "giggles", "chuckles": "giggles", "sighs": "sighing", "sigh": "sighing",
           "gasps": "gasp", "coughs": "cough"}
_BRACKET = re.compile(r"\[([^\]\n]{1,30})\]")
_PAREN = re.compile(r"\(([a-z][a-z -]{1,20})\)", re.I)   # ascii-only, so "(म्याऊँ)" and the like are untouched
_PAUSE = re.compile(r"<#[\d.]+#>")


def clean_for_minimax(text):
    """-> (text, emotion, dropped). First known [mood] becomes the emotion parameter; every [..] is removed from
    the text. (sound) tags are aliased to MiniMax's list or dropped."""
    emotion, dropped = None, []

    def mood(m):
        nonlocal emotion
        t = m.group(1).strip().lower()
        if t in MINIMAX_EMOTIONS and emotion is None:
            emotion = t
        elif t not in MINIMAX_EMOTIONS:
            dropped.append(m.group(0))
        return ""

    def sound(m):
        t = TO_MINIMAX.get(m.group(1).strip().lower(), m.group(1).strip().lower())
        if t in MINIMAX_SOUNDS:
            return f"({t})"
        dropped.append(m.group(0))
        return ""

    text = _PAREN.sub(sound, _BRACKET.sub(mood, text))
    return re.sub(r"[ \t]{2,}", " ", text).strip(), emotion, dropped


def clean_for_qwen(text):
    """-> (text, dropped). Keeps only Qwen's control/sound tags (aliases mapped); anything else in [..] or (..)
    is removed so it is never read aloud. MiniMax pauses mean nothing here and are cut."""
    dropped = []

    def tag(m):
        t = TO_QWEN.get(m.group(1).strip().lower(), m.group(1).strip().lower())
        if t in QWEN_CONTROL or t in QWEN_SOUNDS:
            return f"[{t}]"
        dropped.append(m.group(0))
        return ""

    text = _PAUSE.sub("", _PAREN.sub(tag, _BRACKET.sub(tag, text)))
    return re.sub(r"[ \t]{2,}", " ", text).strip(), dropped

SAMPLES = {
    "hi": "नमस्ते बच्चों! मैं चीको हूँ। चलो आज एक मज़ेदार कहानी सुनते हैं।",
    "ta": "வணக்கம் குழந்தைகளே! நான் சீக்கோ. இன்று ஒரு வேடிக்கையான கதை கேட்போம்.",
    "te": "నమస్కారం పిల్లలూ! నేను చీకో. ఈ రోజు ఒక సరదా కథ విందాం.",
    "kn": "ನಮಸ್ಕಾರ ಮಕ್ಕಳೇ! ನಾನು ಚೀಕೋ. ಇಂದು ಒಂದು ಮಜಾದ ಕಥೆ ಕೇಳೋಣ.",
    "ml": "നമസ്കാരം കുട്ടികളേ! ഞാൻ ചീക്കോ ആണ്. ഇന്ന് ഒരു രസകരമായ കഥ കേൾക്കാം.",
    "bn": "নমস্কার বন্ধুরা! আমি চিকো। চলো আজ একটা মজার গল্প শুনি।",
    "mr": "नमस्कार मुलांनो! मी चीको आहे. चला आज एक मजेदार गोष्ट ऐकूया.",
    "gu": "નમસ્તે બાળકો! હું ચીકો છું. ચાલો આજે એક મજાની વાર્તા સાંભળીએ.",
    "en": "Hello kids! I am Cheeko. Let's listen to a fun story today.",
}

# Emotion-tagged defaults for the UI. Markup differs per provider, so never send one to the other:
# MiniMax = (laughs) sound tags + <#s#> pauses; Qwen = [emotion] mood tags + [sound] tags.
# ponytail: non-hi/en entries are SAMPLES sentences plus tags; tags are documented for en/zh only
TAGGED = {
    "hi": {"minimax": "अरे वाह! <#0.3#> तुमने तो कमाल कर दिया! (laughs) पता है, आज जंगल में एक छोटा सा खरगोश अपनी गाजर ढूँढ रहा था... (sighs) वो बहुत उदास था। <#0.5#> फिर अचानक... (gasps) पेड़ के पीछे से एक गिलहरी आई और बोली, \"ये लो तुम्हारी गाजर!\" (chuckle)",
           "qwen": "[excited]अरे वाह! तुमने तो कमाल कर दिया![laughing] [curious]पता है, आज जंगल में एक छोटा सा खरगोश अपनी गाजर ढूँढ रहा था... [sad]वो बहुत उदास था।[sighing] [whispers]फिर अचानक...[gasp] [excited]पेड़ के पीछे से एक गिलहरी आई और बोली, \"ये लो तुम्हारी गाजर!\"[giggles]"},
    "ta": {"minimax": "வணக்கம் குழந்தைகளே! (laughs) நான் சீக்கோ. <#0.4#> இன்று ஒரு வேடிக்கையான கதை கேட்போம்!",
           "qwen": "[excited]வணக்கம் குழந்தைகளே![giggles] நான் சீக்கோ. [curious]இன்று ஒரு வேடிக்கையான கதை கேட்போம்!"},
    "te": {"minimax": "నమస్కారం పిల్లలూ! (laughs) నేను చీకో. <#0.4#> ఈ రోజు ఒక సరదా కథ విందాం!",
           "qwen": "[excited]నమస్కారం పిల్లలూ![giggles] నేను చీకో. [curious]ఈ రోజు ఒక సరదా కథ విందాం!"},
    "kn": {"minimax": "ನಮಸ್ಕಾರ ಮಕ್ಕಳೇ! (laughs) ನಾನು ಚೀಕೋ. <#0.4#> ಇಂದು ಒಂದು ಮಜಾದ ಕಥೆ ಕೇಳೋಣ!",
           "qwen": "[excited]ನಮಸ್ಕಾರ ಮಕ್ಕಳೇ![giggles] ನಾನು ಚೀಕೋ. [curious]ಇಂದು ಒಂದು ಮಜಾದ ಕಥೆ ಕೇಳೋಣ!"},
    "ml": {"minimax": "നമസ്കാരം കുട്ടികളേ! (laughs) ഞാൻ ചീക്കോ ആണ്. <#0.4#> ഇന്ന് ഒരു രസകരമായ കഥ കേൾക്കാം!",
           "qwen": "[excited]നമസ്കാരം കുട്ടികളേ![giggles] ഞാൻ ചീക്കോ ആണ്. [curious]ഇന്ന് ഒരു രസകരമായ കഥ കേൾക്കാം!"},
    "bn": {"minimax": "নমস্কার বন্ধুরা! (laughs) আমি চিকো। <#0.4#> চলো আজ একটা মজার গল্প শুনি!",
           "qwen": "[excited]নমস্কার বন্ধুরা![giggles] আমি চিকো। [curious]চলো আজ একটা মজার গল্প শুনি!"},
    "mr": {"minimax": "नमस्कार मुलांनो! (laughs) मी चीको आहे. <#0.4#> चला आज एक मजेदार गोष्ट ऐकूया!",
           "qwen": "[excited]नमस्कार मुलांनो![giggles] मी चीको आहे. [curious]चला आज एक मजेदार गोष्ट ऐकूया!"},
    "gu": {"minimax": "નમસ્તે બાળકો! (laughs) હું ચીકો છું. <#0.4#> ચાલો આજે એક મજાની વાર્તા સાંભળીએ!",
           "qwen": "[excited]નમસ્તે બાળકો![giggles] હું ચીકો છું. [curious]ચાલો આજે એક મજાની વાર્તા સાંભળીએ!"},
    "en": {"minimax": "Wow, you found it! (laughs) That's amazing! <#0.5#> Oh no... (sighs) the little bunny lost his carrot. Shh... listen closely. <#0.8#> Did you hear that?",
           "qwen": "[excited]Wow, you found it![laughing] That's amazing! [sad]Oh no... the little bunny lost his carrot.[sighing] [whispers]Shh... listen closely. Did you hear that?"},
}


def tts(key, model, text, voice, lang=None, emotion=None):
    body = {
        "model": model,
        "text": text,
        "stream": False,
        "language_boost": BOOST.get(lang, "auto"),
        "voice_setting": {"voice_id": voice, "speed": 1, "vol": 1, "pitch": 0, **({"emotion": emotion} if emotion else {})},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }
    req = urllib.request.Request(URL, json.dumps(body).encode(), {
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = r.read()
    data = json.loads(raw)
    base = data.get("base_resp") or {}
    if base.get("status_code", 0) != 0:
        raise RuntimeError(f"{base.get('status_code')}: {base.get('status_msg')}")
    return bytes.fromhex(data["data"]["audio"])  # MiniMax returns hex-encoded audio


def qwen_tts(key, model, text, voice, lang=None):  # no language param; voice decides
    if "_v3" not in voice and not voice.startswith("qwen-audio"):
        voice = f"{model}-{voice}"  # base voices (voices_qwen.csv) are listed by suffix; the full id is per model
    ws = websocket.create_connection(QWEN_WS, header=[f"Authorization: bearer {key}"], timeout=120)
    task_id = uuid.uuid4().hex
    hdr = lambda action: {"action": action, "task_id": task_id, "streaming": "duplex"}
    try:
        ws.send(json.dumps({"header": hdr("run-task"), "payload": {
            "task_group": "audio", "task": "tts", "function": "SpeechSynthesizer", "model": model,
            "parameters": {"text_type": "PlainText", "voice": voice, "format": "mp3", "sample_rate": 24000,
                           "bit_rate": 128},  # kbps; default is 160 at 24kHz
            "input": {}}}))
        audio, started = bytearray(), False
        while True:
            msg = ws.recv()
            if isinstance(msg, bytes):
                audio += msg
                continue
            ev = json.loads(msg)["header"]
            if ev.get("event") == "task-failed":
                raise RuntimeError(f"{ev.get('error_code')}: {ev.get('error_message')}")
            if ev.get("event") == "task-started" and not started:
                started = True
                ws.send(json.dumps({"header": hdr("continue-task"), "payload": {"input": {"text": text}}}))
                ws.send(json.dumps({"header": hdr("finish-task"), "payload": {"input": {}}}))
            if ev.get("event") == "task-finished":
                return bytes(audio)
    finally:
        ws.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", nargs="*", choices=list(MODELS), default=list(MODELS))
    p.add_argument("--lang", nargs="*", default=list(SAMPLES), help=" ".join(SAMPLES))
    p.add_argument("--voice", help="override voice id (default per provider)")
    a = p.parse_args()

    os.makedirs("out", exist_ok=True)

    for m in a.model:
        model, qwen = MODELS[m], m.startswith("qwen")
        env = "QWEN_API_KEY" if qwen else "MINIMAX_API_KEY"
        key = os.environ.get(env)
        if not key:
            print(f"SKIP {model}: set {env}")
            continue
        fn = qwen_tts if qwen else tts
        for lang in a.lang:
            voice = a.voice or VOICES[lang]["qwen" if qwen else "minimax"]
            t = time.time()
            try:
                audio = fn(key, model, SAMPLES[lang], voice, lang)
            except urllib.error.HTTPError as e:
                print(f"FAIL {model:28} {lang}  HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
                continue
            except Exception as e:
                print(f"FAIL {model:28} {lang}  {e}")
                continue
            path = f"out/{model}_{lang}.mp3"
            with open(path, "wb") as f:
                f.write(audio)
            print(f"OK   {model:28} {lang}  {time.time() - t:5.2f}s  {len(audio) // 1024}KB  -> {path}")


def _selfcheck():
    t, e, d = clean_for_minimax("[happy] YIPPEE! (giggles) <#0.4#> Wiggly? (banana) [excited] ok")
    assert (t, e) == ("YIPPEE! (laughs) <#0.4#> Wiggly? ok", "happy") and d == ["[excited]", "(banana)"], (t, e, d)
    assert clean_for_minimax("(म्याऊँ) plain")[0] == "(म्याऊँ) plain"
    t, d = clean_for_qwen("[happy] Hi![giggles] (laughs) <#0.5#> [banana] [curious]bye")
    assert t == "[excited] Hi![giggles] [laughing] [curious]bye" and d == ["[banana]"], (t, d)
    print("tts_test self-check ok")


if __name__ == "__main__":
    import sys
    _selfcheck() if "--check" in sys.argv else main()
