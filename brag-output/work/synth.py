"""Original fun soundtrack for the Cheeko brag video: D major, 120 BPM, 22s."""
import numpy as np, wave

SR = 44100
DUR = 22.0
BEAT = 0.5
N = int(SR * DUR)
rng = np.random.default_rng(3)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[: j - i] * gain
def ts(d): return np.arange(int(SR * d)) / SR

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.zeros_like(x); s = 0.0
    for k in range(len(x)):
        s = (1 - a) * x[k] + a * s; y[k] = s
    return y

def marimba(f, d=.35):
    t = ts(d)
    return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*4*f*t)*np.exp(-t*40)) * np.exp(-t*11) * np.minimum(1, t/.002)
def glock(f, d=1.0):
    t = ts(d)
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*8)) * np.exp(-t*4) * np.minimum(1, t/.001)
def bassnote(f, d=.22):
    t = ts(d)
    s = np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)
    return s * np.exp(-t*7) * np.minimum(1, t/.004)
def kick():
    t = ts(.3); f = 48 + 90*np.exp(-t*35)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
def noise(d): return rng.uniform(-1, 1, int(SR*d))
def clap():
    t = ts(.18); x = noise(.18); x = x - lowpass(x, 900)
    e = np.exp(-t*30) + .6*np.exp(-np.maximum(t-.012,0)*30)*(t>.012) + .4*np.exp(-np.maximum(t-.024,0)*25)*(t>.024)
    return x * e * .6
def hat():
    x = noise(.05); x = x - lowpass(x, 7000)
    return x * np.exp(-ts(.05)*70)
def pop(f):
    t = ts(.18); ff = f*(1 + 1.2*np.exp(-t*45))
    return np.sin(2*np.pi*np.cumsum(ff)/SR) * np.exp(-t*22)
def whoosh(d=.3):
    t = ts(d); x = noise(d)
    x = lowpass(x, 3000) - lowpass(x, 400)
    return x * np.sin(np.pi*t/d)**2
def boing(f0=300, d=.45):
    t = ts(d); f = f0*(1 + .6*np.sin(2*np.pi*9*t)*np.exp(-t*4)) * (1 + t)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*5) * np.minimum(1, t/.005)

