"""Original music + sound effects for one Learning Center video, from <slug>/cues_L<n>.json and <slug>/vo_L<n>.wav.
22 styles (one per idea, named in themes.json) built from the same small instrument kit: plucked strings (Karplus-Strong), marimba,
glockenspiel, piano, steel drum, flute, pads, square leads, basses and drums, including tabla-like drums and a tanpura drone.
The music ducks under Cheeko's voice and dips while the child is guessing. Usage: python3 synth.py <idea number> <level>
Writes <slug>/music-final_L<n>.wav (48 kHz stereo). Sound-quiz sounds come from sounds/<key>.mp3 when present."""
import json, os, subprocess, sys, wave, numpy as np
from scipy.signal import lfilter
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000
IDEA = json.load(open('ideas.json'))['ideas'][int(sys.argv[1]) - 1]; LV = int(sys.argv[2]); SLUG = IDEA['slug']
C = json.load(open(f'{SLUG}/cues_L{LV}.json')); DUR = C['dur']; N = int(SR * DUR); rng = np.random.default_rng(IDEA['n'] * 10 + LV)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def ts(d): return np.arange(int(SR * d)) / SR
def place(buf, sig, t0, g=1.0):
    i = int(t0 * SR); j = min(len(buf), i + len(sig))
    if 0 <= i < len(buf): buf[i:j] += sig[:j - i] * g
def env(d, a=.003, r=8.0): t = ts(d); return np.minimum(1, t / a) * np.exp(-t * r)
def lp(x, fc): a = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - a], [1, -a], x)
def noise(d): return rng.uniform(-1, 1, int(SR * d))

# ---------- instruments ----------
def pluck(f, d=.6, bright=.6, decay=.996):
    Nn = max(2, int(SR / f)); x = np.zeros(int(SR * d)); burst = rng.uniform(-1, 1, Nn); burst = lp(burst, 2000 + 6000 * bright); x[:Nn] = burst
    a = np.zeros(Nn + 2); a[0] = 1; a[Nn] = -decay / 2; a[Nn + 1] = -decay / 2
    return lfilter([1], a, x) * np.minimum(1, np.maximum(0, d - ts(d)) / .05)
def marimba(f, d=.35): t = ts(d); return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*4*f*t)*np.exp(-t*40)) * env(d, .002, 11)
def glock(f, d=1.0): t = ts(d); return (np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*2.76*f*t)*np.exp(-t*8)) * env(d, .001, 4)
def xylo(f, d=.3): t = ts(d); return (np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*3.9*f*t)*np.exp(-t*30)) * env(d, .001, 16)
def piano(f, d=.9):
    t = ts(d); x = sum((1 / h ** 1.4) * np.sin(2 * np.pi * f * h * (1 + .0004 * h * h) * t) * np.exp(-t * (2.5 + h * 1.2)) for h in range(1, 7))
    return x * np.minimum(1, t / .003)
def steel(f, d=.6): t = ts(d); mod = 1.6 * np.exp(-t * 6) * np.sin(2 * np.pi * f * 2.4 * t); return np.sin(2 * np.pi * f * t + mod) * env(d, .002, 5)
def flute(f, d=.5):
    t = ts(d); vib = 1 + .006 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / .15)
    x = np.sin(2 * np.pi * f * np.cumsum(vib) / SR) + .12 * np.sin(4 * np.pi * f * np.cumsum(vib) / SR) + .05 * lp(noise(d), 3000)
    return x * np.minimum(1, t / .05) * np.minimum(1, np.maximum(0, d - t) / .08)
def square(f, d=.25, duty=.5):
    t = ts(d); x = sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 12, 2)) if duty == .5 else sum(np.sin(2*np.pi*f*h*t)*np.sin(np.pi*h*duty)/h for h in range(1, 12))
    return x * .7 * env(d, .002, 6)
def pad(notes, d, bright=.12):
    t = ts(d); x = np.zeros_like(t)
    for m in notes:
        for dt in (-.08, .08): f = hz(m) * 2 ** (dt / 12); x += np.sin(2 * np.pi * f * t) + bright * np.sin(2 * np.pi * 2 * f * t)
    return x * np.minimum(1, t / .4) * np.minimum(1, np.maximum(0, d - t) / .4) / len(notes)
