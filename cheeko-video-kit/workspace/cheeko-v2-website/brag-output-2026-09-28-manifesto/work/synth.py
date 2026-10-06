"""Original soundtrack + voiceover mix for the Cheeko manifesto, 37.5s.
A dim B-minor intro under the phone scenes, a warm lift into D major at 100 BPM when Cheeko
arrives, a calm stretch under "It's made to end", and a resolve on D. The music ducks under
the voiceover (Sarvam bulbul:v3, speaker kavya, trimmed clips in vo/trim/<speaker>/).
Usage: python synth.py [speaker]   -> music-final.wav (full mix) and music-only.wav (no VO)."""
import numpy as np, wave, sys

SR = 44100
DUR = 37.5
N = int(SR * DUR)
SPK = sys.argv[1] if len(sys.argv) > 1 else 'kavya'
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def ts(d): return np.arange(int(SR * d)) / SR
def place(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[: j - i] * gain

def lowpass(x, cutoff):
    # one-pole, vectorised via an IIR on blocks is overkill here; the signals are short
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
    for k in range(len(x)):
        s = (1 - a) * x[k] + a * s; y[k] = s
    return y

def keys(f, d=1.2):   # soft electric-piano-ish tone
    t = ts(d)
    s = np.sin(2*np.pi*f*t) + .18*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + .06*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
    return s * np.exp(-t*2.2) * np.minimum(1, t/.004)
def glock(f, d=1.0):
    t = ts(d)
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*8)) * np.exp(-t*4) * np.minimum(1, t/.001)
def bassnote(f, d=.5):
    t = ts(d)
    return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2*f*t)) * np.exp(-t*3.5) * np.minimum(1, t/.006)
def kick():
    t = ts(.3); f = 46 + 80*np.exp(-t*35)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*10)
def noise(d): return rng.uniform(-1, 1, int(SR*d))
_hp = None
def hat():
    x = noise(.05); x = x - lowpass(x, 7000)
    return x * np.exp(-ts(.05)*80)
def snap():
    t = ts(.12); x = noise(.12); x = x - lowpass(x, 1500)
    return x * np.exp(-t*40) * .5
def pop(f):
    t = ts(.18); ff = f*(1 + 1.2*np.exp(-t*45))
    return np.sin(2*np.pi*np.cumsum(ff)/SR) * np.exp(-t*22)
def whoosh(d=.4):
    t = ts(d); x = noise(d)
    x = lowpass(x, 2500) - lowpass(x, 300)
    return x * np.sin(np.pi*t/d)**2
def thump():
    t = ts(.35); f = 60 + 40*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
def pad(notes, d, bright=1.0):
    t = ts(d); s = np.zeros_like(t)
    for m in notes:
        for dt in (-.08, .08):
            f = hz(m)*2**(dt/12); s += np.sin(2*np.pi*f*t) + .15*bright*np.sin(2*np.pi*2*f*t)
    return s*np.minimum(1, t/.5)*np.minimum(1, np.maximum(0, d-t)/.5)/len(notes)

mus = np.zeros(N); drm = np.zeros(N); sfx = np.zeros(N)

# ---- intro 0–6.3: dim B minor, a clock tick, the phone's blue glow ----
place(mus, lowpass(pad([47, 50, 54, 59], 6.6, .3), 600), 0, .30)
for i in range(12):
    place(sfx, glock(hz(96 if i % 2 == 0 else 91), .06), .1 + i*.5, .035)
place(sfx, pop(hz(64)), .45, .08); place(sfx, pop(hz(62)), 1.8, .08)        # the two captions
place(sfx, whoosh(.9)*np.linspace(0, 1, int(SR*.9)), 5.45, .35)             # lift into the reveal

# ---- D major, 100 BPM: bars of 2.4s from 6.35 ----
BEAT = .6; BAR = 2.4; T0 = 6.35
D, A, Bm, G = [62,66,69], [61,64,69], [62,66,71], [62,67,71]
ROOT = {'D':38, 'A':33, 'Bm':35, 'G':31}
CH = {'D':D, 'A':A, 'Bm':Bm, 'G':G}
PROG = ['D','A','Bm','G','D','A','Bm','G','D','A','Bm','G','A','D']   # last two: tension, then home
for b, name in enumerate(PROG):
    t0 = T0 + b*BAR
    if t0 >= DUR: break
    ch, r = CH[name], ROOT[name]
    calm = 25.4 <= t0 < 31.0
    # warm pad on every bar
    place(mus, pad([n-12 for n in ch], BAR+.4, .6), t0, .20 if calm else .16)
    # bass: root on 1, fifth on 3 (sparse in the calm stretch)
    place(mus, bassnote(hz(r)), t0, .42)
    if not calm: place(mus, bassnote(hz(r+7)), t0 + 2*BEAT, .30)
    # keys: gentle eighth-note arpeggio
    arp = [ch[0], ch[1], ch[2], ch[1]+12, ch[2], ch[1], ch[0]+12, ch[2]]
    for i, m in enumerate(arp):
        if calm and i % 2: continue
        place(mus, keys(hz(m), .9), t0 + i*BEAT/2, .10 if not calm else .08)
    # drums from 11.75 (after "stories play"), out for the calm stretch, back for the outro
    if 11.1 <= t0 < 25.4 or t0 >= 31.0:
        for i in range(4):
            bt = t0 + i*BEAT
            place(drm, kick(), bt, .55 if i % 2 == 0 else .35)
            if i % 2: place(drm, snap(), bt, .35)
            place(drm, hat(), bt + BEAT/2, .12)

