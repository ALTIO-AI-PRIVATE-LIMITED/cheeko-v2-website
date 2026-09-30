"""Original soundtrack + VO mix for the Cheeko Reel (script A, MiniMax English_radiant_girl), 26.5s.
Tense hook (tick + pulse, scratch on "NO"), groove drops with the sun burst at 3.25 (D major, 120 BPM),
hard stop on "Just…", restarts on "play!", resolves on D under the outro. Music ducks under the voice."""
import numpy as np, wave

SR = 44100
DUR = 31.45
N = int(SR * DUR)
rng = np.random.default_rng(3)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def ts(d): return np.arange(int(SR * d)) / SR
def place_raw(buf, sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[: j - i] * gain

import json as _json
_W = _json.load(open("warp.json"))
_OLD = [0.0] + _W["old"]; _NEW = [0.0] + _W["new"]
def W(t):  # old timeline -> new (voice-anchored) timeline
    return float(np.interp(t, _OLD, _NEW)) if t <= _OLD[-1] else _NEW[-1] + (t - _OLD[-1])
def place(buf, sig, t0, gain=1.0):
    place_raw(buf, sig, W(t0), gain)
def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
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
    return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)) * np.exp(-t*7) * np.minimum(1, t/.004)
def kick():
    t = ts(.3); f = 48 + 90*np.exp(-t*35)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9)
def noise(d): return rng.uniform(-1, 1, int(SR*d))
def clap():
    t = ts(.18); x = noise(.18); x = x - lowpass(x, 900)
    e = np.exp(-t*30) + .6*np.exp(-np.maximum(t-.012,0)*30)*(t>.012) + .4*np.exp(-np.maximum(t-.024,0)*25)*(t>.024)
    return x * e * .6
HAT = None
def hat():
    global HAT
    if HAT is None:
        x = noise(.05); HAT = (x - lowpass(x, 7000)) * np.exp(-ts(.05)*70)
    return HAT
def pop(f):
    t = ts(.18); ff = f*(1 + 1.2*np.exp(-t*45))
    return np.sin(2*np.pi*np.cumsum(ff)/SR) * np.exp(-t*22)
def whoosh(d=.3):
    t = ts(d); x = noise(d)
    x = lowpass(x, 3000) - lowpass(x, 400)
    return x * np.sin(np.pi*t/d)**2
def crash(d=1.2):
    t = ts(d); x = noise(d); x = x - lowpass(x, 5000)
    return x * np.exp(-t*3.5) * .5
def scratch():
    t = ts(.28); f = 900*np.abs(np.sin(2*np.pi*3.4*t)) + 120
    x = noise(.28) * .5 + np.sin(2*np.pi*np.cumsum(f)/SR)
    return lowpass(x, 2500) * np.sin(np.pi*t/.28)
def thump():
    t = ts(.35); f = 55 + 60*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*8)

mus = np.zeros(N); drm = np.zeros(N); sfx = np.zeros(N)

# ---- hook 0–3.25: tick + low pulse, scratch on "NO", bright stab on "tantrum" ----
for i in range(6):
    place(sfx, marimba(hz(95 if i % 2 == 0 else 90), .08), .15 + i*.25, .10)
for i in range(3):
    place(mus, bassnote(hz(35), .4), .15 + i*.5, .45)
place(sfx, scratch(), 1.6, .55)
place(sfx, kick(), 1.66, .6)
for m in (74, 78, 81): place(mus, marimba(hz(m), .5), 2.19, .25)
place(sfx, whoosh(.9)*np.linspace(0, 1, int(SR*.9)), 2.35, .5)                # riser into the burst

# ---- groove: D - A - Bm - G, bars of 2s. Runs 3.25–19.6, stops for "Just…", restarts on "play!" ----
CH = [[62,66,69],[57,61,64],[59,62,66],[55,59,62]]
RT = [38, 33, 35, 31]
def groove(start, end, bar0=0):
    b = 0
    while start + b*2.0 < end:
        t0 = start + b*2.0; ch = CH[(b+bar0) % 4]; r = RT[(b+bar0) % 4]
        for i in range(8):
            tt = t0 + i*.25
            if tt < end: place_raw(mus, bassnote(hz(r + (12 if i % 2 else 0))), tt, .55)
        for i in range(4):
            tt = t0 + i*.5 + .25
            if tt < end:
                for m in ch: place_raw(mus, marimba(hz(m+12)), tt, .15)
        hook = [(0, 2), (.5, 1), (1.0, 0), (1.25, 1), (1.5, 2)] if b % 2 == 0 else [(0, 1), (.5, 2), (.75, 1), (1.0, 0), (1.5, 1)]
        for k, idx in hook:
            if t0 + k < end: place_raw(mus, glock(hz(ch[idx]+24)), t0 + k, .13)
        for i in range(4):
            bt = t0 + i*.5
            if bt >= end: break
            place_raw(drm, kick(), bt, .8)
            if i % 2: place_raw(drm, clap(), bt, .5)
            place_raw(drm, hat(), bt + .25, .25); place_raw(drm, hat(), bt + .375, .09)
        b += 1