def bass(f, d=.25, kind='pluck'):
    t = ts(d)
    if kind == 'tuba': return lp(square(f, d), 600) * 1.6 * np.minimum(1, t / .01) * np.exp(-t * 3)
    if kind == 'slap': return (pluck(f, d, .9, .993) * 1.4 + .3 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 40))
    if kind == 'sub': return np.sin(2 * np.pi * f * t) * env(d, .005, 3.5)
    return (np.sin(2 * np.pi * f * t) + .55 * np.sin(2 * np.pi * 2 * f * t) + .3 * np.sin(2 * np.pi * 3 * f * t)) * env(d, .003, 9)
def kick(): t = ts(.3); f = 48 + 90 * np.exp(-t * 35); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def snare(): t = ts(.2); return (lp(noise(.2), 6000) * .8 + .4 * np.sin(2 * np.pi * 190 * t)) * np.exp(-t * 18)
def clap():
    t = ts(.18); x = noise(.18); x = x - lp(x, 900)
    return x * (np.exp(-t * 30) + .6 * np.exp(-np.maximum(t - .012, 0) * 30) * (t > .012)) * .6
HAT = (lambda x: (x - lp(x, 7000)) * np.exp(-ts(.05) * 70))(noise(.05))
SHAKE = (lambda x: (x - lp(x, 5000)) * np.exp(-ts(.07) * 45))(noise(.07))
def tom(f=110): t = ts(.35); ff = f * (1 + .5 * np.exp(-t * 20)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 7)
def block(f=1100): t = ts(.12); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.4 * f * t) * np.exp(-t * 80)) * np.exp(-t * 38)
def tabla_dha(): t = ts(.45); f = 90 * (1 + .6 * np.exp(-t * 12)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) + .4 * np.sin(2 * np.pi * 520 * t) * np.exp(-t * 9)
def tabla_na(): t = ts(.3); return (np.sin(2 * np.pi * 620 * t) + .4 * np.sin(2 * np.pi * 1340 * t)) * np.exp(-t * 11)
def pop(f): t = ts(.16); ff = f * (1 + 1.1 * np.exp(-t * 45)); return np.sin(2 * np.pi * np.cumsum(ff) / SR) * np.exp(-t * 24)
def whoosh(d=.45):
    t = ts(d); x = noise(d); y = (lp(x, 2600) - lp(x, 700)) * np.sin(np.pi * t / d) ** 2
    return y * .8

