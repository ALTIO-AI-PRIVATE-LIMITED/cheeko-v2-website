"""Sung lullabies through ElevenLabs Eleven Music. Runs on the dev box; the key stays there in /root/tts-compare/.env.elevenlabs.
Usage (on the box): python3 eleven_music.py <lyrics json> <lang en|hi> <out.mp3> [model]
Builds a composition plan (one chunk per section, our own lyrics and styles) and saves the song plus <out>.json with the song id."""
import json, sys, time, requests
K = dict(l.strip().split('=', 1) for l in open('/root/tts-compare/.env.elevenlabs') if '=' in l)['ELEVENLABS_API_KEY']
src, lang, out = sys.argv[1:4]; model = sys.argv[4] if len(sys.argv) > 4 else 'music_v2_5'
S = json.load(open(src))[lang]
chunks = []
for i, sec in enumerate(S['sections']):
    c = {'text': f"[{sec['name']}]\n" + '\n'.join(sec['lines']), 'duration_ms': sec['ms'],
         'positive_styles': S['styles'] if i == 0 else S['styles'][:4] + S['styles'][-3:], 'negative_styles': S['negative']}
    chunks.append(c)
body = {'model_id': model, 'composition_plan': {'chunks': chunks}}
t0 = time.time()
r = requests.post('https://api.elevenlabs.io/v1/music', params={'output_format': 'mp3_48000_192'},
                  headers={'xi-api-key': K, 'Content-Type': 'application/json'}, json=body, timeout=600)
if not r.ok: print('ERROR', r.status_code, r.text[:600]); sys.exit(1)
open(out, 'wb').write(r.content)
meta = {k: v for k, v in r.headers.items() if k.lower().startswith(('song', 'x-', 'character', 'request'))}
json.dump({'model': model, 'lang': lang, 'secs': round(time.time() - t0, 1), 'headers': meta, 'plan': body}, open(out + '.json', 'w'), indent=1, ensure_ascii=False)
print('saved', out, len(r.content), 'bytes in', round(time.time() - t0, 1), 's', {k: v for k, v in meta.items() if 'song' in k.lower() or 'cost' in k.lower() or 'character' in k.lower()})
