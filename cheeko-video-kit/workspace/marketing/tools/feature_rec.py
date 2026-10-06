"""Record one MiniMax clip per feature line (feature_lines.json format: [speaker, emotion, text, gap, options]) and check each
with Sarvam speech-to-text. Runs on the dev box; API keys are read from the running ui.py process and never leave the box.
Usage: python3 feature_rec.py feature_lines.json V26 [line numbers, e.g. 3,7] [--voice=ID to override the line's voice]"""
import json, os, sys, requests
sys.path.insert(0, '/root/tts-compare')
import tts_test as T
pid = next(p for p in os.listdir('/proc') if p.isdigit() and b'tts-compare/ui.py' in open(f'/proc/{p}/cmdline', 'rb').read())
env = dict(l.split('=', 1) for l in open(f'/proc/{pid}/environ', 'rb').read().decode(errors='ignore').split('\0') if '=' in l)
MK, SK = env['MINIMAX_API_KEY'], env['SARVAM_API_KEY']
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--'))
J = json.load(open(args[0])); vid = args[1]
only = set(map(int, args[2].split(','))) if len(args) > 2 else None
out = f'/root/tts-compare/out/{vid.lower()}'; os.makedirs(out, exist_ok=True)
for i, (spk, emo, text, *_rest) in enumerate(J[vid]['lines']):
    if only is not None and i not in only: continue
    eng, voice = J['voices'][spk]; voice = opt.get('voice', voice); assert eng == 'minimax', spk
    clean, _, dropped = T.clean_for_minimax(text)
    f = f'{out}/{vid}_{i:02d}' + (f'_{voice}' if 'voice' in opt else '') + '.mp3'
    open(f, 'wb').write(T.tts(MK, 'minimax-speech-2.8-hd', clean, voice, lang='en', emotion=emo))
    r = requests.post('https://api.sarvam.ai/speech-to-text', headers={'api-subscription-key': SK},
                      files={'file': (os.path.basename(f), open(f, 'rb'), 'audio/mpeg')},
                      data={'model': 'saarika:v2.5', 'language_code': 'en-IN'}, timeout=60)
    heard = r.json().get('transcript') if r.ok else r.text[:120]
    print(f'{i:02d} {spk:7s} {voice:24s} {emo:9s} | {clean} | heard: {heard}{"  DROPPED " + str(dropped) if dropped else ""}', flush=True)
