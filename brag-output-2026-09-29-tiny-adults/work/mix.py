"""Audio for V09 "Tiny Adults": voiceover + sound effects + licensed music that follows the story.
Music plan (scene timeline, mapped through warp.json):
  0 - 2.45   full track: it's a party!
  2.45       record scratch, music cuts
  2.8 - 20.8 the grown-up world: a thin version (bass + organ stems only, quieter)
  20.8 - 25.8 freeze and rewind: no music, tape stop / rewind sounds
  25.8 - end full track again as Cheeko drops in, placed so the track's own ending lands on the end card
Music (optional; without it this writes voice + sfx only): Envato Elements "Quirky Fun Sports Party Dance" by
SunChannelMusic (downloaded by Ravi 2026-09-29, licensed to his account). music-src.wav = the full mix,
music/**/*bass*, *organ*, *drums* = the stems used for the thin section (falls back to a low-passed full mix).
Real Cheeko sounds in sfx/ (device boot, low battery, popup, success, knob click); the rest is synthesised.
Writes music-final.wav (full mix for render.mjs/finish.sh) and music-only.wav (music + sfx, no voice).
Usage (inside work/): ../../.venv/bin/python mix.py"""
import glob, json, os, subprocess
import numpy as np, wave

SR = 44100
WJ = json.load(open('warp.json'))
DUR = WJ['dur']; N = int(SR * DUR)
rng = np.random.default_rng(7)
_OLD = [0.0] + WJ['old']; _NEW = [0.0] + WJ['new']
def W(t):  # scene timeline -> voice-anchored timeline (same map as compose.html)
    return float(np.interp(t, _OLD, _NEW)) if t <= _OLD[-1] else _NEW[-1] + (t - _OLD[-1])

def ts(d): return np.arange(int(SR * d)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def load(path):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    return np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
def place(buf, sig, t_scene, gain=1.0):
    i = int(W(t_scene) * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[: j - i] * gain
def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
    for k in range(len(x)):
        s = (1 - a) * x[k] + a * s; y[k] = s
    return y
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def pop(f=700):
    t = ts(.16); ff = f * (1 + 1.3 * np.exp(-t * 45))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 24)
def stamp():
    t = ts(.35); f = 60 + 90 * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) + lowpass(noise(.35), 2500) * np.exp(-t * 45) * 2.2
def whoosh(d=.32):
    t = ts(d); x = noise(d); x = lowpass(x, 3200) - lowpass(x, 500)
    return x * np.sin(np.pi * t / d) ** 2 * 1.4
def glock(f, d=.8):
    t = ts(d)
    return (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 8)) * np.exp(-t * 5) * np.minimum(1, t / .001)
def boing(d=.45):
    t = ts(d); f = 240 * (1 + .35 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 4))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
def scratch():  # record scratch: fast back-and-forth pitch sweep
    t = ts(.42); f = 700 * np.abs(np.sin(2 * np.pi * 4.2 * t)) + 90
    x = noise(.42) * .45 + np.sin(2 * np.pi * np.cumsum(f) / SR)
    return lowpass(x, 2600) * np.sin(np.pi * t / .42) * 1.2
def party_horn(d=.55):  # the paper blower at the start
    t = ts(d); f = 520 + 60 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR; x = sum(np.sin(k * ph) / k for k in range(1, 8))
    return lowpass(x, 3000) * np.minimum(1, t / .03) * np.minimum(1, (d - t) / .08) * .6
def ring():  # a phone ringing twice
    t = ts(.18); tone = (np.sin(2 * np.pi * 1320 * t) + np.sin(2 * np.pi * 1760 * t)) * .5 * (np.sin(2 * np.pi * 22 * t) > 0)
    gap = np.zeros(int(SR * .1)); return np.concatenate([tone, gap, tone]) * .5
def shutter():
    t = ts(.12); return lowpass(noise(.12), 5000) * (np.exp(-t * 60) + .7 * np.exp(-np.maximum(t - .05, 0) * 60) * (t > .05))
