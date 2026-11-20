"""Write ../manifest.json (sources, licences, crops, voice lines with their speech checks, timings, outputs) and ../SCRIPT.md
(the spoken script with times) for V30. Usage: python3 manifest.py [rounds, default 10]"""
import json, re, sys, os, glob
NR = int(sys.argv[1]) if len(sys.argv) > 1 else 10
R = json.load(open('rounds.json')); T = json.load(open('timeline.json'))
L = json.load(open('/Users/ravikumar/Cheeko Master/marketing/tools/feature_lines.json'))['V30']['lines']
heard = {}
for l in open('vo/rec.log'):
    m = re.match(r'(\d+) .*?\| (.*?) \| heard: (.*)', l.strip())
    if m: heard[int(m.group(1))] = m.group(3)
heard.update({42: 'Whale shark.', 43: 'Sea Urchin', 56: 'Koi carp', 59: 'Seal', 66: 'Barracuda', 68: 'See, Anemone. (Sarvam; clear on listen)',
              82: 'Konk', 92: 'Boxfish', 93: 'Krill (Whisper small.en; Sarvam hears "Grill")', 101: 'Blobfish', 102: "Here's the last one."})
rounds = []
for r, t in zip(R['rounds'][:NR], T['rounds']):
    s = r.get('source') or {}
    rounds.append({'n': r['n'], 'answer': r['label'], 'start_s': t['start'], 'image': r.get('img'), 'crop_focus_zoom': r['crop'],
                   'envato_item': s.get('envato_item'), 'envato_title': s.get('title'), 'original_file': s.get('file'), 'licence': s.get('licence'),
                   'prompt_line': t['prompt'], 'prompt_text': L[t['prompt']][2] if t['prompt'] is not None else None,
                   'name_line': 22 + r['n'] - 1, 'name_heard_by_stt': heard.get(22 + r['n'] - 1), 'species_check': 'checked by eye against the species (Claude, 2026-10-08)'})
outs = sorted(glob.glob('../device/*')) + ['../preview_on_device.mp4']
M = {'id': 'V30', 'title': 'Ocean and Water Animals (on-device quiz)', 'date': '2026-10-08', 'status': f'{NR}-animal cut rendered; full list of 80 in rounds.json',
     'screen': {'panel': 'JD9853 2.01in IPS', 'logical_px': [296, 240], 'render': '2x (592x480) then Lanczos to 296x240',
                'safe_area': 'glass corners curve in ~78 px from the sides and ~74 px from top and bottom (device-v2/screen_mask.png)'},
     'voice': {'engine': 'MiniMax speech-2.8-hd', 'voice': 'English_PlayfulGirl (Cheeko)', 'recorder': 'marketing/tools/feature_rec.py feature_lines.json V30',
               'check': 'Sarvam saarika:v2.5 en-IN on every clip; Whisper for short names Sarvam mishears'},
     'music': 'original, synth.py (D major, 112 BPM, marimba, glockenspiel, plucked bass, shaker), ducked under the voice and during each countdown',
     'sfx': 'synth.py: wood-block ticks at 3, 2, 1; glockenspiel chime on each reveal; water whoosh on each wave wipe; pops',
     'timing_s': {'round': T['round'], 'inside_round': T['times'], 'first_round': T['rounds'][0]['start'], 'outro': T['outroStart'], 'total': T['dur']},
     'paid_generation': 'none (no AI images or video used); voice TTS only',
     'rounds': rounds, 'outputs': [{'file': os.path.basename(o), 'bytes': os.path.getsize(o)} for o in outs if os.path.exists(o)]}
json.dump(M, open('../manifest.json', 'w'), indent=1, ensure_ascii=False)
lines = [f'# V30 Ocean and Water Animals: script ({NR} animals)', '', 'Cheeko\'s voice (MiniMax English_PlayfulGirl). Times are in the finished video.', '']
for k, t0 in T['intro'].items():
    if k == 'go_end': continue
    i = {'hi': 0, 'title': 1, 'rules': 2, 'harder': 3, 'go': 4}[k]; lines.append(f'- {t0:6.2f}s  {L[i][2]}')
for r in rounds:
    st = r['start_s']
    if r['prompt_text']: lines.append(f'- {st + T["times"]["prompt"]:6.2f}s  {r["prompt_text"]}')
    lines.append(f'- {st + T["times"]["tick0"]:6.2f}s  (3, 2, 1 ticks)')
    lines.append(f'- {st + T["times"]["name"]:6.2f}s  {r["answer"]}!   (label "{r["answer"]}")')
for k, t0 in T['outro'].items():
    i = {'wow': 18, 'howmany': 19, 'again': 20, 'bye': 21}[k]; lines.append(f'- {t0:6.2f}s  {L[i][2]}')
open('../SCRIPT.md', 'w').write('\n'.join(lines) + '\n')
print('wrote ../manifest.json and ../SCRIPT.md')
