"""Timeline + voice track for one level of V31 Guess the Vehicle (on-device quiz). Reads rounds.json and the Cheeko voice
clips in vo/clips (feature_lines.json V31, recorded with feature_rec.py), trims each clip, places every line and writes:
  vo/vo_L<level>.wav            the voice track (48 kHz mono)
  timeline_L<level>.json/.js    intro beats, round start times, outro beats, for compose.html?level=<level>
  cues_L<level>.json            ticks, chimes, whooshes and pops for synth.py
Usage: python3 build_quiz.py <level 1-3> <answer seconds 2-5>"""
import json, subprocess, sys, wave, numpy as np
SR = 48000
LV, N = int(sys.argv[1]), int(sys.argv[2])
R = [r for r in json.load(open('rounds.json'))['rounds'] if r['level'] == LV]
PROMPT, TICK0 = .4, 1.9                   # times inside a round
REVEAL = TICK0 + N; NAME = REVEAL + .25; ROUND = REVEAL + 4.1
NAME0 = 26                                # feature_lines.json V31: first vehicle name line

def clip(i):
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f'vo/clips/V31_{i:02d}.mp3', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    x = np.frombuffer(raw, np.int16).astype(float) / 32768
    e = np.convolve(np.abs(x), np.ones(480) / 480, 'same'); on = np.where(e > 10 ** (-42 / 20))[0]
    a, b = max(0, on[0] - int(SR * .02)), min(len(x), on[-1] + int(SR * .08))
    y = x[a:b].copy(); f = int(SR * .01); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y

lines, clips = [], {}
def say(i, t):
    clips.setdefault(i, clip(i)); lines.append((t, i)); return t + len(clips[i]) / SR

beats, t = {}, .45
for key, i, gap in [('hi', 0 if LV == 1 else 1, .3), ('title', 2, .3), ('level', 2 + LV, .35), ('rules', 6, .4), ('go', 7, .2)]:
    beats[key] = t; t = say(i, t) + gap
T0 = t + .35
rounds = []
for k, r in enumerate(R):
    s = T0 + k * ROUND
    p = 8 if k == 0 else 17 if k == len(R) - 1 else 9 + (k - 1) % 8
    pe = say(p, s + PROMPT) - s
    if pe > TICK0 - .05: print(f'warning: round {r["n"]} prompt ends at {pe:.2f}s, after the countdown starts')
    ne = say(NAME0 + r['n'] - 1, s + NAME) - s
    rounds.append({'n': r['n'], 'k': k + 1, 'label': r['label'], 'start': round(s, 3), 'prompt': p, 'promptEnd': round(pe, 3), 'nameEnd': round(ne, 3),
                   'img': r['img'], 'crop': r.get('crop', [.5, .5, 1])})
O = T0 + len(R) * ROUND
outro, t = {}, O + .35
done, nxt = {1: (18, 19), 2: (20, 21), 3: (22, 23)}[LV]
for key, i, gap in [('done', done, .3), ('howmany', 24, .35), ('next', nxt, .35), ('bye', 25, .3)]:
    outro[key] = t; t = say(i, t) + gap
DUR = round(t + 1.6, 2)

vo = np.zeros(int(SR * DUR) + SR)
for t0, i in lines:
    a = int(t0 * SR); vo[a:a + len(clips[i])] += clips[i]
vo = vo[:int(SR * DUR)]; vo = vo / np.abs(vo).max() * .9
with wave.open(f'vo/vo_L{LV}.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
TL = {'level': LV, 'answer': N, 'dur': DUR, 'round': ROUND, 'n': len(R), 'intro': beats, 'rounds': rounds, 'outroStart': round(O, 3), 'outro': outro,
      'times': {'prompt': PROMPT, 'tick0': TICK0, 'reveal': REVEAL, 'name': NAME}}
json.dump(TL, open(f'timeline_L{LV}.json', 'w'), indent=1, ensure_ascii=False)
open(f'timeline_L{LV}.js', 'w').write('window.TL = ' + json.dumps(TL, ensure_ascii=False) + ';\n')
cues = {'level': LV, 'dur': DUR, 'answer': N, 'roundStarts': [r['start'] for r in rounds], 'tick0': TICK0, 'reveal': REVEAL, 'outro': O,
        'ticks': [r['start'] + TICK0 + j for r in rounds for j in range(N)], 'reveals': [r['start'] + REVEAL for r in rounds],
        'whooshes': [r['start'] - .08 for r in rounds] + [O - .08], 'introPops': [beats[k] for k in ('hi', 'title', 'level', 'rules', 'go')],
        'outroPops': list(outro.values())}
json.dump(cues, open(f'cues_L{LV}.json', 'w'), indent=1)
print(f'level {LV}: {len(R)} rounds of {ROUND:.1f}s ({N}s to answer), first at {T0:.2f}s, outro at {O:.2f}s, total {DUR:.2f}s; {len(lines)} voice lines')
