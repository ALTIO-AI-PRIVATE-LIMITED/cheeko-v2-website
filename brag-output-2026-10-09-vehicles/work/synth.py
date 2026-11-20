"""Music + sound effects for one level of V31 (on-device quiz), driven by cues_L<level>.json and vo/vo_L<level>.wav.
Usage: python3 synth.py <level>. Each level is a step brighter: Level 1 D major 112 BPM, Level 2 E major 118, Level 3 F major 124.
Original music (key and tempo per level, above): marimba offbeats, glockenspiel tune, plucked bass voiced high enough for Cheeko's small
speaker, soft shaker. Countdown: three wood-block ticks (rising), a chime on the reveal, a water whoosh on every wave wipe.
Music ducks under the voice and dips during each countdown. Writes music-final.wav and music-only.wav (48 kHz)."""
import json, sys, wave, numpy as np
LV = int(sys.argv[1]) if len(sys.argv) > 1 else 1
KEY, BPM = {1: (0, 112), 2: (2, 118), 3: (3, 124)}[LV]
SR = 48000
C = json.load(open(f'cues_L{LV}.json')); DUR = C['dur']; N = int(SR * DUR); rng = np.random.default_rng(30)
def hz(m): return 440 * 2 ** ((m + KEY - 69) / 12)
def ts(d): return np.arange(int(SR * d)) / SR
def place(buf, sig, t0, g=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[:j - i] * g
def onepole(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for k in range(len(x)): s = (1 - a) * x[k] + a * s; y[k] = s
    return y
def noise(d): return rng.uniform(-1, 1, int(SR * d))
def marimba(f, d=.35): t = ts(d); return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*4*f*t)*np.exp(-t*40)) * np.exp(-t*11) * np.minimum(1, t/.002)
def glock(f, d=1.0): t = ts(d); return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*8)) * np.exp(-t*4) * np.minimum(1, t/.001)
def pluck(f, d=.3):   # bass with strong 2nd/3rd harmonics so it survives a small speaker
    t = ts(d); return (np.sin(2*np.pi*f*t) + .55*np.sin(2*np.pi*2*f*t) + .3*np.sin(2*np.pi*3*f*t)) * np.exp(-t*9) * np.minimum(1, t/.003)
SHAKE = (lambda x: (x - onepole(x, 5000)) * np.exp(-ts(.06) * 55))(noise(.06))
def block(f):         # wood-block tick
    t = ts(.12); return (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*2.4*f*t)*np.exp(-t*80)) * np.exp(-t*38) * np.minimum(1, t/.0008)
def pop(f): t = ts(.16); ff = f * (1 + 1.1*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(ff)/SR) * np.exp(-t*24)
def whoosh(d=.45):    # water swoosh: band of noise sweeping up then down, plus a few bubble blips
    t = ts(d); x = noise(d); lo = onepole(x, 700); hi = onepole(x, 2600); y = (hi - lo) * np.sin(np.pi * t / d) ** 2
    for k in range(5): place(y, pop(hz(80 + 3 * k)) * .25, d * (.2 + .13 * k))
    return y * .8

mus, sfx = np.zeros(N), np.zeros(N)
CH = [[62, 66, 69], [57, 61, 64], [59, 62, 66], [55, 59, 62]]; RT = [50, 45, 47, 43]     # D A Bm G
TUNE = [[74, 0, 76, 78, 0, 76, 74, 0], [73, 0, 74, 76, 0, 73, 69, 0], [71, 0, 73, 74, 0, 78, 76, 0], [74, 0, 71, 74, 0, 76, 74, 0]]
BEAT = 60 / BPM; BAR = 4 * BEAT
end = C['outro'] + 7.0
b, t0 = 0, 0.0
while t0 < end:
    ch, r = CH[b % 4], RT[b % 4]
    for i in range(8):
        tt = t0 + i * BEAT / 2
        if tt >= end: break
        if i % 2 == 0: place(mus, pluck(hz(r + (12 if i % 4 == 2 else 0))), tt, .5)
        else:
            for m in ch: place(mus, marimba(hz(m + 12)), tt, .12)
        place(mus, SHAKE, tt, .10 if i % 2 else .05)
        m = TUNE[b % 4][i]
        if m and b % 8 not in (6, 7): place(mus, glock(hz(m + 12), .9), tt, .07)
    b += 1; t0 += BAR
for m in (62, 66, 69, 74, 78): place(mus, glock(hz(m + 12), 2.5), end, .12)
place(mus, pluck(hz(50), 1.4), end, .5)

for k, t in enumerate(C['ticks']): place(sfx, block(hz(84 + 2 * (k % C['answer']))), t, .55)
for t in C['reveals']:
    for k, m in enumerate((86, 90, 93, 98)): place(sfx, glock(hz(m), 1.1), t + k * .055, .16)
    place(sfx, pop(hz(88)), t, .25)
for t in C['whooshes']: place(sfx, whoosh(), t - .05, .5)
for t in C['introPops'] + C['outroPops']: place(sfx, pop(hz(86)), t, .22)

def reverb(x, secs=1.0, mix=.15):
    n = int(SR * secs); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 5); ir = onepole(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n; F = 1 << (L - 1).bit_length(); wet = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
    return x * (1 - mix) + wet * mix * 3
music = reverb(mus, mix=.14); music = music / np.abs(music).max() * .9
fx = reverb(sfx, mix=.12); fx = fx / np.abs(fx).max() * .9
with wave.open(f'vo/vo_L{LV}.wav') as w: vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
v = np.zeros(N); v[:min(N, len(vo))] = vo[:N]; v = v / np.abs(v).max() * .92
env = (np.abs(v) > .02).astype(float); k = int(SR * .2); env = np.convolve(env, np.ones(k) / k, 'same'); env = np.clip(env * 3, 0, 1)
env = np.convolve(env, np.ones(int(SR * .1)) / int(SR * .1), 'same')
t = np.arange(N) / SR
cd = np.zeros(N)                                  # dip the music while the child guesses
for s in C['roundStarts']: cd += np.clip(np.minimum((t - s - C['tick0'] + .15) / .15, (s + C['reveal'] + .05 - t) / .15), 0, 1)
fade = np.minimum(1, t / .02) * np.clip((DUR - t) / 1.2, 0, 1) ** 1.3
bed = music * (1 - .65 * env) * (1 - .45 * cd) * .30
mix = (bed + fx * .55 + v) * fade; mix = np.tanh(mix / np.abs(mix).max() * 1.25) * .9
def write(p, x):
    st = np.stack([x, x], 1)
    with wave.open(p, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
write(f'music-final_L{LV}.wav', mix); write(f'music-only_L{LV}.wav', np.tanh((music * .30 + fx * .55) * fade * 1.25) * .9)
print('audio', DUR, 's')
