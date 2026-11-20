"""Device images for thumbnails, new Cheeko design (Sep 2026): the trimmed front render with a real firmware screen in
the measured screen mask (assets/img/device-v2/screen_mask.png, geometry.json). Writes dev2/<name>.png and
dev2/<name>_pink.png / _white.png (yellow is the default). Cheeko's screen is the dark Night theme (fwsim theme1_* renders, Ravi
2026-09-30: every device screen black); <name>_light*.png keep the light Sunny screen. assets/img/device-v2/screens/ is a copy of dev2/.
usage: make_dev_v2.py"""
import json
from pathlib import Path
from PIL import Image, ImageOps

A = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website/assets/img"); OUT = Path(__file__).parent / "dev2"; OUT.mkdir(exist_ok=True)
G = json.loads((A / "device-v2/geometry.json").read_text())["screen"]; MASK = Image.open(A / "device-v2/screen_mask.png").getchannel("A")   # the mask is the alpha channel
SCREENS = {"code": "setup_7_activation_code", "funny": "07_funny_voice_1_chipmunk", "games": "04_games_menu_1_animal", "grandma": "content_play_3_item1",
           "imagine": "imagine_dosa_5_result", "mitthu": "card_mitthu_6_talking", "nani": "03_talk_4_nani_6_talking", "quizzy": "card_quizzy_6_talking",
           "talk": "03_talk_1_cheeko_6_talking", "tutorial": "16_onboarding_1_intro", "home": "00_home_clock", "menu": "01_menu_1_talk"}
ART = {"myo": "myo/peacock.png"}   # pictures that are not firmware renders (a custom card recording's picture): cropped, never stretched
for k, v in list(SCREENS.items()):   # Night by default, the light screen as <name>_light
    if (A / f"fw-screens/theme1_{v}.png").exists(): SCREENS[k + "_light"], SCREENS[k] = v, "theme1_" + v
for colour in ("yellow", "pink", "white"):
    base = Image.open(A / f"device-v2/full/{colour}_front.png").convert("RGBA"); W, H = base.size; x0, y0 = round(G["left"] * W), round(G["top"] * H)
    for name, scr in {**SCREENS, **ART}.items():
        f = A / (scr if name in ART else f"fw-screens/{scr}.png")
        if not f.exists(): print("missing", scr); continue
        src = Image.open(f).convert("RGBA")
        s = ImageOps.fit(src, MASK.size, Image.LANCZOS, centering=(.5, .12)) if name in ART else src.resize(MASK.size, Image.LANCZOS)
        im = base.copy(); im.paste(s, (x0, y0), MASK)
        im.thumbnail((1000, 2000), Image.LANCZOS); im.save(OUT / f"{name}{'' if colour == 'yellow' else '_' + colour}.png", optimize=True)
import shutil
for p in OUT.glob("*.png"): shutil.copy(p, A / "device-v2/screens" / p.name)
print(sorted(p.name for p in OUT.iterdir()))
