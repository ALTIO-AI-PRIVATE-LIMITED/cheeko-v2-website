"""Audio for the Bachpan film (English, sticker motion graphics, 55 s): the 14 voice lines where compose.html animates
them, light comic music that stops dead when Rohan's birthday smile fades, bedtime room tone, a soft warm music-box
theme for the ending, and sound effects. Comic music = placeholder from V06 (Envato "Sneaky Pizzicato Comedy",
licensed to Ravi's account); the ending theme is synthesised here. Writes music-final.wav and music-only.wav.
Usage (inside work/): ../../.venv/bin/python mix.py"""
import json, subprocess, wave, numpy as np
SR, DUR = 44100, 55.0
N = int(SR*DUR); rng = np.random.default_rng(11)
def load(p): return np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',p,'-ac','1','-ar',str(SR),'-f','s16le','-']), dtype=np.int16).astype(float)/32768
def trimmed(p):
    x = load(p); env = np.convolve(np.abs(x), np.ones(441)/441, mode='same'); on = np.nonzero(env > 0.006)[0]
    return x[max(0, on[0]-int(.03*SR)): min(len(x), on[-1]+int(.06*SR))]
def place(b, s, t, g=1.): i = int(t*SR); j = min(len(b), i+len(s)); b[i:j] += s[:j-i]*g
def ts(d): return np.arange(int(SR*d))/SR
def lowpass(x, c):
    a = np.exp(-2*np.pi*c/SR); y = np.empty_like(x); s = 0.
    for k in range(len(x)): s = (1-a)*x[k] + a*s; y[k] = s
    return y
def pop(f=700): t = ts(.16); ff = f*(1 + 1.3*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*24)
def whoosh(d=.4): t = ts(d); x = rng.uniform(-1, 1, len(t)); x = lowpass(x, 3000) - lowpass(x, 450); return x*np.sin(np.pi*t/d)**2*1.3
def shutter(): t = ts(.12); return lowpass(rng.uniform(-1, 1, len(t)), 5000)*(np.exp(-t*60) + .7*np.exp(-np.maximum(t-.05, 0)*60)*(t > .05))
def horn(d=.55):
    t = ts(d); f = 520 + 60*np.sin(2*np.pi*7*t); ph = 2*np.pi*np.cumsum(f)/SR
    return sum(np.sin(k*ph)/k for k in range(1, 8))*np.minimum(1, t/.03)*np.minimum(1, (d-t)/.08)*.5
def cricket(d=.5):
    t = ts(d); return np.sin(2*np.pi*4200*t)*(np.sin(2*np.pi*28*t) > .3)*np.sin(np.pi*t/d)*.4
def thunk(): t = ts(.25); f = 110 + 90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*18)
def bell(f, d=1.6):
    t = ts(d); return (np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + .15*np.sin(2*np.pi*3.01*f*t)*np.exp(-t*6))*np.exp(-t*2.4)*np.minimum(1, t/.004)

LIP = json.load(open('lipsync.json'))
T0 = [1.2, 2.4, 7.6, 9.9, 12.9, 17.0, 24.0, 26.9, 31.0, 32.8, 37.0, 42.6, 45.5, 51.0]      # same starts as compose.html LINES
v = np.zeros(N)
for i, t0 in enumerate(T0): place(v, trimmed(f'vo/clips/FILM_{i:02d}.mp3'), t0)
v = v/np.abs(v).max()*.9
env = np.clip(np.convolve((np.abs(v) > .02).astype(float), np.ones(8820)/8820, mode='same')*3, 0, 1)

music = np.zeros(N)                                           # comic part: stops dead at 26.65
m = load('../../brag-output-2026-09-29-five-minutes/work/music-src.wav'); m = m/np.abs(m).max()
seg = m[: int(26.65*SR)].copy(); seg *= np.minimum(1, np.arange(len(seg))/(SR*.3)); seg[-int(SR*.06):] *= np.linspace(1, 0, int(SR*.06))
place(music, seg, 0, .9)
theme = np.zeros(N)                                           # ending: soft music box, C - G - Am - F
CH = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]
hz = lambda n: 440*2**((n-69)/12)
t0 = 41.2; k = 0
while t0 < DUR - .5:
    ch = CH[k % 4]
    for j, n in enumerate([ch[0], ch[1], ch[2], ch[3], ch[2], ch[1]]): place(theme, bell(hz(n + 12)), t0 + j*.33, .22)
    place(theme, bell(hz(ch[0] - 12), 2.2), t0, .25); t0 += 2.0; k += 1
tt = np.arange(N)/SR
theme *= np.clip((tt - 41.2)/1.5, 0, 1)
room = lowpass(rng.uniform(-1, 1, N), 400)*.06*(tt > 26.65)
sfx = np.zeros(N)
for a in (6.8, 12.2, 16.4, 22.2, 30.0, 50.5): place(sfx, whoosh(), a - .25, .35)
for t_, f in ((.1, 620), (.25, 760), (6.85, 600), (7.0, 700), (7.15, 820), (12.25, 640), (16.45, 600), (16.6, 720), (30.15, 560), (30.35, 660)): place(sfx, pop(f), t_, .3)
for s in (12.6, 13.3, 14.0, 14.7, 15.4, 16.0): place(sfx, shutter(), s, .5)
place(sfx, horn(), 22.55, .45)
for t_ in (20.6, 21.2, 21.8): place(sfx, cricket(), t_, .18)                  # the pause after "no hope for them"
for t_ in np.arange(30.2, 41.0, 1.7): place(sfx, cricket(.35), t_, .05)       # night outside
place(sfx, thunk(), 39.0, .35)                                                # Mum's phone goes face down
place(sfx, load('sfx/success.ogg'), 41.6, .35)                                # Cheeko's own chime
mix = v + music*(1 - .55*env)*.36 + theme*(1 - .45*env)*.9 + sfx*.8 + room
fade = np.minimum(1, tt/.05)*np.clip((DUR - tt)/1.2, 0, 1)
mix = np.tanh(mix*fade*1.1)*.9
def write(path, x):
    st = np.stack([x, np.roll(x, 10)*.98], axis=1)
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
write('music-final.wav', mix)
bed = (music*.36 + theme*.9 + sfx*.8 + room)*fade; write('music-only.wav', np.tanh(bed/(np.abs(bed).max() + 1e-9)*1.2)*.9)
print('ok', DUR)