# D - A - Bm - G, one bar (2s) each
CH = [[62,66,69],[57,61,64],[59,62,66],[55,59,62]]
RT = [38, 33, 35, 31]
bars = int(DUR // 2)

mus = np.zeros(N); drm = np.zeros(N); sfx = np.zeros(N)
END = 20.0   # final downbeat

for b in range(bars):
    t0 = b*2.0; ch = CH[b % 4]; r = RT[b % 4]
    if t0 >= END:
        break
    full = t0 >= 2.0
    # bouncy octave bass in 8ths
    for i in range(8):
        if not full and i % 2: continue
        m = r + (12 if i % 2 else 0)
        place(mus, bassnote(hz(m)), t0 + i*BEAT/2, .55)
    # marimba off-beat skank
    for i in range(4):
        for m in ch:
            place(mus, marimba(hz(m+12)), t0 + i*BEAT + BEAT/2, .16)
    # glockenspiel hook (a little tune, repeats every 2 bars)
    hook = [(0, 2), (.5, 1), (1.0, 0), (1.25, 1), (1.5, 2)] if b % 2 == 0 else [(0, 1), (.5, 2), (.75, 1), (1.0, 0), (1.5, 1)]
    if full and not (14.5 <= t0 < 17):
        for k, idx in hook:
            place(mus, glock(hz(ch[idx]+24)), t0 + k, .16)
    # drums
    if full:
        for i in range(4):
            bt = t0 + i*BEAT
            if 14.5 <= bt < 15.5: continue     # breakdown under "No video. No feed. No ads."
            place(drm, kick(), bt, .75)
            if i % 2: place(drm, clap(), bt, .5)
            place(drm, hat(), bt + BEAT/2, .22)
            place(drm, hat(), bt + BEAT*.75, .08)

# final chord + sparkle
for m in (50, 62, 66, 69, 74):
    place(mus, glock(hz(m+12), 2.5), END, .14)
place(mus, bassnote(hz(38), 1.5), END, .6)
place(drm, kick(), END, .75)
place(drm, clap(), END, .4)

# hook intro: riser into the card landing on beat 1 (0.5s)
place(sfx, whoosh(.5)*np.linspace(0,1,int(SR*.5)), 0, .5)
t = ts(.4); land = np.sin(2*np.pi*np.cumsum(hz(50)*(1+.8*np.exp(-t*40)))/SR)*np.exp(-t*12)
place(sfx, land, .5, .7)
place(sfx, pop(hz(86)), .5, .25)
for i, m in enumerate((74, 78, 81, 86)):          # confetti sparkle
    place(sfx, glock(hz(m+12), .6), .55 + i*.06, .08)
place(sfx, pop(hz(81)), .6, .18)                  # "Insert a card."
place(sfx, pop(hz(86)), 1.0, .2)                  # "Stories play!"

# feature cuts: whoosh + a pop climbing the D major scale
scale = [74, 76, 78, 79, 81, 83, 85, 86]
for i, t0 in enumerate([2.5, 4, 5.5, 7, 8.5, 10, 11.5, 13]):
    place(sfx, whoosh(.28), t0 - .05, .35)
    place(sfx, pop(hz(scale[i])), t0 + .2, .3)
# per-scene candy
for k, t0 in enumerate((2.8, 2.86, 2.92, 2.98, 3.04)):   # cards fanning
    place(sfx, marimba(hz([74,78,81,86,90][k]+12), .25), t0, .12)
place(sfx, boing(420), 4.6, .16); place(sfx, boing(520), 4.85, .14)   # ? and ! bubbles
for i, t0 in enumerate((5.8, 6.3, 6.8)):                   # pictures drop in
    place(sfx, glock(hz([86, 90, 93][i]), .8), t0, .16)
for i in range(5): place(sfx, pop(hz(81 + 2*i)), 7.4 + i*.1, .12)  # game chips
for i in range(6): place(sfx, marimba(hz([74,76,78,81,83,86][i]+12), .25), 8.75 + i*.08, .12)  # glass tiles
st = noise(.25); st = (st - lowpass(st, 2500)) * np.exp(-ts(.25)*10)
place(sfx, st, 10.2, .10)                                  # radio tuning crackle
place(sfx, boing(260, .7), 11.8, .2)                       # funny voice
place(sfx, glock(hz(90), .6), 13.3, .12)                   # parent app
for i, t0 in enumerate((14.75, 15.0, 15.25)):              # manifesto
    place(sfx, clap(), t0, .55); place(sfx, pop(hz([74, 78, 81][i])), t0, .22)
place(sfx, whoosh(.45)*np.linspace(0, 1, int(SR*.45)), 15.05, .4)
place(sfx, kick(), 15.5, .7)                               # "All play." drop
for m in (74, 78, 81, 86): place(sfx, glock(hz(m+12), 1.0), 15.5, .07)
place(sfx, whoosh(.3), 16.95, .35)                         # outro slide
for i in range(8):                                         # confetti sparkle
    place(sfx, glock(hz([86,90,93,98,93,98,102,98][i]), .5), 18.0 + i*.05, .06)
place(sfx, pop(hz(86)), 18.5, .2)                          # price
place(sfx, pop(hz(90)), 19.0, .2)                          # pill

def reverb(x, secs=1.2, mix=0.15):
    n = int(SR*secs); t = np.arange(n)/SR
    ir = rng.normal(0, 1, n)*np.exp(-t*4.5); ir = lowpass(ir, 6000); ir /= np.sqrt((ir**2).sum())
    L = len(x)+n; F = 1 << (L-1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, F)*np.fft.rfft(ir, F), F)[:len(x)]
    return x*(1-mix) + wet*mix*3

mix = reverb(mus, mix=.18) + drm*.9 + reverb(sfx, mix=.25)*.8
t = np.arange(N)/SR
mix *= np.minimum(1, t/.02) * np.clip((DUR - t)/1.2, 0, 1)**1.3
mix = np.tanh(mix/np.abs(mix).max()*1.4)*.85
st = np.stack([mix, np.roll(mix, 14)*.98], axis=1)
with wave.open('music-final.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok', len(mix)/SR)
