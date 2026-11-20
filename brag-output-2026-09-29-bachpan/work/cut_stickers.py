"""Cut every single-sticker image in stickers/src/ (white background, white die-cut border) into a transparent PNG
in stickers/. Images that already have transparency are just trimmed. compose.html adds its own border/shadow.
Usage (inside work/): ../../.venv/bin/python cut_stickers.py"""
import glob, os
from collections import deque
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
KEY = (255, 0, 255)

def components(m):
    h, w = m.shape; seen = np.zeros_like(m); out = []
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]: continue
        q = deque([(y0, x0)]); seen[y0, x0] = True; ys, xs = [], []
        while q:
            y, x = q.popleft(); ys.append(y); xs.append(x)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not seen[yy, xx]: seen[yy, xx] = True; q.append((yy, xx))
        out.append((len(ys), (np.array(ys), np.array(xs))))
    return out

def fill_holes(m):
    h, w = m.shape; outside = np.zeros_like(m); q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if not m[y, x]: outside[y, x] = True; q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if not m[y, x]: outside[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and not m[yy, xx] and not outside[yy, xx]: outside[yy, xx] = True; q.append((yy, xx))
    return ~outside

for src in sorted(glob.glob('stickers/src/*.png')):
    name = os.path.splitext(os.path.basename(src))[0]; dst = f'stickers/{name}.png'
    if os.path.exists(dst) and os.path.getmtime(dst) > os.path.getmtime(src): continue
    im = Image.open(src)
    if im.mode == 'RGBA' and np.asarray(im.getchannel('A')).min() < 250:
        out = im.crop(im.getchannel('A').getbbox()); out.save(dst); print(name, out.size, 'had alpha'); continue
    im = im.convert('RGB'); w, h = im.size
    canvas = Image.new('RGB', (w + 4, h + 4), (255, 255, 255)); canvas.paste(im, (2, 2))
    ImageDraw.floodfill(canvas, (0, 0), KEY, thresh=60)
    a = np.asarray(canvas).astype(int)[2:-2, 2:-2]
    body = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    ink = Image.fromarray(((a.min(2) < 215) & body).astype(np.uint8) * 255, 'L').filter(ImageFilter.MaxFilter(11))
    m = fill_holes(body & (np.asarray(ink) > 0))
    comps = components(m); big = max(c[0] for c in comps); keep = np.zeros_like(m)
    for area, (ys, xs) in comps:
        px = a[ys, xs]
        if area < 2000: continue
        if area < .25 * big and px.min(1).mean() > 165 and (px.max(1) - px.min(1)).mean() < 24: continue
        keep[ys, xs] = True
    rgb = np.asarray(im).copy(); rgb[~keep] = 255
    out = Image.fromarray(np.dstack([rgb, keep.astype(np.uint8) * 255]), 'RGBA')
    out = out.crop(out.getchannel('A').getbbox()); out.putalpha(out.getchannel('A').filter(ImageFilter.GaussianBlur(2.4)))
    out.save(dst); print(name, out.size)
