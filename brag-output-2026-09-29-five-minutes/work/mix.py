"""Audio for V06 "Five Minutes": voiceover + sound effects + (optional) licensed music, ducked under the voice.
Real Cheeko sounds (sfx/): doorbell and clock from the Sounds Around Me card, the device's own low-battery,
charge-full, card-insert, success and popup sounds. Pops, stamps, whooshes and the sad trombone are synthesised.
Music: put the licensed track at music-src.(mp3|wav) and set MUSIC_START (seconds into the track) if needed.
V06 uses Envato Elements "Sneaky Pizzicato Comedy" by Korolkov (Lifetime Commercial License, CFT360 Design Studio
workspace, downloaded 2026-09-29) with MUSIC_START=48.0 so the track's real ending lands on the end card.
Writes music-final.wav (full mix, used by render.mjs/finish.sh) and music-only.wav (music + sfx, no voice).
Usage (inside work/): ../../.venv/bin/python mix.py"""
import glob, json, os, subprocess
import numpy as np, wave

SR = 44100
WJ = json.load(open('warp.json'))
DUR = WJ['dur']; N = int(SR * DUR)
rng = np.random.default_rng(6)
_OLD = [0.0] + WJ['old']; _NEW = [0.0] + WJ['new']
def W(t):  # scene timeline -> voice-anchored timeline (same map as compose.html)
    return float(np.interp(t, _OLD, _NEW)) if t <= _OLD[-1] else _NEW[-1] + (t - _OLD[-1])

def ts(d): return np.arange(int(SR * d)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def load(path):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    return np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
def place(buf, sig, t_scene, gain=1.0, raw=False):
    i = int((t_scene if raw else W(t_scene)) * SR); j = min(len(buf), i + len(sig))
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
def stamp():  # rubber stamp: low thump + a papery slap
    t = ts(.35); f = 60 + 90 * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    slap = lowpass(noise(.35), 2500) * np.exp(-t * 45) * 2.2
    return body + slap
def whoosh(d=.32):
    t = ts(d); x = noise(d); x = lowpass(x, 3200) - lowpass(x, 500)
    return x * np.sin(np.pi * t / d) ** 2 * 1.4
def glock(f, d=.8):
    t = ts(d)
    return (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 8)) * np.exp(-t * 5) * np.minimum(1, t / .001)
def boing(d=.5):
    t = ts(d); f = 220 * (1 + .35 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 4))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
def trombone_note(f, d, vib=0.0):
    t = ts(d); ff = f * (1 + vib * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(ff) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 7))
    env = np.minimum(1, t / .04) * np.minimum(1, (d - t) / .08)
    return lowpass(x * env, 1400)
def sad_trombone():
    notes = [(hz(55), .3), (hz(54), .3), (hz(53), .3), (hz(52), .9)]
    out = []
    for k, (f, d) in enumerate(notes): out.append(trombone_note(f, d, .012 if k == 3 else 0))
    return np.concatenate(out)

S = {os.path.splitext(os.path.basename(f))[0]: load(f) for f in glob.glob('sfx/*')}
sfx = np.zeros(N)
# S1 hook
place(sfx, pop(650), .05, .5); place(sfx, S['popup'], 1.0, .6)
for t0 in (.6, 1.2, 1.9): place(sfx, pop(1100), t0, .18)
# S2 handoff
place(sfx, pop(600), 3.42, .5); place(sfx, stamp(), 3.8, .55)
place(sfx, pop(700), 4.12, .5); place(sfx, stamp(), 4.5, .55)
place(sfx, whoosh(), 4.8, .35); place(sfx, pop(520), 4.95, .5); place(sfx, S['popup'], 5.8, .55)
# S3 five minutes grows: the real clock ticks underneath
tick = np.concatenate([S['clock']] * 2)[: int(SR * (W(11.1) - W(7.0)))]
tick = tick * np.minimum(1, np.arange(len(tick)) / (SR * .1)) * np.minimum(1, (len(tick) - np.arange(len(tick))) / (SR * .2))
place(sfx, tick, 7.0, .35)
for t0, f in ((7.05, 600), (8.0, 700), (9.2, 800)): place(sfx, pop(f), t0, .5)
place(sfx, boing(), 10.2, .45); place(sfx, stamp(), 10.2, .4)
# S4 low battery: the device's own sounds
for t0 in (11.2, 11.4, 11.6): place(sfx, pop(560), t0, .35)
place(sfx, S['battery_low'], 12.2, .6); place(sfx, pop(900), 13.0, .4); place(sfx, S['charge_full'], 13.4, .6)
# S5 the rival: the real doorbell
place(sfx, S['doorbell'][: int(SR * 1.6)] * np.linspace(1, .2, int(SR * 1.6)), 14.45, .75)
place(sfx, whoosh(.4), 14.95, .45)
for k, f in enumerate((1568, 2093, 2637)): place(sfx, glock(f), 15.25 + k * .12, .22)
# S6 the "flaws"
place(sfx, pop(620), 16.8, .45); place(sfx, pop(760), 16.9, .45)
for t0 in (17.2, 18.1, 19.0): place(sfx, stamp(), t0, .6)
# S7 Nani
place(sfx, pop(600), 20.0, .4); place(sfx, S['card_insert'], 20.1, .6)
place(sfx, whoosh(), 20.2, .35); place(sfx, pop(480), 20.3, .5); place(sfx, S['popup'], 21.7, .5)
# S8 together; the phone lands on the fridge
for t0 in (22.8, 22.9, 23.0): place(sfx, pop(640), t0, .35)
place(sfx, whoosh(.3), 24.45, .4); place(sfx, stamp(), 24.75, .35); place(sfx, sad_trombone(), 24.9, .22)
# S9 end card
place(sfx, S['success'], 26.5, .55); place(sfx, whoosh(.45), 26.75, .35); place(sfx, pop(700), 27.0, .4)
for k, f in enumerate((1319, 1568, 2093)): place(sfx, glock(f), 27.35 + k * .1, .2)
place(sfx, pop(820), 27.75, .4)

with wave.open('vo/vo-tight.wav') as w:
    vo = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
v = np.zeros(N); v[: min(N, len(vo))] = vo[:N]; v = v / np.abs(v).max() * .92

env = (np.abs(v) > .02).astype(float)
k = int(SR * .2); env = np.convolve(env, np.ones(k) / k, mode='same'); env = np.clip(env * 3, 0, 1)
k2 = int(SR * .1); env = np.convolve(env, np.ones(k2) / k2, mode='same')
t = np.arange(N) / SR
# short tail fade: the track is placed so its own ending hit lands on the end card
fade = np.minimum(1, t / .02) * np.clip((DUR - t) / .6, 0, 1) ** 1.3

music = np.zeros(N)
src = sorted(glob.glob('music-src.*'))
if src:
    m = load(src[0]); a = int(float(os.environ.get('MUSIC_START', '48.0')) * SR)
    m = m[a: a + N]; music[: len(m)] = m
    music = music / (np.abs(music).max() + 1e-9) * .9
    print('music', src[0], 'from', os.environ.get('MUSIC_START', '48.0'), 's')
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