def news_sting():  # "dun dun DUNNN"
    out = []
    for f, d in ((hz(50), .16), (hz(50), .16), (hz(53), .7)):
        t = ts(d); ph = 2 * np.pi * f * t; x = sum(np.sin(k * ph) / k for k in range(1, 9))
        out.append(lowpass(x * np.minimum(1, t / .01) * np.exp(-t * (2 if d > .5 else 6)), 1800)); out.append(np.zeros(int(SR * .06)))
    return np.concatenate(out)
def tape_stop(d=.6):  # pitch falls to nothing
    t = ts(d); f = 180 * (1 - t / d) ** 2 + 20
    ph = 2 * np.pi * np.cumsum(f) / SR; return lowpass(sum(np.sin(k * ph) / k for k in range(1, 6)), 1500) * (1 - t / d)
def rewind(d=.55):  # fast chirpy tape rewind
    t = ts(d); f = 900 + 700 * np.sin(2 * np.pi * 9 * t)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .5 + lowpass(noise(d), 4000) * .6) * np.sin(np.pi * t / d)

S = {os.path.splitext(os.path.basename(f))[0]: load(f) for f in glob.glob('sfx/*')}
sfx = np.zeros(N)
# S1 party, then the scratch
place(sfx, party_horn(), .05, .5)
for t0, f in ((.05, 620), (.15, 760), (.3, 880)): place(sfx, pop(f), t0, .4)
for k, f in enumerate((1568, 2093, 2637)): place(sfx, glock(f), .5 + k * .1, .18)
place(sfx, scratch(), 2.45, .7)
# S2 corporate kid
place(sfx, pop(600), 2.82, .45); place(sfx, ring(), 3.2, .35); place(sfx, pop(760), 3.9, .35)
place(sfx, stamp(), 4.5, .6); place(sfx, pop(700), 5.55, .35)
# S3 influencer
place(sfx, pop(640), 6.62, .45); place(sfx, shutter(), 7.0, .6); place(sfx, S['popup'], 7.05, .45)
place(sfx, pop(820), 7.45, .35); place(sfx, pop(700), 8.2, .35)
for t0 in (8.8, 9.3): place(sfx, pop(1200), t0, .16)
# S4 breaking news
place(sfx, news_sting(), 10.2, .5); place(sfx, pop(700), 10.6, .3)
# S5 WhatsApp University
place(sfx, pop(620), 14.02, .45); place(sfx, S['popup'], 14.6, .55); place(sfx, S['popup'], 17.0, .55)
for k in range(3): place(sfx, whoosh(.25), 17.5 + k * .12, .25)
# S6 burnt out: the device's own low-battery sound
place(sfx, pop(560), 18.4, .35); place(sfx, S['battery_low'], 19.35, .6); place(sfx, pop(640), 20.15, .3)
# S7 freeze, stamp, rewind
place(sfx, S['knob_click'], 20.8, .8); place(sfx, tape_stop(), 20.8, .35)
place(sfx, stamp(), 24.95, .7); place(sfx, rewind(), 25.35, .6)
# S8 Cheeko drops in: the real boot sound
place(sfx, whoosh(.35), 25.8, .45); place(sfx, S['boot_startup'][: int(SR * 1.2)], 25.95, .6)
for k, f in enumerate((1568, 2093, 2637)): place(sfx, glock(f), 26.15 + k * .1, .2)
# S9 kids being kids
place(sfx, pop(660), 27.0, .4); place(sfx, pop(800), 28.95, .4); place(sfx, S['popup'], 29.1, .35)
for t0 in (31.35, 31.5, 31.65): place(sfx, boing(), t0, .3)
# S10 end card
place(sfx, S['success'], 33.4, .5); place(sfx, whoosh(.45), 33.6, .35); place(sfx, party_horn(.45), 33.75, .35)
for k, f in enumerate((1319, 1568, 2093)): place(sfx, glock(f), 34.3 + k * .1, .2)

with wave.open('vo/vo-tight.wav') as w:
    vo = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
