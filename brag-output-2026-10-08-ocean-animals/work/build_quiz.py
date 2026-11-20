"""Timeline + voice track for the on-device quiz (V30). Reads rounds.json and the Cheeko voice clips in vo/clips
(feature_lines.json V30, recorded with feature_rec.py), trims each clip, places every line and writes:
  vo/vo-tight.wav   the voice track (48 kHz mono)
  timeline.json/js  intro beats, round start times, outro beats, for compose.html
  cues.json         ticks, chimes, whooshes and pops for synth.py
Usage: python3 build_quiz.py [rounds, default 10]"""
import json, subprocess, sys, wave, numpy as np
SR = 48000
NR = int(sys.argv[1]) if len(sys.argv) > 1 else 10
R = json.load(open('rounds.json'))
ROUND = 9.0                       # seconds per animal
PROMPT, TICK0, REVEAL, NAME = .4, 1.9, 4.9, 5.15   # times inside a round

def clip(i):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f'vo/clips/V30_{i:02d}.mp3', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    x = np.frombuffer(raw, np.int16).astype(float) / 32768
    e = np.convolve(np.abs(x), np.ones(480) / 480, 'same'); on = np.where(e > 10 ** (-42 / 20))[0]
    a, b = max(0, on[0] - int(SR * .02)), min(len(x), on[-1] + int(SR * .08))
    y = x[a:b]; f = int(SR * .01); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y

lines, clips = [], {}
def say(i, t):
    clips.setdefault(i, clip(i)); lines.append((t, i)); return t + len(clips[i]) / SR

# intro: hi, title, rules, go (line 3 "they get harder" only in the full 80 cut)
beats = {}
t = .45
for key, i, gap in [('hi', 0, .3), ('title', 1, .35), ('rules', 2, .45)] + ([('harder', 3, .3)] if NR > 20 else []) + [('go', 4, .2)]:
    beats[key] = t; t = say(i, t) + gap
beats['go_end'] = t
T0 = t + .35                      # first round starts here

prompts = {1: 5, NR: 102 if NR <= 20 else 14}
rot = 0
rounds = []
for r in R['rounds'][:NR]:
    n = r['n']; s = T0 + (n - 1) * ROUND
    if n not in prompts:
        if NR <= 20 or n % 3 == 1: prompts[n] = 6 + rot % 8; rot += 1
    p = prompts.get(n)
    pe = say(p, s + PROMPT) - s if p is not None else None
    if pe and pe > TICK0 - .05: print(f'warning: round {n} prompt ends at {pe:.2f}s, after the countdown starts')
    ne = say(22 + n - 1, s + NAME) - s
    rounds.append({'n': n, 'label': r['label'], 'start': round(s, 3), 'prompt': p, 'promptEnd': pe and round(pe, 3), 'nameEnd': round(ne, 3),
                   'img': r.get('img') or (r.get('source') or {}).get('preview'), 'crop': r.get('crop', [.5, .5, 1])})
O = T0 + NR * ROUND
outro = {}
t = O + .35
for key, i, gap in [('wow', 18, .3), ('howmany', 19, .35), ('again', 20, .35), ('bye', 21, .3)]:
    outro[key] = t; t = say(i, t) + gap
DUR = round(t + 1.6, 2)

vo = np.zeros(int(SR * DUR) + SR)
for t0, i in lines:
    a = int(t0 * SR); vo[a:a + len(clips[i])] += clips[i]
vo = vo[:int(SR * DUR)]; vo = vo / np.abs(vo).max() * .9
with wave.open('vo/vo-tight.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())

TL = {'dur': DUR, 'round': ROUND, 'n': NR, 'intro': beats, 'rounds': rounds, 'outroStart': round(O, 3), 'outro': outro,
      'times': {'prompt': PROMPT, 'tick0': TICK0, 'reveal': REVEAL, 'name': NAME}}
json.dump(TL, open('timeline.json', 'w'), indent=1, ensure_ascii=False)
open('timeline.js', 'w').write('window.TL = ' + json.dumps(TL, ensure_ascii=False) + ';\n')
cues = {'dur': DUR, 'roundStarts': [r['start'] for r in rounds], 'outro': O,
        'ticks': [r['start'] + TICK0 + k for r in rounds for k in range(3)], 'reveals': [r['start'] + REVEAL for r in rounds],
        'whooshes': [r['start'] - .08 for r in rounds] + [O - .08], 'introPops': [beats['hi'], beats['title'], beats['rules'], beats['go']],
        'outroPops': list(outro.values())}
json.dump(cues, open('cues.json', 'w'), indent=1)
print(f'{NR} rounds, first at {T0:.2f}s, outro at {O:.2f}s, total {DUR:.2f}s; {len(lines)} voice lines')
