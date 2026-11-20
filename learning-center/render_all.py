"""Render approved ideas end to end, two videos at a time: build -> synth -> render (2x) -> finish (device MP4).
Usage: /usr/bin/python3 render_all.py <idea number>...   Progress in renders.log; finished files in <slug>/device/."""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
D = json.load(open('ideas.json'))
def log(msg):
    with open('renders.log', 'a') as f: f.write(time.strftime('%H:%M:%S ') + msg + '\n')
def name(idea, lv):
    t = re.sub(r'[^A-Za-z0-9 ]', '', idea['title']).strip().replace(' ', '_')
    return f"Cheeko_{idea['id']}.{lv}_{t}_Level_{lv}" if len(idea['levels']) > 1 else f"Cheeko_{idea['id']}_{t}"
def job(n, lv):
    idea = D['ideas'][n - 1]; slug = idea['slug']; nm = name(idea, lv); t0 = time.time()
    try:
        subprocess.run(['/usr/bin/python3', 'build.py', str(n), str(lv)], check=True, capture_output=True)
        subprocess.run(['/usr/bin/python3', 'synth.py', str(n), str(lv)], check=True, capture_output=True)
        dur = json.load(open(f'{slug}/timeline_L{lv}.json'))['dur']
        r = subprocess.run(['node', 'render.mjs', slug, str(lv), str(dur)], cwd='engine', check=True, capture_output=True, text=True)
        subprocess.run(['bash', 'finish.sh', slug, str(lv), nm], check=True, capture_output=True)
        log(f'done {nm} {dur:.0f}s in {time.time() - t0:.0f}s {r.stdout.strip().split("frames")[-1].strip()}')
    except subprocess.CalledProcessError as e:
        log(f'FAILED {nm}: {(e.stderr or b"")[-400:]!r}')
jobs = [(n, lv) for n in map(int, sys.argv[1:]) for lv in range(1, len(D['ideas'][n - 1]['levels']) + 1)]
log(f'start {len(jobs)} videos')
with ThreadPoolExecutor(2) as ex: list(ex.map(lambda a: job(*a), jobs))
log('all finished')
