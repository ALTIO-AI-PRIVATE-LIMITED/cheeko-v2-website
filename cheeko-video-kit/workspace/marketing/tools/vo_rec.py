"""Record one MiniMax clip per voice line and check each with Sarvam speech-to-text. Runs on the dev box;
API keys are read from the running ui.py process and never leave the box.
Usage: python3 vo_rec.py vo_lines.json V06 [line numbers, e.g. 3,7]"""
import json, os, sys, requests
sys.path.insert(0, '/root/tts-compare')
import tts_test as T
pid = next(p for p in os.listdir('/proc') if p.isdigit() and b'tts-compare/ui.py' in open(f'/proc/{p}/cmdline', 'rb').read())
env = dict(l.split('=', 1) for l in open(f'/proc/{pid}/environ', 'rb').read().decode(errors='ignore').split('\0') if '=' in l)
MK, SK = env['MINIMAX_API_KEY'], env['SARVAM_API_KEY']
J = json.load(open(sys.argv[1])); vid = sys.argv[2]
only = set(map(int, sys.argv[3].split(','))) if len(sys.argv) > 3 else None
S = J[vid]; out = f'/root/tts-compare/out/{vid.lower()}'; os.makedirs(out, exist_ok=True)
for i, (emo, text, *_) in enumerate(S['lines']):
    if only is not None and i not in only: continue
    voice = S.get('voices', {}).get(str(i), J['voice'])
    clean, _, dropped = T.clean_for_minimax(text)
    f = f'{out}/{vid}_{i:02d}.mp3'
    open(f, 'wb').write(T.tts(MK, 'minimax-speech-2.8-hd', clean, voice, lang='en', emotion=emo))
    r = requests.post('https://api.sarvam.ai/speech-to-text', headers={'api-subscription-key': SK},
                      files={'file': (os.path.basename(f), open(f, 'rb'), 'audio/mpeg')},
                      data={'model': 'saarika:v2.5', 'language_code': 'en-IN'}, timeout=60)
    heard = r.json().get('transcript') if r.ok else r.text[:120]
    print(f'{i:02d} {voice:18s} {emo:9s} | {clean} | heard: {heard}{"  DROPPED " + str(dropped) if dropped else ""}', flush=True)
