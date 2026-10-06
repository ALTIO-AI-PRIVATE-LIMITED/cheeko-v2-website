"""Scene 1 test audio: the two voice lines at the times compose.html lip-syncs them, soft playground ambience,
light whooshes for the motion-graphic build. Writes music-final.wav. Usage: ../../.venv/bin/python scene1_audio.py"""
import subprocess, wave, numpy as np
SR, DUR = 44100, 9.4
N = int(SR * DUR); rng = np.random.default_rng(3)
def load_trimmed(mp3):  # same trim as the lip-sync envelope
    x = np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',mp3,'-ac','1','-ar',str(SR),'-f','s16le','-']), dtype=np.int16).astype(float) / 32768
    env = np.convolve(np.abs(x), np.ones(441)/441, mode='same'); on = np.nonzero(env > 0.006)[0]
    return x[max(0, on[0]-int(.03*SR)): min(len(x), on[-1]+int(.06*SR))]
def place(buf, sig, t, g=1.0):
    i = int(t*SR); j = min(len(buf), i+len(sig)); buf[i:j] += sig[:j-i]*g
def lowpass(x, c):
    a = np.exp(-2*np.pi*c/SR); y = np.empty_like(x); s = 0.
    for k in range(len(x)): s = (1-a)*x[k] + a*s; y[k] = s
    return y
def ts(d): return np.arange(int(SR*d))/SR
def chirp(f0, f1, d=.09):
    t = ts(d); f = np.linspace(f0, f1, len(t)); return np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi*t/d)**2
def whoosh(d=.35):
    t = ts(d); x = rng.uniform(-1, 1, len(t)); x = lowpass(x, 2600) - lowpass(x, 400); return x*np.sin(np.pi*t/d)**2
voice = np.zeros(N); place(voice, load_trimmed('vo/clips/FILM_00.mp3'), 2.25); place(voice, load_trimmed('vo/clips/FILM_01.mp3'), 3.45)
voice = voice / np.abs(voice).max() * .9
amb = lowpass(rng.uniform(-1, 1, N), 700) * .05                       # soft air
for t0 in (.8, 1.1, 3.0, 5.6, 5.8, 7.9, 8.3):                         # birds
    for k in range(2): place(amb, chirp(2600 + 400*rng.random(), 3600 + 500*rng.random()), t0 + k*.13, .05)
for t0, g in ((0.05, .1), (.45, .08), (.55, .1)): place(amb, whoosh(), t0, g)
t = np.arange(N)/SR; fade = np.minimum(1, t/.3) * np.clip((DUR - t)/.6, 0, 1)
mix = np.tanh((voice + amb) * fade * 1.1) * .9
st = np.stack([mix, np.roll(mix, 10)*.98], axis=1)
with wave.open('music-final.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok', DUR)