# ---------- styles ----------
MAJ, MIN, PENT, MINP = [0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10], [0, 2, 4, 7, 9], [0, 3, 5, 7, 10]
S = {  # bpm, key, scale, meter, progression (scale degrees), lead, chord instr, bass kind, drums, extras
 'farm':      dict(bpm=118, key=62, sc=MAJ, meter=4, prog=[0, 3, 4, 0], lead='pluck', chord='pluck', bass='tuba', drums='boomchick'),
 'calypso':   dict(bpm=112, key=65, sc=MAJ, meter=4, prog=[0, 3, 4, 3], lead='steel', chord='steel', bass='pluck', drums='calypso'),
 'musicbox':  dict(bpm=96,  key=67, sc=MAJ, meter=3, prog=[0, 5, 3, 4], lead='glock', chord='glock', bass='sub', drums='none'),
 'claps':     dict(bpm=120, key=60, sc=MAJ, meter=4, prog=[0, 4, 5, 3], lead='marimba', chord='marimba', bass='pluck', drums='claps'),
 'lullaby':   dict(bpm=84,  key=65, sc=MAJ, meter=3, prog=[0, 3, 0, 4], lead='glock', chord='pad', bass='sub', drums='none'),
 'piano':     dict(bpm=108, key=60, sc=MAJ, meter=4, prog=[0, 5, 3, 4], lead='piano', chord='piano', bass='pluck', drums='light'),
 'xylophone': dict(bpm=116, key=67, sc=PENT, meter=4, prog=[0, 3, 4, 0], lead='xylo', chord='marimba', bass='pluck', drums='light'),
 'mystery':   dict(bpm=100, key=62, sc=MIN, meter=4, prog=[0, 5, 3, 4], lead='pizz', chord='pad', bass='pluck', drums='softtom'),
 'ukulele':   dict(bpm=104, key=64, sc=MAJ, meter=4, prog=[0, 4, 5, 3], lead='glock', chord='uke', bass='pluck', drums='shaker'),
 'synthpop':  dict(bpm=118, key=62, sc=MAJ, meter=4, prog=[5, 3, 0, 4], lead='square', chord='pad', bass='sub', drums='pop'),
 'march':     dict(bpm=112, key=65, sc=MAJ, meter=4, prog=[0, 4, 0, 4], lead='glock', chord='marimba', bass='tuba', drums='march'),
 'soft':      dict(bpm=92,  key=64, sc=MAJ, meter=4, prog=[0, 3, 5, 4], lead='piano', chord='pad', bass='sub', drums='shaker'),
 'flute':     dict(bpm=100, key=67, sc=PENT, meter=4, prog=[0, 3, 4, 0], lead='flute', chord='pluck', bass='pluck', drums='shaker'),
 'funky':     dict(bpm=110, key=64, sc=MINP, meter=4, prog=[0, 3, 0, 4], lead='square', chord='marimba', bass='slap', drums='funk'),
 'indian':    dict(bpm=100, key=62, sc=[0, 2, 4, 5, 7, 9, 10], meter=4, prog=[0, 0, 3, 0], lead='sitar', chord='none', bass='sub', drums='tabla', drone=True),
 'space':     dict(bpm=90,  key=62, sc=MAJ, meter=4, prog=[0, 5, 3, 4], lead='glock', chord='pad', bass='sub', drums='none', arp=True),
 'quirky':    dict(bpm=124, key=60, sc=MAJ, meter=4, prog=[0, 3, 4, 0], lead='square25', chord='pizz', bass='tuba', drums='woodblock'),
 'mystery2':  dict(bpm=96,  key=69, sc=MIN, meter=4, prog=[0, 3, 4, 0], lead='glock', chord='pizz', bass='pluck', drums='softtom'),
 'jungle':    dict(bpm=114, key=62, sc=PENT, meter=4, prog=[0, 3, 4, 3], lead='marimba', chord='marimba', bass='sub', drums='jungle'),
 'travel':    dict(bpm=106, key=64, sc=[0, 2, 4, 5, 7, 9, 10], meter=4, prog=[0, 3, 4, 0], lead='sitar', chord='pluck', bass='pluck', drums='tabla'),
 'ticktock':  dict(bpm=108, key=65, sc=MAJ, meter=4, prog=[0, 4, 5, 3], lead='xylo', chord='glock', bass='pluck', drums='woodblock'),
 'happysynth':dict(bpm=122, key=64, sc=MAJ, meter=4, prog=[0, 4, 5, 3], lead='square', chord='marimba', bass='pluck', drums='pop'),
}
ST = S[C['music']]; BEAT = 60 / ST['bpm']; BAR = ST['meter'] * BEAT; SC = ST['sc']
def deg(d, octv=0):   # scale degree -> midi note
    d0 = d % len(SC); return ST['key'] + SC[d0] + 12 * (d // len(SC) + octv)
def triad(d): return [deg(d), deg(d + 2), deg(d + 4)]
def lead_note(m, d):
    f = hz(m); L = ST['lead']
    return {'pluck': lambda: pluck(f, d + .3, .7), 'steel': lambda: steel(f, d + .3), 'glock': lambda: glock(f, d + .6), 'marimba': lambda: marimba(f, d + .2),
            'piano': lambda: piano(f, d + .4), 'xylo': lambda: xylo(f, d + .15), 'pizz': lambda: pluck(f, .3, .4, .99), 'square': lambda: square(f, d + .05),
            'square25': lambda: square(f, d + .05, .25), 'flute': lambda: flute(f, d), 'sitar': lambda: pluck(f, d + .6, .95, .998) + .2 * pluck(f * 2.01, d + .6, .9, .997)}[L]()
LEAD_G = {'pluck': .16, 'steel': .14, 'glock': .09, 'marimba': .16, 'piano': .14, 'xylo': .15, 'pizz': .2, 'square': .055, 'square25': .05, 'flute': .12, 'sitar': .16}[ST['lead']]
mus, drm, sfx = np.zeros(N), np.zeros(N), np.zeros(N)
end = C['outro'] + 7.0
phrase = []   # a 4-bar melody, reused A A B A so it sounds composed
for section in range(2):
    mel = []
    for bar in range(4):
        steps = ST['meter'] * 2; cd = ST['prog'][bar]
        for s in range(steps):
            if rng.random() < (.55 if s % 2 == 0 else .22): mel.append((bar, s, cd + rng.choice([0, 2, 4, 7, 4, 2])))
    phrase.append(mel)
b, t0 = 0, 0.0
while t0 < end:
    ch = ST['prog'][b % 4]; notes = triad(ch)
    # bass
    for i in range(ST['meter']):
        tt = t0 + i * BEAT
        if tt >= end: break
        if ST['bass'] == 'tuba' and i % 2: continue
        place(mus, bass(hz(deg(ch, -2) + (7 if (ST['meter'] == 4 and i == 2 and ST['bass'] != 'sub') else 0)), BEAT * (1.8 if ST['bass'] == 'sub' else .9), ST['bass']), tt, .55 if ST['bass'] != 'sub' else .45)
    # chords
    chd = ST['chord']
    if chd == 'pad' and b % 2 == 0: place(mus, pad([n - 12 for n in notes], BAR * 2), t0, .28)
    elif chd in ('marimba', 'glock', 'steel', 'pluck', 'pizz', 'piano', 'uke'):
        for i in range(ST['meter']):
            tt = t0 + i * BEAT + (BEAT / 2 if chd in ('marimba', 'steel', 'pluck') and ST['meter'] == 4 else 0)
            if tt >= end or (ST['meter'] == 3 and i == 0): continue
            for j, m in enumerate(notes):
                if chd == 'uke': place(mus, pluck(hz(m), .5, .5), tt + j * .012, .09)
                elif chd == 'piano': place(mus, piano(hz(m), .5), tt, .06)
                elif chd == 'pizz': place(mus, pluck(hz(m), .25, .35, .99), tt, .08)
                elif chd == 'pluck': place(mus, pluck(hz(m + 12), .4, .5), tt, .07)
                elif chd == 'steel': place(mus, steel(hz(m + 12), .35), tt, .05)
                else: place(mus, (marimba if chd == 'marimba' else glock)(hz(m + 12), .35 if chd == 'marimba' else .6), tt, .07)
    if ST.get('drone') and b % 2 == 0:
        for k, m in enumerate([deg(0, -1), deg(4, -1), deg(0), deg(0)]): place(mus, pluck(hz(m), 2.2, .3, .9995), t0 + k * BAR / 2, .07)
    if ST.get('arp'):
        for k in range(ST['meter'] * 2): place(mus, glock(hz(notes[k % 3] + 12), .5), t0 + k * BEAT / 2, .04)
    # melody: A A B A, silent every 8th bar so it breathes
    mel = phrase[1 if (b // 4) % 4 == 2 else 0]
    if b % 8 != 7:
        for bar, s, d in mel:
            if bar == b % 4:
                tt = t0 + s * BEAT / 2
                if tt < end: place(mus, lead_note(deg(d, 1), BEAT * .5), tt, LEAD_G)
    # drums
    dk = ST['drums']
    for i in range(ST['meter'] * 2):
        tt = t0 + i * BEAT / 2; on = i % 2 == 0; beat = i // 2
        if tt >= end or dk == 'none': continue
        if dk == 'boomchick': place(drm, kick() if (on and beat % 2 == 0) else (snare() * .5 if on else HAT * .5), tt, .5)
        elif dk == 'calypso': place(drm, SHAKE, tt, .14); place(drm, kick(), tt, .45) if i in (0, 3, 4) else None; place(drm, tom(220), tt, .2) if i == 6 else None
        elif dk == 'claps': place(drm, kick(), tt, .55) if on else None; place(drm, clap(), tt, .45) if beat % 2 and on else None; place(drm, HAT, tt + BEAT / 4, .12)
        elif dk == 'light': place(drm, HAT, tt, .1 if on else .05); place(drm, kick(), tt, .35) if i == 0 else None
        elif dk == 'softtom': place(drm, tom(90), tt, .25) if i in (0, 5) else None; place(drm, HAT, tt, .05)
        elif dk == 'shaker': place(drm, SHAKE, tt, .12 if on else .07); place(drm, kick(), tt, .3) if i == 0 else None
        elif dk == 'pop': place(drm, kick(), tt, .55) if on else None; place(drm, snare(), tt, .4) if beat % 2 and on else None; place(drm, HAT, tt, .1)
        elif dk == 'march': place(drm, kick(), tt, .45) if beat % 2 == 0 and on else None; place(drm, snare(), tt, .3 if on else .15)
        elif dk == 'funk': place(drm, kick(), tt, .55) if i in (0, 3, 5) else None; place(drm, clap(), tt, .4) if i in (2, 6) else None; place(drm, HAT, tt, .1)
        elif dk == 'tabla': place(drm, tabla_dha(), tt, .4) if i in (0, 3) else None; place(drm, tabla_na(), tt, .25) if i in (2, 5, 6, 7) else None
        elif dk == 'woodblock': place(drm, block(1300 if on else 900), tt, .22); place(drm, kick(), tt, .35) if i == 0 else None
        elif dk == 'jungle': place(drm, tom(140 if i % 3 else 95), tt, .35) if i in (0, 2, 3, 5, 6) else None; place(drm, SHAKE, tt, .1)
    b += 1; t0 += BAR
for m in [triad(0)[0] + 12, triad(0)[1] + 12, triad(0)[2] + 12, triad(0)[0] + 24]: place(mus, glock(hz(m), 2.5), end, .1)
place(mus, bass(hz(deg(0, -2)), 1.4), end, .5)

# ---------- sound effects ----------
bell = {'farm': glock, 'calypso': steel, 'indian': lambda f, d: pluck(f, d, .9)}.get(C['music'], glock)
for k, t in enumerate(C['ticks']): place(sfx, block(1100 + 90 * (k % C['answer'])), t, .5)
for t in C['reveals']:
    for k, m in enumerate((86, 90, 93, 98)): place(sfx, bell(hz(m - 12 + ST['key'] - 62), 1.0), t + k * .055, .16)
    place(sfx, pop(hz(88)), t, .22)
for t in C['whooshes']: place(sfx, whoosh(), t - .05, .45)
for t in C['introPops'] + C['outroPops']: place(sfx, pop(hz(86)), t, .2)
for k, t in enumerate(C.get('pops', [])): place(sfx, pop(hz(80 + (k % 10))), t, .3)
for t in C.get('covers', []): place(sfx, whoosh(.3), t, .5); place(sfx, pop(hz(70)), t + .2, .3)
def load(f):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; return x / (np.abs(x).max() + 1e-9)
real = np.zeros(N)
for t, key in C.get('sounds', []):
    f = f'sounds/{key}.mp3'
    if os.path.exists(f): place(real, load(f), t, .8)

def reverb(x, secs=1.0, mix=.15):
    n = int(SR * secs); t = np.arange(n) / SR; ir = rng.normal(0, 1, n) * np.exp(-t * 5); ir = lp(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    L = len(x) + n; F = 1 << (L - 1).bit_length(); wet = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)]
    return x * (1 - mix) + wet * mix * 3
music = reverb(mus, mix=.14) + drm * .85; music = music / (np.abs(music).max() + 1e-9) * .9
fx = reverb(sfx, mix=.12); fx = fx / (np.abs(fx).max() + 1e-9) * .9
with wave.open(f'{SLUG}/vo_L{LV}.wav') as w: vo = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
v = np.zeros(N); v[:min(N, len(vo))] = vo[:N]; v = v / np.abs(v).max() * .92
envv = (np.abs(v) > .02).astype(float); k = int(SR * .2); envv = np.convolve(envv, np.ones(k) / k, 'same'); envv = np.clip(envv * 3, 0, 1)
envv = np.convolve(envv, np.ones(int(SR * .1)) / int(SR * .1), 'same')
t = np.arange(N) / SR; cd = np.zeros(N)
for a, b2 in zip(C['roundTick0'], C['roundReveal']): cd += np.clip(np.minimum((t - a + .15) / .15, (b2 + .05 - t) / .15), 0, 1)
rlv = (np.abs(real) > .01).astype(float); rlv = np.convolve(rlv, np.ones(int(SR * .2)) / int(SR * .2), 'same')
fade = np.minimum(1, t / .02) * np.clip((DUR - t) / 1.2, 0, 1) ** 1.3
bed = music * (1 - .65 * envv) * (1 - .45 * cd) * (1 - .7 * np.clip(rlv * 2, 0, 1)) * .30
mix = (bed + fx * .55 + v + real * .9) * fade; mix = np.tanh(mix / np.abs(mix).max() * 1.25) * .9
with wave.open(f'{SLUG}/music-final_L{LV}.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
print(f'{SLUG} L{LV}: music {C["music"]}, {DUR:.1f}s')
