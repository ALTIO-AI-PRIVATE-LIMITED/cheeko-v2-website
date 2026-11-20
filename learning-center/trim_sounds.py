"""Unpack the Envato zips (sounds/zips/<key>.zip) and cut one short clean clip per sound into sounds/<key>.mp3.
Each clip starts at the first strong hit before the loudest moment, runs up to 2.6 s (shorter if the sound ends), fades out
and is levelled to the same loudness. Also writes sounds/check_<group>.mp3 (all clips in a row) for listening.
Usage: /usr/bin/python3 trim_sounds.py [key ...]"""
import glob, json, os, subprocess, sys, zipfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000; L = 2.6
EXTRA = {}   # was the Sounds Around Me card clip for house_pressure_cooker; replaced by Envato Steam Whistle (team review 2026-10-29)     # Sounds Around Me card clip (source to confirm with Abilash)

def load(f):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'])
    return np.frombuffer(raw, np.float32).astype(float)
def source(key):
    if key in EXTRA: return EXTRA[key]
    d = f'sounds/raw/{key}'
    if not os.path.isdir(d):
        os.makedirs(d); zipfile.ZipFile(f'sounds/zips/{key}.zip').extractall(d)
    files = [f for f in glob.glob(f'{d}/**/*', recursive=True) if f.lower().endswith(('.wav', '.mp3', '.aif', '.aiff', '.flac')) and '__MACOSX' not in f]
    return sorted(files, key=lambda f: (-('preview' not in f.lower()), os.path.getsize(f)))[-1] if files else None
def cut(x):
    hop = int(SR * .02); env = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))[::hop] + 1e-9
    db = 20 * np.log10(env / env.max()); peak = int(np.argmax(db))
    i = peak
    while i > 0 and db[i] > -30 and (peak - i) * .02 < 2.0: i -= 1        # walk back to the quiet before the hit
    if (peak - i) * .02 > 1.2 and len(x) > SR * L: i = max(0, peak - int(.3 / .02))   # continuous sound: start just before the loudest part
    start = max(0, i * hop - int(SR * .03)); end = min(len(x), start + int(SR * L))
    loud = np.where(db[start // hop:end // hop] > -32)[0]                 # stop early when the sound has ended
    if len(loud): end = min(end, start + (loud[-1] + 8) * hop)
    end = max(end, min(len(x), start + int(SR * .8)))
    y = x[start:end].copy(); fi, fo = int(SR * .008), min(int(SR * .15), len(y) // 3)
    y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    return y
keys = sys.argv[1:] or [x['key'] for x in json.load(open('envato_dl.json'))] + list(EXTRA)
info = {}
for k in keys:
    src = source(k)
    if not src: print('no audio', k); continue
    y = cut(load(src))
    if len(y) < SR * 1.2 and k not in ('lion',):      # one short oink or snip: repeat it so a child can catch it
        gap = np.zeros(int(SR * .14)); reps = 3 if len(y) < SR * .6 else 2
        y = np.concatenate(sum([[y, gap] for _ in range(reps)], [])[:-1])
    tmp = f'sounds/_{k}.f32'; y.astype(np.float32).tofile(tmp)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', tmp,
                    '-af', 'loudnorm=I=-18:TP=-2:LRA=11', '-ar', str(SR), '-c:a', 'libmp3lame', '-b:a', '160k', f'sounds/{k}.mp3'], check=True)
    os.remove(tmp); info[k] = {'src': os.path.relpath(src, 'sounds'), 'secs': round(len(y) / SR, 2)}
    print(f'{k:24s} {len(y) / SR:4.2f}s  from {os.path.basename(src)}')
old = json.load(open('sounds/sounds.json')) if os.path.exists('sounds/sounds.json') else {}
old.update(info); json.dump(old, open('sounds/sounds.json', 'w'), indent=1)
for g, pre in (('animals', ''), ('house', 'house_'), ('instruments', 'inst_')):
    ks = [k for k in old if (k.startswith(pre) if pre else not k.startswith(('house_', 'inst_')))]
    lst = f'sounds/_{g}.txt'; gap = 'sounds/_gap.mp3'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=mono', '-t', '0.7', '-c:a', 'libmp3lame', gap], check=True)
    open(lst, 'w').write(''.join(f"file '{os.path.abspath('sounds/' + k + '.mp3')}'\nfile '{os.path.abspath(gap)}'\n" for k in ks))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'libmp3lame', '-b:a', '128k', f'sounds/check_{g}.mp3'], check=True)
    os.remove(lst)
os.remove('sounds/_gap.mp3')