# ---- beats and sweeteners ----
for i, m in enumerate((74, 78, 81, 86, 90)): place(sfx, glock(hz(m), .8), 6.4 + i*.06, .07)   # Cheeko arrives
place(sfx, pop(hz(81)), 6.6, .14)
place(sfx, whoosh(.45)*np.linspace(0, 1, int(SR*.45)), 8.5, .25)                             # card drops
place(sfx, thump(), 8.95, .45)                                                                # lands in the slot
for k, m in enumerate((86, 90, 93, 98)): place(sfx, glock(hz(m), .7), 9.0 + k*.05, .06)       # world blooms
place(sfx, whoosh(.3), 11.7, .2)
for i, t0 in enumerate([14.45 + i*.09 for i in range(10)]):                                   # language glyphs
    place(sfx, pop(hz([74,76,78,81,83,86,88,90,93,95][i])), t0, .06)
place(sfx, whoosh(.35), 16.7, .22)
for k in range(10): place(sfx, glock(hz(86 + (k*5) % 17), .25), 17.0 + k*.085, .025)          # typing the wish
for k, m in enumerate((86, 90, 93, 98, 102)): place(sfx, glock(hz(m), .8), 18.3 + k*.12, .05) # drawing appears
place(sfx, pop(hz(90)), 18.95, .1)
for t0 in (20.05, 20.98, 21.97): place(sfx, thump(), t0, .5)                                  # No video / feed / ads
for k in range(5): place(sfx, pop(hz(81 + k*2)), 22.32 + k*.07, .05)                          # menu icons
place(sfx, kick(), 23.2, .6)                                                                  # All play!
for k in range(10): place(sfx, glock(hz([86,90,93,98,93,98,102,98,105,110][k]), .5), 23.22 + k*.05, .05)
for i, t0 in enumerate((23.4, 23.6, 23.8)): place(sfx, pop(hz([83, 86, 90][i])), t0, .08)
place(sfx, whoosh(.5), 25.2, .15)
place(sfx, whoosh(.4), 31.2, .18)
for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), 34.05 + k*.05, .05)  # childhood
place(sfx, pop(hz(86)), 34.8, .1); place(sfx, pop(hz(90)), 35.3, .1)
# final chord rings out
for m in (50, 62, 66, 69, 74): place(mus, glock(hz(m+12), 3.0), 35.15, .10)
place(mus, bassnote(hz(38), 2.0), 35.15, .5)

def reverb(x, secs=1.6, mix=0.2):
    n = int(SR*secs); t = np.arange(n)/SR
    ir = rng.normal(0, 1, n)*np.exp(-t*4.0); ir = lowpass(ir, 5000); ir /= np.sqrt((ir**2).sum())
    L = len(x)+n; F = 1 << (L-1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, F)*np.fft.rfft(ir, F), F)[:len(x)]
    return x*(1-mix) + wet*mix*3

music = reverb(mus, mix=.22) + drm*.8 + reverb(sfx, mix=.25)*.9

# ---- voiceover, placed where each line is timed in compose.html ----
VO = [('01', .5), ('02', 3.45), ('03', 6.6), ('04', 8.4), ('05', 11.85), ('06', 16.85),
      ('07', 20.05), ('08', 23.2), ('09', 25.65), ('10', 31.6)]
vo = np.zeros(N)
for n, t0 in VO:
    with wave.open(f'vo/trim/{SPK}/{n}.wav') as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
    place(vo, x, t0)
vo = vo / np.abs(vo).max() * .9

# duck the music under the voice (smoothed envelope, ~ -8 dB)
env = np.abs(vo) > .02
k = int(SR*.25); env = np.convolve(env.astype(float), np.ones(k)/k, mode='same')
env = np.clip(env*3, 0, 1)
k2 = int(SR*.12); env = np.convolve(env, np.ones(k2)/k2, mode='same')
music = music / np.abs(music).max() * .9
t = np.arange(N)/SR
fade = np.minimum(1, t/.05) * np.clip((DUR - t)/1.5, 0, 1)**1.3
music_d = music * (1 - .6*env) * .55
mix = (music_d + vo) * fade
mix = np.tanh(mix/np.abs(mix).max()*1.2)*.9

def write(path, x):
    st = np.stack([x, np.roll(x, 12)*.98], axis=1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st*32767).astype(np.int16).tobytes())
write('music-final.wav', mix)
write('music-only.wav', np.tanh(music*.55*fade*1.2)*.9)
# per-second levels, to check the balance without listening
for name, x in (('music', music_d*fade), ('vo', vo)):
    print(name.ljust(5), ' '.join(f'{20*np.log10(np.sqrt(np.mean(x[i*SR:(i+1)*SR]**2))+1e-9):4.0f}' for i in range(int(DUR))))
print('ok', DUR, SPK)
