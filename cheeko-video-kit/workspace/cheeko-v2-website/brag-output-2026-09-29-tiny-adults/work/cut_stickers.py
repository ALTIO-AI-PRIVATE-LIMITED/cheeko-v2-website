"""Cut the 14 V09 stickers out of Ravi's ChatGPT sticker sheet (white background, 1024x1536) into
transparent 3x PNG stickers. The old white border and its grey shadow ring are removed;
compose.html adds a fresh border with the #stk filter.
Usage (inside work/): ../../.venv/bin/python cut_stickers.py"""
from collections import deque
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = 'stickers/kids-sheet-source.png'
# sticker boxes found from the ink bands of the sheet (x0, y0, x1, y1)
R1, R2, R3, R4 = (30, 391), (433, 771), (797, 1136), (1145, 1502)
BOX = {
    'corp-adult': (31, R1[0], 223, R1[1]), 'corp-kid': (258, R1[0], 482, R1[1]), 'infl-adult': (533, R1[0], 761, R1[1]), 'infl-kid': (794, R1[0], 1008, R1[1]),
    'news-adult': (23, R2[0], 247, R2[1]), 'news-kid': (272, R2[0], 489, R2[1]), 'uncle-adult': (519, R2[0], 739, R2[1]), 'uncle-kid': (801, R2[0], 985, R2[1]),
    'tired-adult': (22, R3[0], 264, R3[1]), 'tired-kid': (274, R3[0], 500, R3[1]), 'bday-confused': (532, R3[0], 729, R3[1]), 'bday-cheer': (802, R3[0], 998, R3[1]),
    'cake': (249, R4[0], 488, R4[1]), 'balloons': (545, R4[0], 763, R4[1]),
}
PAD, UP, THRESH, INK = 14, 3, 60, 215
KEY = (255, 0, 255)
N8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def components(m):
    """Label 8-connected True regions; returns list of (area, touches_side, pixel index arrays)."""
    h, w = m.shape; seen = np.zeros_like(m); out = []
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]: continue
        q = deque([(y0, x0)]); seen[y0, x0] = True; ys, xs = [], []
        while q:
            y, x = q.popleft(); ys.append(y); xs.append(x)
            for dy, dx in N8:
                yy, xx = y + dy, x + dx
                if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True; q.append((yy, xx))
        ys, xs = np.array(ys), np.array(xs)
        side = xs.min() == 0 or xs.max() == w - 1 or ys.min() == 0
        out.append((len(ys), side, (ys, xs)))
    return out


def fill_holes(m):
    """Make transparent pockets that don't reach the edge opaque (speech bubble, clock face, mugs)."""
    h, w = m.shape; outside = np.zeros_like(m); q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if not m[y, x] and not outside[y, x]: outside[y, x] = True; q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if not m[y, x] and not outside[y, x]: outside[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and not m[yy, xx] and not outside[yy, xx]:
                outside[yy, xx] = True; q.append((yy, xx))
    return ~outside


import os
sheet = Image.open(SRC).convert('RGB')
W, H = sheet.size
for name, (x0, y0, x1, y1) in BOX.items():
    # a one-sticker-per-image version in stickers/hires-source/ (made later, ~4x sharper) wins over the sheet crop
    hires = f'stickers/hires-source/{name}.png'
    if os.path.exists(hires):
        im = Image.open(hires).convert('RGB'); up = 1
    else:
        box = (max(0, x0 - PAD), max(0, y0 - PAD), min(W, x1 + PAD), min(H, y1 + 8))
        im = sheet.crop(box); up = UP
    w, h = im.size
    k = 1 if up == UP else 4          # scale the edge clean-up to the image's resolution
    canvas = Image.new('RGB', (w + 4, h + 4), (255, 255, 255)); canvas.paste(im, (2, 2))
    ImageDraw.floodfill(canvas, (0, 0), KEY, thresh=THRESH)
    a = np.asarray(canvas).astype(int)[2:-2, 2:-2]
    body = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    # keep only what sits within 3 px of real ink: drops the old white border and its grey ring
    ink = Image.fromarray(((a.min(2) < INK) & body).astype(np.uint8) * 255, 'L').filter(ImageFilter.MaxFilter(7 if k == 1 else 11))
    m = body & (np.asarray(ink) > 0)
    m = fill_holes(m)
    comps = components(m); big = max(c[0] for c in comps)
    keep = np.zeros_like(m)
    for area, side, (ys, xs) in comps:
        if area < 120 * k * k: continue                  # specks left from the ring
        if side and area < .06 * big: continue           # slivers of the neighbouring panel
        px = a[ys, xs]; light, sat = px.min(1).mean(), (px.max(1) - px.min(1)).mean()
        if area < .25 * big and light > 165 and sat < 24: continue   # pale grey remnants of the old border and its shadow
        keep[ys, xs] = True
    rgb = np.asarray(im).copy(); rgb[~keep] = 255
    out = Image.fromarray(np.dstack([rgb, keep.astype(np.uint8) * 255]), 'RGBA')
    out = out.crop(out.getchannel('A').getbbox())
    out.putalpha(out.getchannel('A').filter(ImageFilter.GaussianBlur(.6 * k)))
    if up > 1: out = out.resize((out.width * up, out.height * up), Image.LANCZOS)
    out.save(f'stickers/{name}.png')
    print(name, out.size, 'hires' if up == 1 else 'sheet', len(comps), 'regions')
