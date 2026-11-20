"""Original Cheeko lullabies, made entirely in code (no samples, no licences). Three 1-minute samples:
  A  music box: music box melody over a soft harp arpeggio and a warm pad, 3/4 at 72 bpm, slowing at the end
  B  bansuri: bansuri melody in a Bhupali-like pentatonic over a tanpura drone, swarmandal shimmer, no drums
  C  goodnight: harp and music box with Cheeko's calm goodnight lines in the gaps (vo/LUL_00..04.mp3)
Usage: /usr/bin/python3 lullaby.py [A|B|C ...]   ->  samples/<name>.mp3 (stereo, -20 LUFS) and .wav"""
import os, subprocess, sys
import numpy as np
from scipy.signal import lfilter, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); os.makedirs('samples', exist_ok=True)
SR = 48000; rng = np.random.default_rng(7)
ts = lambda d: np.arange(int(SR * d)) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def lp(x, fc): a = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - a], [1, -a], x)
def hp(x, fc): return x - lp(x, fc)

# ---------- instruments ----------
def musicbox(f, d=2.4, v=1.0):    # a plucked steel tine: cantilever modes 1 : 6.27 : 17.6, the high ones die fast
    t = ts(d); x = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.5)
    for r, a, k in ((6.27, .22, 9), (17.55, .06, 25)):
        if f * r < SR / 2.2: x += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k)
    x += .03 * rng.standard_normal(len(t)) * np.exp(-t * 300)            # the tiny click of the pin
    return v * x * np.minimum(1, t / .002)
def harp(f, d=3.0, v=1.0, bright=.35, decay=.9985):    # Karplus-Strong string, dark and long
    n = max(2, int(SR / f)); x = np.zeros(int(SR * d)); x[:n] = lp(rng.uniform(-1, 1, n), 1500 + 5000 * bright)
    a = np.zeros(n + 2); a[0] = 1; a[n] = a[n + 1] = -decay / 2
    y = lfilter([1], a, x); return v * y / (np.abs(y).max() + 1e-9)
def pad(notes, d, v=1.0):
    t = ts(d); x = np.zeros_like(t)
    for m in notes:
        for det in (-.07, .07): x += np.sin(2 * np.pi * hz(m) * 2 ** (det / 12) * t)
    x = lp(x, 900); return v * x / (2 * len(notes)) * np.minimum(1, t / 1.2) * np.minimum(1, np.maximum(0, d - t) / 1.2)
