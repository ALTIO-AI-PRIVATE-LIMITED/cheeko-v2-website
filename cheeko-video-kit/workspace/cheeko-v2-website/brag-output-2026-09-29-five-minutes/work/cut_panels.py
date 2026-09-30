"""Cut storyboard panels 01-12 out of Ravi's storyboard image (white background) into
transparent 3x PNG stickers. The old white border and its grey shadow ring are removed;
compose.html adds a fresh border with the #stk filter.
Usage (inside work/): ../../.venv/bin/python cut_panels.py"""
from collections import deque
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = 'stickers/storyboard-source.webp'
# panel boxes found from the ink bands of the 1145x1374 source (x0, y0, x1, y1)
BOX = {
    'p01': (14, 104, 278, 349), 'p02': (303, 104, 559, 349), 'p03': (575, 104, 863, 349), 'p04': (870, 104, 1134, 349),
    'p05': (15, 404, 277, 648), 'p06': (288, 404, 571, 648), 'p07': (589, 404, 860, 648), 'p08': (899, 404, 1116, 648),
    'p09': (7, 702, 295, 941), 'p10': (301, 702, 544, 941), 'p11': (561, 702, 803, 941), 'p12': (823, 702, 1138, 941),
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


src = Image.open(SRC).convert('RGB')
W, H = src.size
for name, (x0, y0, x1, y1) in BOX.items():
    box = (max(0, x0 - PAD), max(0, y0 - PAD), min(W, x1 + PAD), min(H, y1 + 8))
    im = src.crop(box); w, h = im.size
    canvas = Image.new('RGB', (w + 4, h + 4), (255, 255, 255)); canvas.paste(im, (2, 2))
    ImageDraw.floodfill(canvas, (0, 0), KEY, thresh=THRESH)
    a = np.asarray(canvas).astype(int)[2:-2, 2:-2]
    body = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    # keep only what sits within 3 px of real ink: drops the old white border and its grey ring
    ink = Image.fromarray(((a.min(2) < INK) & body).astype(np.uint8) * 255, 'L').filter(ImageFilter.MaxFilter(7))
    m = body & (np.asarray(ink) > 0)
    m = fill_holes(m)
    comps = components(m); big = max(c[0] for c in comps)
    keep = np.zeros_like(m)
    for area, side, (ys, xs) in comps:
        if area < 120: continue                          # specks left from the ring
        if side and area < .06 * big: continue           # slivers of the neighbouring panel
        if name == 'p03' and area < .05 * big: continue  # half-kept "5 min?" bubble; compose.html redraws it
        keep[ys, xs] = True
    rgb = np.asarray(im).copy(); rgb[~keep] = 255
    out = Image.fromarray(np.dstack([rgb, keep.astype(np.uint8) * 255]), 'RGBA')
    out = out.crop(out.getchannel('A').getbbox())
    out.putalpha(out.getchannel('A').filter(ImageFilter.GaussianBlur(.6)))
    out = out.resize((out.width * UP, out.height * UP), Image.LANCZOS)
    out.save(f'stickers/{name}.png')
    print(name, out.size, len(comps), 'regions')
