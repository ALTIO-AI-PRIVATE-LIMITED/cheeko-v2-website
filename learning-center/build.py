"""Build the timeline, voice track and sound cues for one Learning Center video from ideas.json + the recorded clips.
Usage: python3 build.py <idea number 1-22> <level 1..n>     (writes <slug>/timeline_L<n>.js|json, cues_L<n>.json, vo_L<n>.wav)
Each round is timed from its own clips: entrance, prompt or clue (or sound, or counting pops), a short gap, the countdown
(the level's answer seconds), the reveal, the answer line, a hold. Pictures: images/<key>.jpg, shadows images/sil/, cut-outs images/cut/."""
import json, os, subprocess, sys, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SR = 48000
D = json.load(open('ideas.json')); IDEA = D['ideas'][int(sys.argv[1]) - 1]; LV = int(sys.argv[2]); LEVEL = IDEA['levels'][LV - 1]
N = LEVEL['answer']; MODE = IDEA['mode']; NL = len(IDEA['levels'])
THEMES = json.load(open('themes.json'))
TH = THEMES[str(IDEA['n'])]

def clip(ref):
    vid, i = ref; f = f'vo/{vid.lower()}/{vid}_{i:02d}.mp3'
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    x = np.frombuffer(raw, np.int16).astype(float) / 32768
    e = np.convolve(np.abs(x), np.ones(480) / 480, 'same'); on = np.where(e > 10 ** (-42 / 20))[0]
    a, b = max(0, on[0] - int(SR * .02)), min(len(x), on[-1] + int(SR * .08))
    y = x[a:b].copy(); f2 = int(SR * .01); y[:f2] *= np.linspace(0, 1, f2); y[-f2:] *= np.linspace(1, 0, f2)
    return y
def sound_len(key):
    f = f'sounds/{key}.mp3'
    if not os.path.exists(f): return None
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))

lines, clips = [], {}
def say(ref, t):
    k = tuple(ref); clips.setdefault(k, clip(ref)); lines.append((t, k)); return t + len(clips[k]) / SR
LCX = {l[2]: ['LCX', i] for i, l in enumerate(json.load(open('lines.json'))['LCX']['lines'])}
X = lambda text: LCX[text]

beats, t = {}, .45
intro = [('hi', X("Hi! I'm Cheeko!"), .3), ('title', IDEA['title_line'], .3)]
if NL > 1: intro.append(('level', X(['Level one!', 'Level two!', 'Level three!'][LV - 1]), .35))
intro += [('rules', IDEA['rules_line'], .4), ('go', X("Ready? Let's go!"), .2)]
for key, ref, gap in intro:
    beats[key] = t; t = say(ref, t) + gap
beats.setdefault('level', beats['title'] + 1.2)
t += .35

paths, rounds, cues = {}, [], {'ticks': [], 'reveals': [], 'whooshes': [], 'pops': [], 'sounds': [], 'covers': [], 'missing_sounds': []}
def P(kind, key):
    k = {'img': key, 'sil': 'sil_' + key, 'cut': 'cut_' + key}[kind]
    paths[k] = {'img': f'../images/{key}.jpg', 'sil': f'../images/sil/{key}.jpg', 'cut': f'../images/cut/{key}.png'}[kind]; return k
items = LEVEL['items']; prompts = IDEA['prompts']
for k, it in enumerate(items):
    s = t; r = {'k': k + 1, 'start': round(s, 3), 'label': it['label'], 'pill': it['label']}
    T = {}
    first, last = k == 0, k == len(items) - 1
    pref = X("Here's the first one!") if first else X("Here's the last one!") if last else prompts[(k - 1) % len(prompts)]
    if MODE in ('ask', 'riddle'):
        T['ask0'] = .4; pe = say(it['ask_line'], s + .4) - s; r['bubble'] = json.load(open('lines.json'))[it['ask_line'][0]]['lines'][it['ask_line'][1]][2]
    elif MODE == 'missing':
        pe = say(IDEA['prompts'][0], s + .4) - s; cover = max(pe + .7, 3.2); T['cover'] = cover; cues['covers'].append(s + cover)
        pe = say(IDEA['after_line'], s + cover + .35) - s
    else:
        pe = say(pref, s + .4) - s
    if MODE == 'sound':
        sl = sound_len(it['sound']); T['snd0'] = pe + .25; dur = sl or 2.0
        if sl is None: cues['missing_sounds'].append(it['sound'])
        cues['sounds'].append([s + T['snd0'], it['sound']]); T['snd1'] = T['snd0'] + dur; pe = T['snd1']
    if MODE == 'count':
        n = it['count']; T['pop0'] = .55; T['popGap'] = min(.38, 2.6 / n); pe = max(pe, T['pop0'] + n * T['popGap'] + .25)
        cues['pops'] += [s + T['pop0'] + i * T['popGap'] for i in range(n)]
    T['tick0'] = pe + .3; T['reveal'] = T['tick0'] + N; T['name'] = T['reveal'] + .25
    ne = say(it['say_line'], s + T['name']) - s
    end = max(ne + 1.0, T['reveal'] + 2.6)
    r['times'] = {a: round(b, 3) for a, b in T.items()}; r['dur'] = round(end, 3)
    cues['ticks'] += [s + T['tick0'] + j for j in range(N)]; cues['reveals'].append(s + T['reveal']); cues['whooshes'].append(s - .08)
    # pictures for each mode
    if MODE == 'shadow': r['img'] = P('sil', it['img']); r['img2'] = P('img', it['img'])
    elif MODE == 'swap': r['img'] = P('img', it['img']); r['img2'] = P('img', it['img2']); r['pill'] = f"{it['sub']} and {it['label']}"
    elif MODE in ('odd', 'missing'): r['grid'] = [P('img', g) for g in it['imgs']]; r['odd'] = it['odd']
    elif MODE == 'count': r['cut'] = P('cut', it['img']); r['count'] = it['count']
    elif MODE == 'pair': r['cut'] = [P('cut', g) for g in it['imgs']]
    else: r['img'] = P('img', it['img'])
    if MODE == 'zoom':
        rings = json.load(open('rings.json')); r['ring'] = rings[it['ring']]
    if it.get('letter'): r['letter'] = it['letter']
    if it.get('shape'): r['shape'] = it['shape']
    rounds.append(r); t = s + end