v = np.zeros(N); v[: min(N, len(vo))] = vo[:N]; v = v / np.abs(v).max() * .92
env = (np.abs(v) > .02).astype(float)
k = int(SR * .2); env = np.convolve(env, np.ones(k) / k, mode='same'); env = np.clip(env * 3, 0, 1)
k2 = int(SR * .1); env = np.convolve(env, np.ones(k2) / k2, mode='same')
t = np.arange(N) / SR
fade = np.minimum(1, t / .02) * np.clip((DUR - t) / .6, 0, 1) ** 1.3

def ramp(n, a, b, edge=.04):  # 0..1 gate between samples a and b with short fades
    g = np.zeros(n); a, b = max(0, a), min(n, b)
    if b <= a: return g
    g[a:b] = 1; e = int(SR * edge)
    g[a:min(b, a + e)] *= np.linspace(0, 1, min(b, a + e) - a); g[max(a, b - e):b] *= np.linspace(1, 0, b - max(a, b - e))
    return g

music = np.zeros(N)
src = sorted(glob.glob('music-src.*'))
if src:
    full = load(src[0]); full /= np.abs(full).max() + 1e-9
    L = len(full) / SR
    # thin = the song without its leads: bass + organ, drums at half (bass alone vanishes on phone speakers)
    stems = [f for f in glob.glob('music/**/*', recursive=True) if os.path.isfile(f) and any(s in f.lower() for s in ('bass', 'organ', 'drums'))]
    thin = sum(load(f) * (.5 if 'drums' in f.lower() else 1) for f in stems) if stems else lowpass(full, 500)
    thin = thin[: len(full)] / (np.abs(thin).max() + 1e-9)
    BAR = 60 / 114 * 4                                               # "Quirky Fun Sports Party Dance" is 114 BPM
    INTRO = float(os.environ.get('MUSIC_INTRO', 8 * BAR))            # the loud chorus (16.8 s) for "birthday party!"
    THIN = float(os.environ.get('MUSIC_THIN', 4 * BAR))              # bass + organ from 8.4 s for the grown-up scenes
    HIT_END = float(os.environ.get('MUSIC_END', 77.0))               # track time at the video's end: final hit (75.5 s) lands on the end card
    a1 = int(W(2.45) * SR)
    music[:a1] += full[int(INTRO * SR): int(INTRO * SR) + a1] * ramp(a1, 0, a1, .02)
    b0, b1 = int(W(2.8) * SR), int(W(20.8) * SR)
    seg = thin[int(THIN * SR): int(THIN * SR) + b1 - b0]; music[b0:b0 + len(seg)] += seg * ramp(len(seg), 0, len(seg), .3) * 1.2
    c0 = int(W(25.8) * SR)
    start = HIT_END - (N - c0) / SR; start = round(start / BAR) * BAR # snap so Cheeko lands on a downbeat
    tail = full[int(start * SR): int(start * SR) + N - c0]
    music[c0:c0 + len(tail)] += tail * ramp(len(tail), 0, len(tail), .03)
    print(f'intro from {INTRO:.2f}s, thin from {THIN:.2f}s, Cheeko section from {start:.2f}s (final hit at video {W(25.8) + 75.5 - start:.2f}s of {DUR}s)')
    print('music', src[0], f'{L:.1f}s', 'stems:', [os.path.basename(s) for s in stems] or 'none (low-passed full mix)')
else:
    print('no music-src.* yet: voice + sound effects only')
music_d = music * (1 - .55 * env) * .46
sfx_d = sfx * .9
mix = (music_d + sfx_d + v) * fade
mix = np.tanh(mix / np.abs(mix).max() * 1.3) * .9

def write(path, x):
    st = np.stack([x, np.roll(x, 12) * .98], axis=1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
write('music-final.wav', mix)
bed = music_d + sfx_d
write('music-only.wav', np.tanh(bed * fade / (np.abs(bed).max() + 1e-9) * 1.2) * .9)
print('ok', DUR, 's')
