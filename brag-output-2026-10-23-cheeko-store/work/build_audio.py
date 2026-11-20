"""V55 audio: places every voice clip (vo/V55_*.wav) and the Guess the Dinosaur quiz's own sound at their film times
(vo/vo-tight.wav, 44.1 kHz mono), writes cues.json, then runs the feature template's synth.py (music + sound effects,
ducked under the voice) and copies the mix to film/assets/audio/mix.wav. Line starts here are the film's clock: the
compositions in film/ use the same numbers (SPEC.md)."""
import json, shutil, subprocess, wave
from pathlib import Path
import numpy as np

SR, DUR = 44100, 45.5
HERE = Path(__file__).parent
QUIZ = HERE.parent.parent / 'learning-center/19-guess-the-dinosaur/device/Cheeko_V50.1_Guess_the_Dinosaur_Level_1_296x240.mp4'
SYNTH = Path('/Users/ravikumar/Cheeko Master/marketing/tools/feature/synth.py')
START = {0: 0.15, 1: 3.15, 2: 5.00, 3: 6.95, 4: 10.05, 5: 13.35, 6: 15.85, 7: 18.65, 8: 22.65, 9: 24.85, 10: 31.25, 11: 37.75, 12: 41.85}
FILE = {8: 'V55_08_English_Strong-WilledBoy'}   # the boy's "T-Rex!" (Strong-Willed Boy sounds like a small boy)
QUIZ_CUTS = [(9.79, 1.90, 21.05), (15.20, 1.65, 22.95)]   # (source start, length, film start): round 1 question, then the reveal


def load(path, ss=None, t=None):
    cmd = ['ffmpeg', '-loglevel', 'error'] + (['-ss', str(ss), '-t', str(t)] if ss is not None else []) + ['-i', str(path), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-']
    return np.frombuffer(subprocess.check_output(cmd), np.int16).astype(float) / 32768


vo = np.zeros(int(SR * DUR))
def place(x, t0, g=1.0):
    i = int(t0 * SR); vo[i:i + len(x)] += x[:len(vo) - i] * g

ends = {}
for i, t0 in START.items():
    x = load(HERE / 'vo' / (FILE.get(i, f'V55_{i:02d}') + '.wav')); place(x, t0); ends[i] = round(t0 + len(x) / SR, 3)
for ss, n, t0 in QUIZ_CUTS:
    x = load(QUIZ, ss, n); k = int(SR * .03); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k)
    place(x / (np.abs(x).max() + 1e-9) * .8, t0)
with wave.open(str(HERE / 'vo/vo-tight.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(vo, -1, 1) * 32767).astype(np.int16).tobytes())

cues = {'dur': DUR, 'mood': 'bright', 'outro': 42.3, 'lastLine': 41.85, 'calm': [[21.0, 24.6]],
        'shots': [[0, 'hook'], [4.75, 'store'], [12.85, 'drop'], [13.05, 'cheeko'], [15.85, 'pullback'], [20.7, 'zoom'], [24.6, 'more'], [37.55, 'end']],
        'stamps': [0.35, 1.05, 1.75, 2.21], 'bubbles': [13.35, 18.65, 22.65], 'cards': [13.5], 'flashes': [18.65], 'presses': [],
        'pops': [3.2, 6.95, 10.55, 11.35, 26.45, 29.05, 31.2, 32.1, 34.25, 35.75, 37.75, 41.85], 'letters': [], 'screens': []}
json.dump(cues, open(HERE / 'cues.json', 'w'), indent=1)
json.dump({'start': START, 'end': ends}, open(HERE / 'timing.json', 'w'), indent=1)
subprocess.run(['/Users/ravikumar/Cheeko Master/cheeko-v2-website/.venv/bin/python', str(SYNTH)], cwd=HERE, check=True)
out = HERE.parent / 'film/assets/audio/mix.wav'; out.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(HERE / 'music-final.wav', out)
print('line ends:', ends)
