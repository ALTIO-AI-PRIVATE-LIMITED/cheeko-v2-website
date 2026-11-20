"""Review sheet for one idea, for Ravi's yes before any final render: builds every level, then stills of the intro, the first
question (before the answer), every round's reveal in every level, and the outro. Writes stills/<NN>/<ID>_review.jpg.
Usage: /usr/bin/python3 review.py <idea number> [...]"""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
D = json.load(open('ideas.json'))
for n in map(int, sys.argv[1:]):
    idea = D['ideas'][n - 1]; slug = idea['slug']; out = f'stills/{n:02d}'; os.makedirs(out, exist_ok=True)
    for f in glob.glob(f'{out}/*.png'): os.remove(f)
    for lv in range(1, len(idea['levels']) + 1):
        subprocess.run(['/usr/bin/python3', 'build.py', str(n), str(lv)], check=True)
        t = json.load(open(f'{slug}/timeline_L{lv}.json')); r0 = t['rounds'][0]
        ts = [r['start'] + r['times']['name'] + .9 for r in t['rounds']]
        if lv == 1:
            ts = [t['intro']['level'] + 1.0 if 'level' in t['intro'] else t['intro']['title'] + 1.5,
                  r0['start'] + (r0['times']['tick0'] + r0['times']['reveal']) / 2] + ts + [t['outro']['howmany'] + 1.4]
        subprocess.run(['node', 'stills.mjs', slug, str(lv), f'../{out}/L{lv}_'] + [f'{x:.2f}' for x in ts], cwd='engine', check=True)
    subprocess.run(['/usr/bin/python3', 'sheet_stills.py', f'{out}/{idea["id"]}_review.jpg'] + sorted(glob.glob(f'{out}/L*_*.png')), check=True)
    print(f'{out}/{idea["id"]}_review.jpg')