O = t
outro, t = {}, O + .35
nxt = X('Ready for level two?') if (NL > 1 and LV == 1) else X('Now try level three!') if (NL > 2 and LV == 2) else X('Play again and beat your score!')
for key, ref, gap in [('done', IDEA['done_line'], .3), ('howmany', X('How many did you get right?'), .35), ('next', nxt, .35), ('bye', X('Bye bye!'), .3)]:
    outro[key] = t; t = say(ref, t) + gap
DUR = round(t + 1.6, 2)

vo = np.zeros(int(SR * DUR) + SR)
for t0, k in lines:
    a = int(t0 * SR); vo[a:a + len(clips[k])] += clips[k]
vo = vo[:int(SR * DUR)]; vo = vo / np.abs(vo).max() * .9
os.makedirs(IDEA['slug'], exist_ok=True)
with wave.open(f"{IDEA['slug']}/vo_L{LV}.wav", 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
chips = {'sound': [['?', 'Listen closely'], [str(N), f'{N} seconds'], ['!', 'Say the name']], 'count': [['?', 'Count them'], [str(N), f'{N} seconds'], ['!', 'Say how many']],
         'letter': [['A', 'Look at the letter'], [str(N), f'{N} seconds'], ['!', 'Say the word']], 'odd': [['?', 'Look at all four'], [str(N), f'{N} seconds'], ['!', 'Find the odd one']],
         'missing': [['?', 'Remember them'], [str(N), f'{N} seconds'], ['!', 'Say what went']], 'ask': [['?', 'Listen to Cheeko'], [str(N), f'{N} seconds'], ['!', 'Say the answer']],
         'riddle': [['?', 'Listen to the clues'], [str(N), f'{N} seconds'], ['!', 'Guess the answer']], 'zoom': [['?', 'Look at the circle'], [str(N), f'{N} seconds'], ['!', 'Touch and say']],
         'pair': [['?', 'Look at both'], [str(N), f'{N} seconds'], ['!', 'Say the word']], 'swap': [['?', 'Look at the mummy'], [str(N), f'{N} seconds'], ['!', 'Say the baby']]}
def edge(img):                       # a picture's border colour, to fill around it when the question shrinks it
    raw = subprocess.check_output(['ffmpeg', '-loglevel', 'error', '-i', img, '-vf', 'scale=16:16', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    a = np.frombuffer(raw, np.uint8).reshape(16, 16, 3).astype(float); e = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    return 'rgb(%d,%d,%d)' % tuple(e.mean(0))
for r in rounds:
    if MODE == 'ask' and r.get('bubble') and r.get('img'): r['edge'] = edge(paths[r['img']].replace('../', '', 1))
stamp = ['Great job!', 'Awesome!', 'Super!', 'Brilliant!', 'Well done!'][(IDEA['n'] + LV) % 5]
TL = {'idea': IDEA['slug'], 'id': IDEA['id'], 'level': LV, 'nLevels': NL, 'mode': MODE, 'theme': TH, 'answer': N, 'dur': DUR, 'n': len(items),
      't1': IDEA['t1'], 't2': IDEA['t2'], 'head': IDEA['head'], 'chips': chips.get(MODE, [['?', 'Look closely'], [str(N), f'{N} seconds'], ['!', IDEA.get('chip3', 'Say the name')]]),
      'outroText': [stamp, f'Level {LV} done!' if NL > 1 else 'All done!', f'Play Level {LV + 1}!' if LV < NL else 'Play again!'],
      'intro': beats, 'rounds': rounds, 'outroStart': round(O, 3), 'outro': outro, 'paths': paths}
json.dump(TL, open(f"{IDEA['slug']}/timeline_L{LV}.json", 'w'), indent=1, ensure_ascii=False)
open(f"{IDEA['slug']}/timeline_L{LV}.js", 'w').write('window.TL = ' + json.dumps(TL, ensure_ascii=False) + ';\n')
cues.update({'dur': DUR, 'answer': N, 'music': TH['music'], 'outro': O, 'roundStarts': [r['start'] for r in rounds],
             'roundTick0': [r['start'] + r['times']['tick0'] for r in rounds], 'roundReveal': [r['start'] + r['times']['reveal'] for r in rounds],
             'introPops': [beats[k] for k in ('hi', 'title', 'level', 'rules', 'go')], 'outroPops': list(outro.values())})
cues['whooshes'].append(O - .08)
json.dump(cues, open(f"{IDEA['slug']}/cues_L{LV}.json", 'w'), indent=1)
miss = [k for k, v in paths.items() if not os.path.exists(os.path.join('engine', v))]
print(f"{IDEA['id']} {IDEA['slug']} L{LV}: {len(items)} rounds, {N}s to answer, {DUR:.1f}s" + (f"; missing pictures {miss}" if miss else '') +
      (f"; missing sounds {len(cues['missing_sounds'])}" if cues['missing_sounds'] else ''))
