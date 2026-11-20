"""Tile stills into one labelled sheet: python3 sheet_stills.py <out.jpg> <png>...  (label = time from the file name)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
out, fs = sys.argv[1], sys.argv[2:]; W, H, c = 296, 240, 6
f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 14)
S = Image.new('RGB', (c * (W + 6), ((len(fs) + c - 1) // c) * (H + 22)), (25, 25, 25)); d = ImageDraw.Draw(S)
for i, p in enumerate(fs):
    im = Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS); x, y = (i % c) * (W + 6), (i // c) * (H + 22)
    S.paste(im, (x, y + 20)); d.text((x + 4, y + 2), os.path.basename(p)[:-4], fill=(255, 230, 0), font=f)
S.save(out, quality=88)
