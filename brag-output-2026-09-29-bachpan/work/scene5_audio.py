"""Scene 5 test audio: placeholder party music (V09's licensed track) that stops dead when Rohan's smile fades,
quiet room tone for the uncomfortable beat, the two voice lines where compose.html animates them, party horn and pops.
Writes music-final.wav. Usage: ../../.venv/bin/python scene5_audio.py"""
import subprocess, wave, numpy as np
SR, DUR = 44100, 7.8
N = int(SR*DUR); rng = np.random.default_rng(5)
def load(p): return np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',p,'-ac','1','-ar',str(SR),'-f','s16le','-']), dtype=np.int16).astype(float)/32768
def trimmed(p):
    x = load(p); env = np.convolve(np.abs(x), np.ones(441)/441, mode='same'); on = np.nonzero(env > 0.006)[0]
    return x[max(0, on[0]-int(.03*SR)): min(len(x), on[-1]+int(.06*SR))]
def place(b, s, t, g=1.): i = int(t*SR); j = min(len(b), i+len(s)); b[i:j] += s[:j-i]*g
def ts(d): return np.arange(int(SR*d))/SR
def pop(f=700): t = ts(.16); ff = f*(1 + 1.3*np.exp(-t*45)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*24)
def horn(d=.55):
    t = ts(d); f = 520 + 60*np.sin(2*np.pi*7*t); ph = 2*np.pi*np.cumsum(f)/SR
    return sum(np.sin(k*ph)/k for k in range(1, 8)) * np.minimum(1, t/.03) * np.minimum(1, (d-t)/.08) * .5
v = np.zeros(N); place(v, trimmed('vo/clips/FILM_06.mp3'), 1.8); place(v, trimmed('vo/clips/FILM_07.mp3'), 4.7); v = v/np.abs(v).max()*.9
env = np.clip(np.convolve((np.abs(v) > .02).astype(float), np.ones(8820)/8820, mode='same')*3, 0, 1)
music = np.zeros(N)
m = load('../../brag-output-2026-09-29-tiny-adults/work/music-src.wav'); m = m/np.abs(m).max()
seg = m[int(16.84*SR): int(16.84*SR) + int(4.3*SR)]; seg = seg*np.minimum(1, np.arange(len(seg))/(SR*.05)); seg[-400:] *= np.linspace(1, 0, 400)
place(music, seg, 0)
room = np.convolve(rng.uniform(-1, 1, N), np.ones(60)/60, mode='same')*.05*(np.arange(N)/SR > 4.3)
sfx = np.zeros(N); place(sfx, horn(), .35, .5)
for t0, f in ((.15, 620), (.3, 760), (.35, 880), (.5, 700), (1.15, 600)): place(sfx, pop(f), t0, .35)
mix = v + music*(1 - .55*env)*.42 + sfx*.8 + room
t = np.arange(N)/SR; mix *= np.minimum(1, t/.05)*np.clip((DUR - t)/.5, 0, 1)
mix = np.tanh(mix*1.1)*.9; st = np.stack([mix, np.roll(mix, 10)*.98], axis=1)
with wave.open('music-final.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('ok', DUR)
