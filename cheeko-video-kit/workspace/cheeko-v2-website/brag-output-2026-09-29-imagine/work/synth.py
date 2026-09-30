"""Music + sound effects for a feature Reel, driven by cues.json (shots, bubbles, cards...) and the voice in vo/vo-tight.wav.
D major, 120 BPM groove; real device sounds for card insert and knob click; music ducks under the voice. Writes music-final.wav."""
import json, wave, subprocess, numpy as np
from pathlib import Path
SR = 44100
C = json.load(open('cues.json')); DUR = C['dur']; N = int(SR * DUR); rng = np.random.default_rng(5)
FW = Path('/Users/ravikumar/Cheeko Master/cheeko-os-v2/main/assets/common')
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def ts(d): return np.arange(int(SR * d)) / SR
def place(buf, sig, t0, g=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[:j - i] * g
def lp(x, fc):
    a = np.exp(-2*np.pi*fc/SR); y = np.empty_like(x); s = 0.0
    for k in range(len(x)): s = (1-a)*x[k] + a*s; y[k] = s
    return y
def noise(d): return rng.uniform(-1, 1, int(SR*d))
def marimba(f, d=.35): t = ts(d); return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*4*f*t)*np.exp(-t*40))*np.exp(-t*11)*np.minimum(1, t/.002)
def glock(f, d=1.0): t = ts(d); return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*8))*np.exp(-t*4)*np.minimum(1, t/.001)
def bass(f, d=.22): t = ts(d); return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t))*np.exp(-t*7)*np.minimum(1, t/.004)
def kick(): t = ts(.3); f = 48 + 90*np.exp(-t*35); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
HAT = (lambda x: (x - lp(x, 7000))*np.exp(-ts(.05)*70))(noise(.05))
def clap():
    t = ts(.18); x = noise(.18); x = x - lp(x, 900)
    return x*(np.exp(-t*30) + .6*np.exp(-np.maximum(t-.012, 0)*30)*(t > .012))*.6
def pop(f): t = ts(.18); ff = f*(1 + 1.2*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*22)
def whoosh(d=.3): t = ts(d); x = noise(d); x = lp(x, 3000) - lp(x, 400); return x*np.sin(np.pi*t/d)**2
def thump(): t = ts(.35); f = 55 + 60*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)
def crash(d=1.2): t = ts(d); x = noise(d); x = x - lp(x, 5000); return x*np.exp(-t*3.5)*.5
def device_sound(name):
    try:
        raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', str(FW / name), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
        x = np.frombuffer(raw, np.int16).astype(float)/32768; return x/(np.abs(x).max() + 1e-9)
    except Exception: return None
CARD, KNOB = device_sound('card_insert.ogg'), device_sound('knob_click.ogg')

mus, drm, sfx = np.zeros(N), np.zeros(N), np.zeros(N)
CH = [[62,66,69],[57,61,64],[59,62,66],[55,59,62]]; RT = [38, 33, 35, 31]
end = (C.get('outro') or DUR - 3) + 1.4
drums_from = C['shots'][1][0] if len(C['shots']) > 1 else 1.0
calm = C.get('calm') or []   # [[from, to], ...] stretches without drums
b = 0; t0 = 0.0
while t0 < end:
    ch, r = CH[b % 4], RT[b % 4]
    for i in range(8):
        tt = t0 + i*.25
        if tt < end: place(mus, bass(hz(r + (12 if i % 2 else 0))), tt, .5)
    for i in range(4):
        tt = t0 + i*.5 + .25
        if tt < end:
            for m in ch: place(mus, marimba(hz(m+12)), tt, .13)
    for k, idx in ([(0, 2), (.5, 1), (1.0, 0), (1.25, 1), (1.5, 2)] if b % 2 == 0 else [(0, 1), (.5, 2), (.75, 1), (1.0, 0), (1.5, 1)]):
        if t0 + k < end: place(mus, glock(hz(ch[idx]+24)), t0 + k, .11)
    for i in range(4):
        bt = t0 + i*.5
        if bt >= end or bt < drums_from or any(a <= bt < z for a, z in calm): continue
        place(drm, kick(), bt, .7)
        if i % 2: place(drm, clap(), bt, .45)
        place(drm, HAT, bt + .25, .22); place(drm, HAT, bt + .375, .08)
    b += 1; t0 += 2.0
for m in (50, 62, 66, 69, 74): place(mus, glock(hz(m+12), 2.5), end, .13)
place(mus, bass(hz(38), 1.5), end, .6); place(drm, kick(), end, .7); place(drm, crash(1.8), end, .35)

for t, kind in C['shots'][1:]: place(sfx, whoosh(.3), t - .05, .28)
for t in C['bubbles']: place(sfx, pop(hz(84)), t, .1)
for t in C['cards']: place(sfx, CARD if CARD is not None else thump(), t, .5 if CARD is not None else .6)
for t in C['presses']: place(sfx, KNOB if KNOB is not None else pop(hz(90)), t, .45)
for t in C['flashes']:
    place(sfx, kick(), t, .8); place(sfx, crash(), t, .35)
    for k, m in enumerate((86, 90, 93, 98, 102)): place(sfx, glock(hz(m), .8), t + .02 + k*.05, .06)
for t in C['stamps']: place(sfx, thump(), t, .75)
for k, t in enumerate(C['letters']): place(sfx, pop(hz(76 + k)), t, .12)
for t in C['pops']: place(sfx, pop(hz(86)), t, .1)
if C.get('lastLine'):
    for k in range(8): place(sfx, glock(hz([86,90,93,98,93,98,102,98][k]), .5), C['lastLine'] + .9 + k*.05, .05)

def reverb(x, secs=1.0, mix=.15):
    n = int(SR*secs); t = np.arange(n)/SR; ir = rng.normal(0, 1, n)*np.exp(-t*5); ir = lp(ir, 6000); ir /= np.sqrt((ir**2).sum())
    L = len(x) + n; F = 1 << (L-1).bit_length(); wet = np.fft.irfft(np.fft.rfft(x, F)*np.fft.rfft(ir, F), F)[:len(x)]
    return x*(1-mix) + wet*mix*3
music = reverb(mus, mix=.16) + drm*.9 + reverb(sfx, mix=.2)*.8; music = music/np.abs(music).max()*.9
with wave.open('vo/vo-tight.wav') as w: vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)/32768
v = np.zeros(N); v[:min(N, len(vo))] = vo[:N]; v = v/np.abs(v).max()*.92
env = (np.abs(v) > .02).astype(float); k = int(SR*.2); env = np.convolve(env, np.ones(k)/k, 'same'); env = np.clip(env*3, 0, 1)
env = np.convolve(env, np.ones(int(SR*.1))/int(SR*.1), 'same')
t = np.arange(N)/SR; fade = np.minimum(1, t/.02)*np.clip((DUR - t)/1.2, 0, 1)**1.3
mix = (music*(1 - .6*env)*.42 + v)*fade; mix = np.tanh(mix/np.abs(mix).max()*1.3)*.9
def write(p, x):
    st = np.stack([x, np.roll(x, 12)*.98], 1)
    with wave.open(p, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
write('music-final.wav', mix); write('music-only.wav', np.tanh(music*.42*fade*1.3)*.9)
print('music', DUR, 's')
