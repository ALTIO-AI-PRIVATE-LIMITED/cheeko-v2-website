"""Collect every picture into images/<key>.jpg, then make the shadows (images/sil/) and cut-outs (images/cut/) the engine needs,
and contact sheets for checking (sheets/). Usage: python3 prep_images.py [gen_dir]   (gen_dir holds lc_<key>.jpg from the dev box)"""
import json, os, sys, glob
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
GEN = sys.argv[1] if len(sys.argv) > 1 else 'gen'
D = json.load(open('ideas.json'))
V31 = '/Users/ravikumar/Cheeko Master/cheeko-v2-website/brag-output-2026-10-09-vehicles/work/assets/vehicles/'
LCS = '/Users/ravikumar/Cheeko Master/marketing/learning-center/samples/'
os.makedirs('images/sil', exist_ok=True); os.makedirs('images/cut', exist_ok=True); os.makedirs('sheets', exist_ok=True)

def save(src, key):
    im = Image.open(src).convert('RGB'); im.thumbnail((1536, 1536), Image.LANCZOS); im.save(f'images/{key}.jpg', quality=90)
def save_photo(src, key):      # Envato photo -> 1536x1152: centre crop unless it is a portrait photo, which goes over a blurred copy of itself
    im = Image.open(src).convert('RGB'); W, H = 1536, 1152
    if im.width / im.height >= 1.05:
        r = max(W / im.width, H / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, t = (im.width - W) // 2, (im.height - H) // 2; out = im.crop((l, t, l + W, t + H))
    else:
        r = max(W / im.width, H / im.height); bg = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, t = (bg.width - W) // 2, (bg.height - H) // 2; out = bg.crop((l, t, l + W, t + H)).filter(ImageFilter.GaussianBlur(28))
        out = Image.blend(out, Image.new('RGB', (W, H), (20, 30, 60)), .25)
        fg = im.copy(); fg.thumbnail((W, H), Image.LANCZOS); out.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    out.save(f'images/{key}.jpg', quality=90)
for key, ref in D['reuse'].items():
    if os.path.exists(f'images/{key}.jpg') and not ref.startswith('env:'): continue
    kind, name = ref.split(':')
    if kind == 'env': save_photo(f'photos/raw/{name}.jpg', key); continue
    src = (V31 + name + '.jpg') if kind == 'v31' else (LCS + 'lc_' + name + '.jpg') if kind == 'lc' else None
    save(src, key)
missing = []
for key in D['new']:
    src = f'{GEN}/lc_{key}.jpg'
    if os.path.exists(src): save(src, key)
    elif not os.path.exists(f'images/{key}.jpg'): missing.append(key)

KEEP_DARK = {'rain_cloud'}; NO_FLOOR = {'fruit_grapes', 'fruit_strawberry', 'owl'}
def mask_of(key):
    a = np.asarray(Image.open(f'images/{key}.jpg').convert('RGB')).astype(float)
    vm = f'images/mask/{key}.png'     # Apple Vision subject mask (swift mask.swift images/mask images/<key>.jpg), best for white/blue/grey subjects
    if os.path.exists(vm):
        m = np.asarray(Image.open(vm).convert('L').resize((a.shape[1], a.shape[0]), Image.LANCZOS)) > 127
        border = np.concatenate([a[:20].reshape(-1, 3), a[-20:].reshape(-1, 3), a[:, :20].reshape(-1, 3), a[:, -20:].reshape(-1, 3)])
        bg = np.median(border, 0); d = np.sqrt(((a - bg) ** 2).sum(2))
        if key in KEEP_DARK:      # parts Vision drops (rain drops): add clearly darker pixels
            add = np.asarray(Image.fromarray(((d > 55) * 255).astype('uint8')).filter(ImageFilter.MedianFilter(5))) > 127
            lab, n = ndimage.label(add & ~m)
            for i, sl in enumerate(ndimage.find_objects(lab), 1):     # keep drop-like blobs, drop the flat puddle on the floor
                h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
                if w > 2.5 * h: add[lab == i] = False
            m = m | add
        if key in NO_FLOOR:       # Vision keeps the floor disc under these: keep only pixels near the real colours
            blueish = (a[:, :, 2] > a[:, :, 0] + 25) & (a[:, :, 2] > a[:, :, 1] + 5) & (d < 140)
            near = Image.fromarray((((d > 60) & ~blueish) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(21))
            m = ndimage.binary_fill_holes(m & (np.asarray(near.filter(ImageFilter.MinFilter(9))) > 127))
        return a, bg, m
    border = np.concatenate([a[:20].reshape(-1, 3), a[-20:].reshape(-1, 3), a[:, :20].reshape(-1, 3), a[:, -20:].reshape(-1, 3)])
    bg = np.median(border, 0); d = np.sqrt(((a - bg) ** 2).sum(2))
    blueish = (a[:, :, 2] > a[:, :, 0] + 25) & (a[:, :, 2] > a[:, :, 1] + 5) & (d < 140)     # soft floor shadow and sky stay background
    fg = Image.fromarray((((d > 60) & ~blueish) * 255).astype('uint8')).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    out = fg.point(lambda v: 0 if v > 128 else 255).convert('L'); ImageDraw.floodfill(out, (0, 0), 128)
    return a, bg, np.asarray(out) != 128
used = {'sil': set(), 'cut': set()}
for d in D['ideas']:
    for lv in d['levels']:
        for it in lv['items']:
            if d['mode'] == 'shadow': used['sil'].add(it['img'])
            if d['mode'] == 'count': used['cut'].add(it['img'])
            if d['mode'] == 'pair': used['cut'].update(it['imgs'])
for key in sorted(used['sil']):
    if not os.path.exists(f'images/{key}.jpg'): continue
    a, bg, m = mask_of(key); sil = np.empty_like(a); sil[:] = bg; sil[m] = (22, 32, 64)
    Image.fromarray(sil.astype('uint8')).filter(ImageFilter.SMOOTH).save(f'images/sil/{key}.jpg', quality=90)
for key in sorted(used['cut']):
    if not os.path.exists(f'images/{key}.jpg'): continue
    a, bg, m = mask_of(key); alpha = Image.fromarray((m * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    rgba = Image.fromarray(a.astype('uint8')).convert('RGBA'); rgba.putalpha(alpha)
    bb = alpha.getbbox(); rgba = rgba.crop(bb) if bb else rgba; rgba.thumbnail((600, 600), Image.LANCZOS); rgba.save(f'images/cut/{key}.png')

def sheet(keys, out, cols=6, folder='images', ext='jpg'):
    W, H = 300, 225; S = Image.new('RGB', (cols * (W + 6), ((len(keys) + cols - 1) // cols) * (H + 22)), (25, 25, 25)); dr = ImageDraw.Draw(S)
    for i, k in enumerate(keys):
        x, y = (i % cols) * (W + 6), (i // cols) * (H + 22); f = f'{folder}/{k}.{ext}'
        if os.path.exists(f):
            im = Image.open(f).convert('RGBA'); bgc = Image.new('RGBA', im.size, (142, 197, 245, 255)); bgc.alpha_composite(im)
            im = bgc.convert('RGB'); im.thumbnail((W, H)); S.paste(im, (x + (W - im.width) // 2, y + 20))
        dr.text((x + 4, y + 4), k, fill=(255, 255, 0))
    S.save(out, quality=85)
new = list(D['new'])
for i in range(0, len(new), 30): sheet(new[i:i + 30], f'sheets/new_{i // 30:02d}.jpg')
sheet(sorted(used['sil']), 'sheets/shadows.jpg', folder='images/sil'); sheet(sorted(used['cut']), 'sheets/cutouts.jpg', folder='images/cut', ext='png')
print('pictures:', len(glob.glob('images/*.jpg')), 'missing:', missing, '| shadows', len(used['sil']), 'cut-outs', len(used['cut']))
