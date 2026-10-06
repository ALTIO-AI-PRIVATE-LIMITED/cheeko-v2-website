"""Measure the screen of the new Cheeko render (Sep 2026 design) and write the screen mask the video template uses.

The black glass is one connected dark area around the baked-in UI; the screen is that area plus everything it encloses. All three colour renders share one geometry.
Writes assets/img/device-v2/screen_mask.png (the screen's own box, white = screen) and prints the box as fractions of the
trimmed front render, for .scr in feature.html.
usage: device_v2_mask.py
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

A = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website/assets/img/device-v2")
im = Image.open(A / "full/yellow_front.png").convert("RGBA"); a = np.array(im).astype(int); H, W = a.shape[:2]
r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
body = (al > 200) & (((r - b) > 40) & (r > 110) | ((r > 200) & (g > 200) & (b > 200)))

y1c = int(H * .47)                                          # the screen lives in the top part
dark = (al[:y1c] > 200) & (np.maximum(np.maximum(r, g), b)[:y1c] < 70)   # the black glass around the UI
row = int(H * .25); sx = next(x for x in range(int(W * .10), W // 2) if dark[row, x])   # first dark pixel from the left
comp = Image.fromarray(np.where(dark, 255, 0).astype(np.uint8)).copy()   # .copy(): floodfill is a no-op on array-backed images (Pillow 12)
ImageDraw.floodfill(comp, (sx, row), 128, thresh=0)                  # the glass: one connected dark ring + background
ring = np.array(comp) == 128
out = Image.fromarray(np.where(ring, 255, 0).astype(np.uint8)).copy()
ImageDraw.floodfill(out, (0, 0), 100, thresh=0)                      # outside the ring
m = np.array(out) != 100                                             # ring + everything it encloses = the screen
ys, xs = np.where(m); x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
box = {"left": x0 / W, "top": y0 / H, "width": (x1 - x0) / W, "height": (y1 - y0) / H, "aspect": (x1 - x0) / (y1 - y0)}
alpha = Image.fromarray(np.where(m[y0:y1, x0:x1], 255, 0).astype(np.uint8)).copy()
mk = Image.new("RGBA", alpha.size, (255, 255, 255, 0)); mk.putalpha(alpha)   # CSS masks use ALPHA: an opaque grey PNG clips nothing
mk.save(A / "screen_mask.png")
(A / "geometry.json").write_text(json.dumps({"render": [W, H], "aspect_h_over_w": H / W, "screen": box,
    "knob": [0.49, 0.571], "speaker": [0.5, 0.843]}, indent=1))
print(json.dumps(box, indent=1), "px", x0, y0, x1, y1)
