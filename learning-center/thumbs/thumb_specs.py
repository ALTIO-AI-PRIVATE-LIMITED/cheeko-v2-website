"""Specs for the Learning shelf thumbnails (208x116 JPEG, the picture area inside the white card): one per video, written next to it.
Writes thumbs/specs.json for make_thumbs.mjs. Usage: /usr/bin/python3 thumbs/thumb_specs.py"""
import glob, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); LC = os.path.dirname(HERE); WEB = os.path.dirname(LC)
D = json.load(open(f'{LC}/ideas.json')); T = json.load(open(f'{LC}/themes.json'))
rel = lambda p: os.path.relpath(p, HERE)
img = lambda k: rel(f'{LC}/images/{k}.jpg')
specs = []
for d in D['ideas']:
    th = T[str(d['n'])]; vids = sorted(glob.glob(f"{LC}/{d['slug']}/device/*_296x240.mp4"))
    title = f"{d['t1']} {d['t2']}"          # the same words as the video's intro title
    for i, (lv, v) in enumerate(zip(d['levels'], vids)):
        it = lv['items'][0]; m = d['mode']; s = {'mode': m, 'pics': [], 'overlay': ''}
        if m == 'shadow': s['pics'] = [rel(f"{LC}/images/sil/{it['img']}.jpg")]; s['overlay'] = 'shadow'
        elif m == 'swap': s['pics'] = [img(it['img2'])]
        elif m == 'count': s['pics'] = [rel(f"{LC}/images/cut/{it['img']}.png")]; s['overlay'] = str(it['count'])
        elif m == 'letter': s['pics'] = [img(it['img'])]; s['overlay'] = it['letter']
        elif m in ('odd', 'missing'): s['pics'] = [img(g) for g in it['imgs']]; s['hide'] = it['odd'] if m == 'missing' else -1
        elif m == 'pair': s['pics'] = [rel(f"{LC}/images/cut/{g}.png") for g in it['imgs']]
        elif m == 'riddle': s['pics'] = [img('cheeko_surprised')]; s['overlay'] = '?'
        else: s['pics'] = [img(it['img'])]
        if m == 'sound': s['overlay'] = 'sound'
        s.update(title=title, level=(i + 1) if len(d['levels']) > 1 else 0, c1=th['pals'][0][0], c2=th['pals'][0][1],
                 out=v.replace('_296x240.mp4', '_thumb_208x116.jpg'), drive=re.sub(r"[^A-Za-z0-9 ]", "", d['title']).strip())
        specs.append(s)
# V30 and V31 (made before the Learning Center engine)
V30 = f'{WEB}/brag-output-2026-10-08-ocean-animals/device/Cheeko_V30_Ocean_Animals_10_296x240.mp4'
specs.append({'mode': 'picture', 'pics': [rel('/Users/ravikumar/Cheeko Master/marketing/assets/envato/v30-ocean-animals/03_bigg-s-orca-whale-jumping-out-of-the-sea-in-vancou-2026-09-24-03-12-13-utc.jpeg')],
              'overlay': '', 'title': 'Ocean Animals', 'level': 0, 'c1': '#4DC3FF', 'c2': '#0B4F8A', 'out': V30.replace('_296x240.mp4', '_thumb_208x116.jpg'), 'drive': 'Ocean and Water Animals'})
for lv, key in ((1, '01_car'), (2, '11_fire_engine'), (3, '26_rocket')):
    v = f'{WEB}/brag-output-2026-10-09-vehicles/device/Cheeko_V31.{lv}_Guess_the_Vehicle_Level_{lv}_296x240.mp4'
    specs.append({'mode': 'picture', 'pics': [rel(f'{WEB}/brag-output-2026-10-09-vehicles/work/assets/vehicles/{key}.jpg')], 'overlay': '',
                  'title': 'Guess the Vehicle', 'level': lv, 'c1': '#FFD43B', 'c2': '#E8590C', 'out': v.replace('_296x240.mp4', '_thumb_208x116.jpg'), 'drive': 'Guess the Vehicle'})
for s in specs: assert all(os.path.exists(os.path.join(HERE, p)) for p in s['pics']), s
json.dump(specs, open(f'{HERE}/specs.json', 'w'), indent=1, ensure_ascii=False)
print(len(specs), 'thumbnails')
