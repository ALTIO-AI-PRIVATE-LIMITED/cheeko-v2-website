"""Tile still-*.png (time order) into review.png, 5 per row, for quick scene review.
Usage (inside work/): LABELS='1 Hook,2 ...' ../../.venv/bin/python review_sheet.py [cols] [width]"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
files = sorted(glob.glob('still-*.png'), key=lambda f: float(f[6:-4]))
cols = int(sys.argv[1]) if len(sys.argv) > 1 else 5
w = int(sys.argv[2]) if len(sys.argv) > 2 else 432
h = w * 16 // 9; g = 16; rows = -(-len(files) // cols)
labels = os.environ.get('LABELS', '').split(',') if os.environ.get('LABELS') else [f'Scene {k + 1}' for k in range(len(files))]
sheet = Image.new('RGB', (cols * (w + g) + g, rows * (h + g + 44) + g), (30, 30, 30))
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
except OSError: font = ImageFont.load_default()
for k, f in enumerate(files):
    x, y = g + (k % cols) * (w + g), g + (k // cols) * (h + g + 44)
    sheet.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 44))
    d.text((x, y + 6), labels[k] if k < len(labels) else '', fill=(255, 255, 255), font=font)
sheet.save('review.png'); print(len(files), sheet.size)
