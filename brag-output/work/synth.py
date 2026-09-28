"""Original soundtrack for the Cheeko brag video: D major, 96 BPM, 22.5s."""
import numpy as np, wave

SR = 44100
DUR = 22.5
BEAT = 60 / 96
N = int(SR * DUR)
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r, sustain=True):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    return e * np.exp(-t / r) if not sustain else e
def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[: j - i] * gain

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.zeros_like(x); s = 0.0
    for k in range(len(x)):  # one-pole, fine for these lengths
        s = (1 - a) * x[k] + a * s; y[k] = s
    return y

def pluck(freq, dur, bright=0.5):
    n = int(SR * dur); p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for k in range(n):
        out[k] = buf[k % p]
        buf[k % p] = 0.5 * (buf[k % p] + buf[(k + 1) % p]) * (0.994 + 0.004 * bright)
    return out * env(n, 0.002, dur * 0.5, sustain=False)

def bell(freq, dur, amt=1.0):
    t = np.arange(int(SR * dur)) / SR
    mod = amt * 2.2 * np.exp(-t * 3) * np.sin(2 * np.pi * freq * 3.5 * t)
    return np.sin(2 * np.pi * freq * t + mod) * np.exp(-t * 2.2) * np.minimum(1, t / 0.003)

def pad_chord(notes, dur):
    t = np.arange(int(SR * dur)) / SR; s = np.zeros_like(t)
    for m in notes:
        for d in (-0.08, 0.0, 0.08):
            f = hz(m) * 2 ** (d / 12)
            s += np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    e = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return s * e / (len(notes) * 3)

# progression, one chord per bar (4 beats = 2.5s)
D, Bm, G, A = [62, 66, 69, 73], [59, 62, 66, 69], [55, 59, 62, 66], [57, 61, 64, 69]
prog = [D, Bm, G, A, D, Bm, G, A, D]
roots = [38, 35, 31, 33, 38, 35, 31, 33, 38]
BAR = BEAT * 4

pad = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N); sfx = np.zeros(N)

for b, (ch, r) in enumerate(zip(prog, roots)):
    t0 = b * BAR
    last = b == len(prog) - 1
    place(pad, pad_chord(ch, BAR + (1.6 if last else 0.4)), t0, 0.5)
    # sub bass: root on beat 1, fifth on beat 3
    for k, m in ((0, r), (2, r + 7 if not last else r)):
        if last and k == 2: continue
        n = int(SR * BEAT * (2 if not last else 4)); t = np.arange(n) / SR
        place(bass, np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / .01) * np.exp(-t / 0.9), t0 + k * BEAT, 0.55)
    if last:
        continue
    # plucked arpeggio in 8ths (starts at bar 0, thinner in bar 0)
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    for i, idx in enumerate(pattern):
        if b == 0 and i % 2: continue
        m = ch[idx] + 12
        place(arp, pluck(hz(m), 0.9, bright=0.6), t0 + i * BEAT / 2, 0.32 if i % 2 else 0.42)

# light kick + shaker from scene 2 (4.375s) up to resolution at 20.0s
def kick():
    t = np.arange(int(SR * .35)) / SR
    f = 50 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
def shaker():
    n = int(SR * .08); x = rng.uniform(-1, 1, n)
    x = x - lowpass(x, 5000)
    return x * np.exp(-np.arange(n) / SR * 45)
bt = 4.375
while bt < 20.0 - 1e-6:
    k = round(bt / BEAT)
    if k % 2 == 0: place(drums, kick(), bt, 0.5)
    place(drums, shaker(), bt + BEAT / 2, 0.10)
    bt += BEAT

# sfx, tuned to D
def thock(freq):  # soft card-landing thud in key
    t = np.arange(int(SR * .5)) / SR
    f = freq * (1 + 0.6 * np.exp(-t * 40))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)
    click = lowpass(rng.uniform(-1, 1, len(t)), 2500) * np.exp(-t * 90)
    return body + 0.6 * click
place(sfx, thock(hz(50)), 1.25, 0.5)                 # card lands (D3)
place(sfx, bell(hz(81), 2.5), 1.35, 0.16)            # chip pop (A5)
for t0 in (10.0, 12.5):                               # pictures appear
    place(sfx, bell(hz(86), 2.5), t0, 0.18)           # D6
    place(sfx, bell(hz(90), 2.5), t0 + 0.08, 0.12)    # F#6
    place(sfx, bell(hz(93), 2.5), t0 + 0.16, 0.09)    # A6
# soft typing ticks under the wish text
for a, b_, chars in ((9.35, 9.95, 24), (11.5, 12.35, 34)):
    for i in range(0, chars, 3):
        place(sfx, bell(hz(98), .15, amt=.3), a + (b_ - a) * i / chars, 0.03)
for i, t0 in enumerate((13.9, 14.3, 14.7)):          # manifesto lines
    place(sfx, pluck(hz([74, 78, 81][i]), .8), t0, 0.35)
place(sfx, bell(hz(86), 3.0), 15.0, 0.22)            # "All play."
place(sfx, bell(hz(74), 3.0), 15.0, 0.15)
# swell into the outro
sw_t = np.arange(int(SR * 1.2)) / SR
swell = lowpass(rng.uniform(-1, 1, len(sw_t)), 1800) * (sw_t / 1.2) ** 2
place(sfx, swell, 16.3, 0.12)
place(sfx, bell(hz(74), 4.0), 17.5, 0.2)
place(sfx, bell(hz(81), 4.0), 17.5, 0.12)

def reverb(x, secs=1.8, mix=0.22):
    n = int(SR * secs); t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.2); ir = lowpass(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n; F = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[: len(x)]
    return x * (1 - mix) + wet * mix * 3

pad = lowpass(pad, 2200)
music = pad * 0.55 + arp * 0.6 + bass * 0.7 + drums * 0.55
mix = reverb(music, mix=0.2) + reverb(sfx * 0.8, mix=0.3)
# gentle intro fade and tail fade
t = np.arange(N) / SR
mix *= np.minimum(1, t / 0.08) * np.clip((DUR - t) / 2.0, 0, 1) ** 1.5
mix = np.tanh(mix / np.abs(mix).max() * 1.2) * 0.85
st = np.stack([mix, np.roll(mix, 12) * 0.98], axis=1)
with wave.open('music-final.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok', len(mix) / SR)
