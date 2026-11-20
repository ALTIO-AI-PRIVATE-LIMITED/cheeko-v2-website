"""Write ../manifest.json (image prompts and sources, voice lines with their speech checks, timings, costs, outputs) and
../SCRIPT.md (the spoken script of each level with times) for V31 Guess the Vehicle. Usage: python3 manifest.py"""
import json, re, os, glob
R = json.load(open('rounds.json'))['rounds']
L = json.load(open('/Users/ravikumar/Cheeko Master/marketing/tools/feature_lines.json'))['V31']['lines']
heard = {}
for l in open('vo/rec.log'):
    m = re.match(r'(\d+) .*?\| (.*?) \| heard: (.*)', l.strip())
    if m: heard[int(m.group(1))] = m.group(3)
heard.update({42: 'School bus (retake)', 54: 'Cable car (retake)'})
levels, script = [], ['# V31 Guess the Vehicle: script', '', "Cheeko's voice (MiniMax English_PlayfulGirl). Times are in each finished video.", '']
for lv in (1, 2, 3):
    T = json.load(open(f'timeline_L{lv}.json'))
    levels.append({'level': lv, 'answer_s': T['answer'], 'round_s': T['round'], 'total_s': T['dur'], 'first_round_s': T['rounds'][0]['start'],
                   'rounds': [{'n': r['n'], 'answer': r['label'], 'start_s': r['start'], 'prompt': L[r['prompt']][2], 'name_line': 26 + r['n'] - 1,
                               'name_heard_by_stt': heard.get(26 + r['n'] - 1)} for r in T['rounds']]})
    script += [f'## Level {lv} ({T["answer"]} s to answer, {T["dur"]:.0f} s)', '']
    for k, t0 in T['intro'].items():
        i = {'hi': 0 if lv == 1 else 1, 'title': 2, 'level': 2 + lv, 'rules': 6, 'go': 7}[k]; script.append(f'- {t0:6.2f}s  {L[i][2]}')
    for r in T['rounds']:
        st = r['start']; script.append(f'- {st + T["times"]["prompt"]:6.2f}s  {L[r["prompt"]][2]}')
        script.append(f'- {st + T["times"]["tick0"]:6.2f}s  ({", ".join(str(T["answer"] - j) for j in range(T["answer"]))} ticks)')
        script.append(f'- {st + T["times"]["name"]:6.2f}s  {r["label"]}!')
    done, nxt = {1: (18, 19), 2: (20, 21), 3: (22, 23)}[lv]
    for k, t0 in T['outro'].items():
        i = {'done': done, 'howmany': 24, 'next': nxt, 'bye': 25}[k]; script.append(f'- {t0:6.2f}s  {L[i][2]}')
    script.append('')
C = json.load(open('costs.json'))
M = {'id': 'V31', 'title': 'Guess the Vehicle, Levels 1 to 3 (on-device quiz)', 'date': '2026-10-09',
     'screen': {'logical_px': [296, 240], 'render': '2x (592x480) then Lanczos to 296x240', 'safe_area': 'rounded glass, see V30 manifest'},
     'images': {'generator': 'Seedream 5.0 Flash via the dev box image lab (keys on the box), 1536x1152, watermark off, 3D toy style',
                'style_reference': 'the approved Car (gen/test2_car_toy_seedflash.jpg) passed as a reference image to every vehicle',
                'retakes': 'Motorbike (came out as a scooter), Ambulance (red cross removed; protected emblem), Tractor (green and yellow looked like one brand)',
                'checked': 'every image checked by eye for the right vehicle, no text, logos, flags or emblems (Claude, 2026-10-09)',
                'items': [{'n': r['n'], 'name': r['name'], 'level': r['level'], 'file': r['img'], 'prompt': r['source']['prompt']} for r in R]},
     'voice': {'engine': 'MiniMax speech-2.8-hd', 'voice': 'English_PlayfulGirl (Cheeko)', 'lines': 'feature_lines.json V31', 'check': 'Sarvam saarika:v2.5 en-IN'},
     'music_sfx': 'original, synth.py (free): marimba, glockenspiel, plucked bass, shaker; key and tempo rise per level; wood-block ticks, reveal chime, whoosh, pops',
     'cost_usd': {'images': C['spent_usd'], 'voice_estimate': 0.12, 'music_sfx': 0},
     'levels': levels,
     'outputs': [{'file': os.path.basename(o), 'bytes': os.path.getsize(o)} for o in sorted(glob.glob('../device/*')) + sorted(glob.glob('../preview_on_device_L*.mp4'))]}
json.dump(M, open('../manifest.json', 'w'), indent=1, ensure_ascii=False)
open('../SCRIPT.md', 'w').write('\n'.join(script))
print('wrote ../manifest.json and ../SCRIPT.md')
