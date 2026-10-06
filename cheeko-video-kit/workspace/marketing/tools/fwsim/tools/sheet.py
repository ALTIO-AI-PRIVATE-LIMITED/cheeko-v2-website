#!/usr/bin/env python3
"""Upscale every native PNG 4x (nearest) and build a labelled contact sheet.
usage: sheet.py OUT_DIR [--only-sheet PATTERN] [--sheet NAME] [--cols N] [--scale S]"""
import sys, os, glob, fnmatch
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]
args = sys.argv[2:]
opt = {"--pattern": "*", "--sheet": "contact_sheet.png", "--cols": "6", "--scale": "2", "--noupscale": None}
i = 0
while i < len(args):
    if args[i] == "--noupscale":
        opt["--noupscale"] = True; i += 1
    else:
        opt[args[i]] = args[i + 1]; i += 2
files = sorted(f for f in glob.glob(os.path.join(out, "*.png"))
               if not f.endswith("_4x.png") and "contact_sheet" not in os.path.basename(f)
               and fnmatch.fnmatch(os.path.basename(f), opt["--pattern"]))
if not opt["--noupscale"]:
    os.makedirs(os.path.join(out, "4x"), exist_ok=True)
    for f in files:
        im = Image.open(f)
        im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(
            os.path.join(out, "4x", os.path.basename(f)[:-4] + "_4x.png"))
s = int(opt["--scale"]); cols = int(opt["--cols"])
W, H, lab = 296 * s, 240 * s, 18
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (W + 8) + 8, rows * (H + lab + 8) + 8), (40, 40, 40))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
except Exception:
    font = ImageFont.load_default()
for n, f in enumerate(files):
    r, c = divmod(n, cols)
    x, y = 8 + c * (W + 8), 8 + r * (H + lab + 8)
    sheet.paste(Image.open(f).resize((W, H), Image.NEAREST), (x, y + lab))
    d.text((x, y + 2), os.path.basename(f)[:-4], fill=(230, 230, 230), font=font)
sheet.save(os.path.join(out, opt["--sheet"]))
print(f"{len(files)} screens -> {opt['--sheet']}")
