"""Put frames on the real device: the new-design Cheeko (yellow front) with each frame clipped by the glass mask.
Usage: python3 mock.py out.png still-a.png [still-b.png ...]  (tiles several mocks side by side)"""
import sys, json
from PIL import Image
IMG = '/Users/ravikumar/Cheeko Master/cheeko-v2-website/assets/img/device-v2/'
G = json.load(open(IMG + 'geometry.json'))
dev = Image.open(IMG + 'yellow_front.png').convert('RGBA'); W, H = dev.size
sx, sy = int(G['screen']['left'] * W), int(G['screen']['top'] * H); sw, sh = int(G['screen']['width'] * W), int(G['screen']['height'] * H)
mask = Image.open(IMG + 'screen_mask.png').split()[-1].resize((sw, sh), Image.LANCZOS)
out = []
for f in sys.argv[2:]:
    d = dev.copy(); fr = Image.open(f).convert('RGBA').resize((sw, sh), Image.LANCZOS)
    d.paste(fr, (sx, sy), mask); d = d.crop((0, 0, W, int(H * .5))); d.thumbnail((700, 700)); out.append(d)
T = Image.new('RGBA', (sum(o.width for o in out) + 10 * (len(out) - 1), max(o.height for o in out)), (235, 235, 235, 255)); x = 0
for o in out: T.alpha_composite(o, (x, 0)); x += o.width + 10
T.convert('RGB').save(sys.argv[1]); print(sys.argv[1], T.size)