def soft_bass(m, d, v=1.0): t = ts(d); return v * np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / .08) * np.exp(-t * .9)
def bansuri(m, d, prev=None, v=1.0):    # breathy flute with a slow vibrato and a meend (glide) from the previous note
    t = ts(d); f0 = hz(m); f = np.full_like(t, f0)
    if prev is not None:
        g = min(.18, d * .3); k = np.clip(t / g, 0, 1); f = hz(prev) + (f0 - hz(prev)) * (1 - (1 - k) ** 2)
    vib = 1 + .007 * np.sin(2 * np.pi * 5 * t) * np.clip((t - .35) / .4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    tone = np.sin(ph) + .18 * np.sin(2 * ph) + .06 * np.sin(3 * ph)
    breath = hp(lp(rng.standard_normal(len(t)), 3500), 900) * .05
    e = np.minimum(1, t / .12) * np.minimum(1, np.maximum(0, d - t) / .18)
    return v * (tone + breath) * e
def tanpura_string(m, d=5.0, v=1.0):    # bright sustained string; the slow wobble stands in for the jawari buzz
    t = ts(d); y = harp(hz(m), d, 1, bright=.95, decay=.9996)
    return v * y * (1 + .25 * np.sin(2 * np.pi * .6 * t)) * np.minimum(1, np.maximum(0, d - t) / .5)

# ---------- mixing helpers ----------
class Track:
    def __init__(s, secs): s.L = np.zeros(int(SR * secs)); s.R = np.zeros(int(SR * secs))
    def add(s, x, t, pan=0.0, g=1.0):
        a = int(t * SR); x = x[:max(0, len(s.L) - a)]
        s.L[a:a + len(x)] += x * g * np.sqrt((1 - pan) / 2); s.R[a:a + len(x)] += x * g * np.sqrt((1 + pan) / 2)
def reverb(L, R, rt=2.4, wet=.32):
    n = int(SR * rt); t = np.arange(n) / SR; env = np.exp(-t * 6.91 / rt)
    irs = [lp(rng.standard_normal(n), 4200) * env for _ in range(2)]
    for ir in irs: ir[:int(SR * .018)] = 0; ir /= np.sqrt((ir ** 2).sum())
    wl = fftconvolve(L, irs[0])[:len(L)]; wr = fftconvolve(R, irs[1])[:len(R)]
    return L * (1 - wet) + wl * wet * 2.2, R * (1 - wet) + wr * wet * 2.2
def master(tr, name, fade=6.0):
    L, R = reverb(tr.L, tr.R)
    n = int(SR * fade); w = np.linspace(1, 0, n) ** 2; L[-n:] *= w; R[-n:] *= w
    st = np.stack([L, R], 1); st /= np.abs(st).max() / .9
    wav = f'samples/{name}.wav'; import wave
    with wave.open(wav, 'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'loudnorm=I=-20:TP=-2:LRA=9', '-ar', '48000', '-b:a', '192k', f'samples/{name}.mp3'], check=True)
    print(f'samples/{name}.mp3', f'{len(L) / SR:.1f}s')

# ---------- the tune (original): four 4-bar phrases in 3/4, scale steps from the tonic ----------
CH = {'I': [0, 4, 7], 'IV': [5, 9, 12], 'V': [7, 11, 14], 'vi': [9, 12, 16]}
TUNE = [('I', [(4, 2), (7, 1)]), ('IV', [(9, 2), (7, 1)]), ('IV', [(5, 2), (4, 1)]), ('V', [(2, 3)]),
        ('I', [(4, 2), (7, 1)]), ('IV', [(9, 2), (12, 1)]), ('V', [(11, 1), (9, 1), (7, 1)]), ('I', [(7, 3)]),
        ('vi', [(9, 2), (7, 1)]), ('IV', [(5, 2), (4, 1)]), ('V', [(2, 1), (4, 1), (5, 1)]), ('I', [(4, 3)]),
        ('I', [(4, 2), (2, 1)]), ('IV', [(0, 2), (2, 1)]), ('V', [(4, 1), (2, 1), (-1, 1)]), ('I', [(0, 3)])]
def accompany(tr, chord, t0, beat, key, harp_g=.16, bass_g=.22, pad_g=.10):
    c = [key - 12 + n for n in CH[chord]]; root = c[0]
    tr.add(soft_bass(root - 12, beat * 3 + .5), t0, 0, bass_g)
    pat = [c[0], c[2], c[1] + 12, c[2] + 12, c[1] + 12, c[2]]          # a rocking broken chord in eighths
    for i, m in enumerate(pat): tr.add(harp(hz(m), 2.6), t0 + i * beat / 2, -.35 + .14 * i, harp_g * (1 if i % 2 == 0 else .7))
    tr.add(pad([key - 12 + n for n in CH[chord]], beat * 3 + 1.2), t0, 0, pad_g)

def track_A():    # music box, 72 bpm, slows at the end
    key = 79; beat0 = 60 / 72; bars = 2 + len(TUNE) + 1
    tr = Track(bars * beat0 * 3 * 1.2 + 8); t = 0.4
    for b in range(2): accompany(tr, 'I', t, beat0, key); t += beat0 * 3      # intro: just the cradle rocking
    for i, (ch, notes) in enumerate(TUNE):
        beat = beat0 * (1 + max(0, i - 11) * .06)                               # ritardando over the last phrase
        accompany(tr, ch, t, beat, key, harp_g=.11, bass_g=.16, pad_g=.08); tt = t
        for m, b in notes: tr.add(musicbox(hz(key + m), b * beat + 1.6), tt, .15, .6); tt += b * beat
        t += beat * 3
    accompany(tr, 'I', t, beat0 * 1.5, key, harp_g=.12)
    tr.add(musicbox(hz(key + 12), 4), t + .2, .2, .35); tr.add(musicbox(hz(key + 7), 4), t + .8, -.2, .3)
    tr.L, tr.R = tr.L[:int(SR * (t + 7))], tr.R[:int(SR * (t + 7))]
    master(tr, 'lullaby_A_music_box')

PENTA = {'S': 0, 'R': 2, 'G': 4, 'P': 7, 'D': 9, "S'": 12, "R'": 14}
BANS = [[('G', 1), ('R', .5), ('S', .5), ('R', 2), ('G', 1), ('P', 1), ('G', 2)],
        [('P', 1), ('D', 1), ("S'", 2), ('D', 1), ('P', .5), ('G', .5), ('P', 2)],
        [('G', 1), ('P', 1), ('D', 1), ('P', 1), ('G', 1), ('R', 1), ('S', 2)],
        [('R', 1), ('G', 1), ('P', 2), ('G', 1), ('R', 1), ('S', 4)]]
def track_B():    # bansuri over tanpura, about 60 bpm, free and slow
    sa = 62; beat = 1.0; secs = 6 + 32 + 17 + 10
    tr = Track(secs + 6)
    for k, t0 in enumerate(np.arange(0, secs, 4.4)):                     # tanpura cycle: Pa, Sa', Sa', Sa
        for j, (m, pan) in enumerate(((sa - 5, -.4), (sa + 12, -.1), (sa + 12, .1), (sa, .4))):
            tr.add(tanpura_string(m, 5.5), t0 + j * 1.1, pan, .13)
    def gliss(t0, up=True):                                                 # swarmandal shimmer
        notes = [sa + 12 + PENTA[n] for n in ('S', 'R', 'G', 'P', 'D', "S'", "R'")]
        for i, m in enumerate(notes if up else notes[::-1]): tr.add(harp(hz(m), 2.5, bright=.8, decay=.9992), t0 + i * .11, .5 - i * .15, .09)
    gliss(1.0); t = 6.0; prev = None
    phrases = BANS + [BANS[2], BANS[3]]
    for p, ph in enumerate(phrases):
        soft = .75 if p >= 4 else 1.0
        for n, b in ph:
            m = sa + 12 + PENTA[n]; tr.add(bansuri(m, b * beat + .25, prev, .3 * soft), t, .05); prev = m; t += b * beat
        t += .6 if p in (1, 3) else .2                                      # breathe between phrases
    gliss(t + .5, up=False)
    tr.L, tr.R = tr.L[:int(SR * (t + 9))], tr.R[:int(SR * (t + 9))]
    master(tr, 'lullaby_B_bansuri', fade=7)

def vo(i, slow=.93):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f'vo/LUL_{i:02d}.mp3', '-af', f'atempo={slow},lowpass=f=9000',
                                   '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'])
    return np.frombuffer(raw, np.float32).astype(float)