groove(W(3.25), W(19.6))
groove(W(20.42), W(24.8), bar0=0)
place(drm, crash(), 3.25, .5); place(drm, crash(), 20.42, .6)
# resolve on D
END = 24.8
for m in (50, 62, 66, 69, 74): place(mus, glock(hz(m+12), 2.5), END, .13)
place(mus, bassnote(hz(38), 1.5), END, .6); place(drm, kick(), END, .8); place(drm, crash(1.8), END, .4)

# ---- sweeteners on the visual beats ----
for i, m in enumerate((74, 78, 81, 86)): place(sfx, glock(hz(m+12), .6), 3.3 + i*.05, .08)     # sun burst
place(sfx, whoosh(.4), 4.05, .35); place(sfx, thump(), 4.45, .8)                                  # Cheeko lands
for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), 4.47 + k*.05, .06)
place(sfx, whoosh(.4)*np.linspace(0, 1, int(SR*.4)), 5.3, .3); place(sfx, thump(), 5.7, .6)      # card in
for k, m in enumerate((86, 90, 93, 98)): place(sfx, glock(hz(m), .7), 5.72 + k*.05, .06)
place(sfx, whoosh(.3), 6.45, .25)
place(sfx, pop(hz(88)), 8.15, .12)                                                                 # talks back punch
for t0, m in ((9.2, 81), (9.95, 85), (10.62, 88)): place(sfx, pop(hz(m)), t0, .18)                # glyphs
for k in range(10): place(sfx, pop(hz(81 + k*2)), 11.25 + k*.04, .05)
place(sfx, whoosh(.3), 12.62, .25)
for k in range(10): place(sfx, glock(hz(86 + (k*5) % 17), .25), 13.3 + k*.11, .025)              # typing
place(sfx, kick(), 15.08, .9); place(sfx, crash(), 15.08, .45)                                    # BOOM
for k, m in enumerate((86, 90, 93, 98, 102)): place(sfx, glock(hz(m), .8), 15.1 + k*.05, .07)
for t0 in (16.93, 17.85, 18.67): place(sfx, thump(), t0, .8); place(sfx, whoosh(.2), t0 - .1, .2)  # stamps
for i, t0 in enumerate((19.7, 19.85, 20.0)): place(sfx, pop(hz([83, 86, 90][i])), t0, .1)
for k in range(10): place(sfx, glock(hz([86,90,93,98,93,98,102,98,105,110][k]), .5), 20.44 + k*.05, .06)
place(sfx, whoosh(.3), 21.0, .3)
for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), 23.2 + k*.05, .06)   # Cheeko!
place(sfx, pop(hz(86)), 23.9, .1); place(sfx, pop(hz(90)), 24.2, .1)

def reverb(x, secs=1.0, mix=0.15):
    n = int(SR*secs); t = np.arange(n)/SR
    ir = rng.normal(0, 1, n)*np.exp(-t*5); ir = lowpass(ir, 6000); ir /= np.sqrt((ir**2).sum())
    L = len(x)+n; F = 1 << (L-1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, F)*np.fft.rfft(ir, F), F)[:len(x)]
    return x*(1-mix) + wet*mix*3

music = reverb(mus, mix=.16) + drm*.9 + reverb(sfx, mix=.2)*.8
music = music / np.abs(music).max() * .9

with wave.open('vo/vo-tight.wav') as w:
    vo = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
v = np.zeros(N); place_raw(v, vo, 0); v = v / np.abs(v).max() * .92

env = (np.abs(v) > .02).astype(float)
k = int(SR*.2); env = np.convolve(env, np.ones(k)/k, mode='same'); env = np.clip(env*3, 0, 1)
k2 = int(SR*.1); env = np.convolve(env, np.ones(k2)/k2, mode='same')
t = np.arange(N)/SR
fade = np.minimum(1, t/.02) * np.clip((DUR - t)/1.2, 0, 1)**1.3
music_d = music * (1 - .6*env) * .42
mix = (music_d + v) * fade
mix = np.tanh(mix/np.abs(mix).max()*1.3)*.9

def write(path, x):
    st = np.stack([x, np.roll(x, 12)*.98], axis=1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st*32767).astype(np.int16).tobytes())
write('music-final.wav', mix)
write('music-only.wav', np.tanh(music*.62*fade*1.3)*.9)   # for posting with the voice track muted / re-editing
for name, x in (('music', music_d*fade), ('vo', v)):
    print(name.ljust(5), ' '.join(f'{20*np.log10(np.sqrt(np.mean(x[i*SR:(i+1)*SR]**2))+1e-9):4.0f}' for i in range(int(DUR))))
print('ok', DUR)
