"""Record voice lines on ANY machine (the dev-box recorders vo_rec.py / feature_rec.py only run on the dev box).

One clip per line, each with its own emotion, then a speech-to-text check with Sarvam so you can see what was heard.
Keys come from environment variables and are never written anywhere:
    MINIMAX_API_KEY   MiniMax speech-2.8-hd through Tencent TokenHub (see tts_test.py URL; override with MINIMAX_TTS_URL)
    QWEN_API_KEY      Qwen-Audio 3.0 (only needed for Qwen voices, e.g. Mitthu and Quizzy in English)
    SARVAM_API_KEY    optional, for the speech-to-text check

Works with both line formats:
    vo_lines.json       {"voice": ..., "V03": {"lines": [[emotion, text, old_start, gap], ...], "voices": {"3": voice}}}
    vo_lines_hi.json    same, lines are [qwen tag, emotion, text, old_start, gap]
    feature_lines.json  {"voices": {speaker: [engine, voice]}, "V12": {"lines": [[speaker, emotion, text, gap, options], ...]}}

Usage:
    python rec_anywhere.py <lines.json> <VIDEO_ID> <out_dir> [--only=3,7] [--lang=hi] [--dry]
    --lang=hi  Hindi: language_boost Hindi and Sarvam hi-IN (default en)
    --dry      print what would be recorded, call nothing
Then copy <out_dir> to wherever build_vo.py / build_feature.py expects the clips (see HOW-WE-MAKE-VIDEOS.md).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_test as T

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = dict((a[2:].split('=', 1) + [''])[:2] for a in sys.argv[1:] if a.startswith('--'))
if len(args) < 3:
    sys.exit(__doc__)
lines_file, vid, out = args
lang = opt.get('lang', 'en')
only = set(map(int, opt['only'].split(','))) if opt.get('only') else None
dry = 'dry' in opt
J = json.load(open(lines_file))
S = J[vid]
os.makedirs(out, exist_ok=True)

def jobs():
    for i, row in enumerate(S['lines']):
        if only is not None and i not in only:
            continue
        if 'voices' in J and isinstance(row[0], str) and row[0] in J['voices']:      # feature format
            spk, emo, text = row[0], row[1], row[2]
            eng, voice = J['voices'][spk]
        elif isinstance(row[2], str):                                                 # vo_lines_hi: [qwen tag, emotion, text, old, gap]
            spk, emo, text = 'N', row[1], row[2]
            eng, voice = 'minimax', S.get('voices', {}).get(str(i), J.get('voice'))
        else:                                                                         # vo_lines: [emotion, text, old, gap]
            spk, emo, text = 'N', row[0], row[1]
            eng, voice = 'minimax', S.get('voices', {}).get(str(i), J.get('voice'))
        yield i, spk, eng, voice, emo, text

def stt(path):
    key = os.environ.get('SARVAM_API_KEY')
    if not key:
        return '(no SARVAM_API_KEY, not checked)'
    import requests
    r = requests.post('https://api.sarvam.ai/speech-to-text', headers={'api-subscription-key': key},
                      files={'file': (os.path.basename(path), open(path, 'rb'), 'audio/mpeg')},
                      data={'model': 'saarika:v2.5', 'language_code': 'hi-IN' if lang == 'hi' else 'en-IN'}, timeout=60)
    return r.json().get('transcript') if r.ok else r.text[:120]

for i, spk, eng, voice, emo, text in jobs():
    path = os.path.join(out, f'{vid}_{i:02d}.mp3')
    if eng == 'qwen':
        tag = T.TO_QWEN.get(emo, emo)
        clean, dropped = T.clean_for_qwen((f'[{tag}]' if tag in T.QWEN_CONTROL else '') + text)
    else:
        clean, _, dropped = T.clean_for_minimax(text)
    if dry:
        print(f'{i:02d} {spk:7s} {eng:7s} {voice:24s} {emo:9s} | {clean}')
        continue
    key = os.environ.get('QWEN_API_KEY' if eng == 'qwen' else 'MINIMAX_API_KEY')
    if not key:
        sys.exit(f'Set {"QWEN_API_KEY" if eng == "qwen" else "MINIMAX_API_KEY"} first.')
    t = time.time()
    audio = (T.qwen_tts(key, 'qwen-audio-3.0-tts-plus', clean, voice) if eng == 'qwen'
             else T.tts(key, 'minimax-speech-2.8-hd', clean, voice, lang=lang, emotion=emo))
    open(path, 'wb').write(audio)
    print(f'{i:02d} {spk:7s} {voice:24s} {emo:9s} {time.time() - t:4.1f}s | {clean} | heard: {stt(path)}'
          + (f'  DROPPED {dropped}' if dropped else ''), flush=True)