def track_C():    # harp-led tune with Cheeko's goodnight lines in the gaps
    key = 72; beat = 60 / 66; bar = beat * 3
    tr = Track(40 * bar); t = 0.4; voice = []
    def gap(bars, line):
        nonlocal t
        for b in range(bars): accompany(tr, 'I' if b % 2 == 0 else 'IV', t + b * bar, beat, key, harp_g=.12, pad_g=.12)
        voice.append((t + .5, line)); t += bars * bar
    gap(2, 0)
    for p in range(4):
        for ch, notes in TUNE[p * 4:p * 4 + 4]:
            accompany(tr, ch, t, beat, key, harp_g=.13); tt = t
            for m, b in notes:
                tr.add(harp(hz(key + 12 + m), 3.0, bright=.5), tt, .1, .30); tr.add(musicbox(hz(key + 24 + m), 2.2), tt, .25, .12); tt += b * beat
            t += bar
        gap(3 if p == 3 else 2, p + 1)
    tr.L, tr.R = tr.L[:int(SR * (t + 4))], tr.R[:int(SR * (t + 4))]
    music_L, music_R = reverb(tr.L, tr.R)
    v = np.zeros_like(music_L); duck = np.ones_like(music_L)
    for t0, i in voice:
        x = vo(i); a = int(t0 * SR); v[a:a + len(x)] += x[:len(v) - a]
        d0, d1 = max(0, a - int(SR * .3)), min(len(duck), a + len(x) + int(SR * .4)); duck[d0:d1] = np.minimum(duck[d0:d1], .55)
    duck = lp(duck, 3)
    v = v / np.abs(v).max() * .8; vl, vr = reverb(v * .9, v * .9, rt=1.2, wet=.12)
    tr.L, tr.R = music_L * duck * .55 + vl, music_R * duck * .55 + vr
    tr.L, tr.R = tr.L * 1, tr.R * 1
    # master without a second reverb on the music
    n = int(SR * 4); w = np.linspace(1, 0, n) ** 2; tr.L[-n:] *= w; tr.R[-n:] *= w
    st = np.stack([tr.L, tr.R], 1); st /= np.abs(st).max() / .9; wav = 'samples/lullaby_C_goodnight_cheeko.wav'; import wave
    with wave.open(wav, 'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'loudnorm=I=-20:TP=-2:LRA=9', '-ar', '48000', '-b:a', '192k',
                    'samples/lullaby_C_goodnight_cheeko.mp3'], check=True)
    print('samples/lullaby_C_goodnight_cheeko.mp3', f'{len(tr.L) / SR:.1f}s')

for k in (sys.argv[1:] or ['A', 'B', 'C']): {'A': track_A, 'B': track_B, 'C': track_C}[k]()
