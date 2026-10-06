"""Build web assets for the animated 'Meet the device' section on cheekoai.in.

Outputs into cheeko-v2-website/assets/img/device-v2/web/:
  cheeko-front.webp  new yellow render, TALK menu (current firmware) baked into the screen
  knob.webp          the rotary dial as its own disc (alpha), so CSS can rotate it
  menu-*.webp        the six main-menu screens from the firmware renders
  screen-mask.png    alpha mask for the rounded screen glass
Prints geometry (fractions of the front render) for the CSS/JS.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json, numpy as np

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "cheeko-v2-website"
DEV = SITE / "assets/img/device-v2"
FW4X = ROOT / "marketing/tools/fwsim/out/4x"
OUT = DEV / "web"
OUT.mkdir(exist_ok=True)

WIDTH = 1000                     # web width of the device image
KNOB = (0.490, 0.571)            # dial centre, fraction of width / height
KNOB_R = 0.191                   # disc radius, fraction of width (sits on the dark well ring)
MENU = ["1_talk", "2_imagine", "3_games", "4_funny_voice", "5_radio", "6_settings"]
# firmware theme for the screens: "" = Sunny (cream, the default), "theme1_" = Night (black),
# "theme2_" = Ocean, "theme3_" = Candy. Ravi chose Night for the website (2026-09-30).
THEME = "theme1_"

geo = json.loads((DEV / "geometry.json").read_text())
full = Image.open(DEV / "full/yellow_front.png").convert("RGBA")
H = round(WIDTH * full.height / full.width)
dev = full.resize((WIDTH, H), Image.LANCZOS)

s = geo["screen"]
box = (round(s["left"] * WIDTH), round(s["top"] * H),
       round((s["left"] + s["width"]) * WIDTH), round((s["top"] + s["height"]) * H))
bw, bh = box[2] - box[0], box[3] - box[1]
mask = Image.open(DEV / "screen_mask.png").getchannel("A").resize((bw, bh), Image.LANCZOS)

def screen(name, w, h):
    return Image.open(FW4X / f"{THEME}01_menu_{name}_4x.png").convert("RGBA").resize((w, h), Image.LANCZOS)

# base: bake the current TALK screen in, so no-JS / first paint never shows the old dark UI
dev.paste(screen(MENU[0], bw, bh), box[:2], mask)
dev.save(OUT / "cheeko-front.webp", quality=90, method=6)

# screens at 2x of the largest on-page size (~300 css px wide)
for n in MENU:
    screen(n, 600, round(600 / s["aspect"])).save(OUT / f"menu-{n.split('_', 1)[1]}.webp", quality=90, method=6)
# CSS masks read ALPHA, so the mask must be white + alpha, not greyscale
m600 = mask.resize((600, round(600 / s["aspect"])), Image.LANCZOS)
rgba = Image.new("RGBA", m600.size, (255, 255, 255, 0)); rgba.putalpha(m600)
rgba.save(OUT / "screen-mask.png")

# dial disc from the full-res render, feathered circular alpha
FW, FH = full.size
cx, cy, r = KNOB[0] * FW, KNOB[1] * FH, KNOB_R * FW
disc = full.crop((round(cx - r), round(cy - r), round(cx + r), round(cy + r)))
ss = 4
m = Image.new("L", (disc.width * ss, disc.height * ss), 0)
ImageDraw.Draw(m).ellipse((ss, ss, disc.width * ss - ss, disc.height * ss - ss), fill=255)
m = m.resize(disc.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
disc.putalpha(m)
d = round(2 * KNOB_R * WIDTH * 1.5)          # 1.5x the base scale, stays crisp on retina
disc.resize((d, d), Image.LANCZOS).save(OUT / "knob.webp", quality=92, method=6)

# left / right body edge at given heights, for arrow targets
a = np.asarray(dev.getchannel("A"))
def edges(fy):
    row = np.nonzero(a[round(fy * H)] > 128)[0]
    return round(row[0] / WIDTH, 4), round(row[-1] / WIDTH, 4)
top_row = np.nonzero(a[:, round(0.55 * WIDTH)] > 128)[0][0] / H
print(json.dumps({
    "size": [WIDTH, H], "screen": s, "knob": [*KNOB, KNOB_R],
    "usbc_y.325": edges(0.325), "jack_y.51": edges(0.51), "buttons_y.33": edges(0.33),
    "speaker_y.84": edges(0.84), "top_at_x.55": round(top_row, 4),
}, indent=1))
