"""Original soundtrack for the Cheeko card video: a bored B-minor intro, then D major at 120 BPM, 22.5s."""
import numpy as np, wave

SR = 44100
DUR = 22.5
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


def pad(notes, d):
    t = ts(d); s = np.zeros_like(t)
    for m in notes:
        for dt in (-.07, .07):
            f = hz(m)*2**(dt/12); s += np.sin(2*np.pi*f*t) + .2*np.sin(2*np.pi*2*f*t)
    return s*np.minimum(1, t/.3)*np.minimum(1, (d-t)/.3)/len(notes)

# D - A - Bm - G, one bar (2s) each, starting when Cheeko arrives at 3.0s
CH = [[62,66,69],[57,61,64],[59,62,66],[55,59,62]]
RT = [38, 33, 35, 31]
mus = np.zeros(N); drm = np.zeros(N); sfx = np.zeros(N)
START, END = 3.0, 21.0

# bored intro: dull B-minor pad and a clock tick
place(mus, lowpass(pad([47, 50, 54], 3.0), 700), 0, .22)
for i in range(6):
    tk = marimba(hz(95 if i % 2 == 0 else 90), .08)
    place(sfx, tk, .0 + i*.5, .12)
place(sfx, pop(hz(55)), .25, .25)                     # "Kid bored?"
t = ts(.35); buzz = np.sign(np.sin(2*np.pi*hz(35)*t)) * np.exp(-t*8)
place(sfx, lowpass(buzz, 1200), 1.3, .3)             # ✕ stamp
place(sfx, kick(), 1.3, .5)
place(sfx, pop(hz(57)), 1.4, .2)                      # "Skip the phone."
place(sfx, whoosh(.6)*np.linspace(0, 1, int(SR*.6)), 2.4, .55)   # riser into the drop

b = 0
while START + b*2.0 < END:
    t0 = START + b*2.0; ch = CH[b % 4]; r = RT[b % 4]
    for i in range(8):
        place(mus, bassnote(hz(r + (12 if i % 2 else 0))), t0 + i*BEAT/2, .55)
    for i in range(4):
        for m in ch:
            place(mus, marimba(hz(m+12)), t0 + i*BEAT + BEAT/2, .16)
    hook = [(0, 2), (.5, 1), (1.0, 0), (1.25, 1), (1.5, 2)] if b % 2 == 0 else [(0, 1), (.5, 2), (.75, 1), (1.0, 0), (1.5, 1)]
    for k, idx in hook:
        place(mus, glock(hz(ch[idx]+24)), t0 + k, .14)
    for i in range(4):
        bt = t0 + i*BEAT
        place(drm, kick(), bt, .75)
        if i % 2: place(drm, clap(), bt, .5)
        place(drm, hat(), bt + BEAT/2, .22)
        place(drm, hat(), bt + BEAT*.75, .08)
    b += 1

for m in (50, 62, 66, 69, 74):
    place(mus, glock(hz(m+12), 2.5), END, .14)
place(mus, bassnote(hz(38), 1.5), END, .6)
place(drm, kick(), END, .75); place(drm, clap(), END, .4)

# Cheeko arrives
for i, m in enumerate((74, 78, 81, 86)): place(sfx, glock(hz(m+12), .6), 3.05 + i*.05, .09)
place(sfx, pop(hz(86)), 3.5, .2)                        # "Hand them Cheeko."
for k in range(4): place(sfx, marimba(hz([74,78,81,86][k]+12), .25), 3.7 + k*.07, .12)   # cards fan
place(sfx, whoosh(.3), 5.15, .3)                        # cards tucked away
place(sfx, pop(hz(81)), 5.45, .2)                       # "Insert a card…"
# three rounds: card drops, lands on the beat, the world blooms
for i, r0 in enumerate((5.5, 8.0, 10.5)):
    if i: place(sfx, boing(520 + i*60, .35), r0 - .05, .12)          # previous card pops out
    place(sfx, whoosh(.45)*np.linspace(0, 1, int(SR*.45)), r0 + .05, .3)
    t = ts(.4); land = np.sin(2*np.pi*np.cumsum(hz(50)*(1 + .8*np.exp(-t*40)))/SR)*np.exp(-t*12)
    place(sfx, land, r0 + .5, .6)
    base = [86, 88, 90][i]
    for k, m in enumerate((base, base+4, base+7, base+12)):
        place(sfx, glock(hz(m), .7), r0 + .55 + k*.05, .07)
    place(sfx, pop(hz([81, 83, 85][i])), r0 + .6, .2)
for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), 6.0 + k*.05, .05)   # confetti
place(sfx, boing(640, .35), 12.95, .12)
# proof
place(sfx, whoosh(.3), 12.95, .35)
for i, t0 in enumerate((13.2, 13.45, 13.95, 14.45)): place(sfx, pop(hz([81, 83, 85, 86][i])), t0, .2)
# outro
place(sfx, whoosh(.3), 15.95, .35)
for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), 17.0 + k*.05, .06)
place(sfx, pop(hz(86)), 17.5, .2)
place(sfx, pop(hz(90)), 18.0, .2)

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
