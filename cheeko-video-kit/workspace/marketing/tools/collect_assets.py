"""Collect every marketing-usable asset from the Cheeko repos into Drive "cheeko ai videos/01 Shared assets".

Media only (images, audio, video, fonts, PDFs) — never code, configs or keys. Small resized duplicates
(-800, -m, -s) are skipped. Other companies' logos, admin-dashboard art and upstream picoclaw images are skipped.
Writes MANIFEST.csv (destination, source repo path, bytes) next to the folders. Safe to re-run.
"""
import csv, re, shutil, subprocess
from pathlib import Path

ROOT = Path("/Users/ravikumar/Cheeko Master")
WEB = ROOT / "cheeko-v2-website/assets"
FW = ROOT / "cheeko-os-v2"
APP = ROOT / "CheekoAI-Parent-App"
OUT = Path.home() / "Library/CloudStorage/GoogleDrive-ravi.ramp36@gmail.com/My Drive/cheeko ai videos/01 Shared assets"
MEDIA = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".mov", ".mp3", ".wav", ".ogg", ".m4a", ".ttf", ".otf", ".pdf"}
SMALL_DUP = re.compile(r"-(800|m|s)$")

rows = []


def put(src: Path, dest_dir: str, name: str | None = None):
    if src.suffix.lower() not in MEDIA or not src.is_file():
        return
    d = OUT / dest_dir
    d.mkdir(parents=True, exist_ok=True)
    dst = d / (name or src.name)
    shutil.copy2(src, dst)
    rows.append((str(dst.relative_to(OUT)), str(src.relative_to(ROOT)), src.stat().st_size))


def put_tree(src_dir: Path, dest_dir: str, flatten_prefix=False):
    for f in sorted(src_dir.rglob("*")):
        if f.is_file():
            rel = f.relative_to(src_dir)
            sub = str(rel.parent) if str(rel.parent) != "." else ""
            put(f, f"{dest_dir}/{sub}".rstrip("/"))


# ---------- website ----------
def web_category(name: str, live: bool) -> str | None:
    stem = Path(name).stem
    if SMALL_DUP.search(stem):
        return None
    if live:
        if stem.startswith("card-") or stem.startswith("next-drop"):
            return "Old website cards (DO NOT USE - not shipping)"
        if stem.startswith("char-"):
            return "Characters/Website art"
        if stem.startswith("im-") or stem.startswith("imagine-"):
            return "Imagine drawings/Website"
        if stem.startswith("menu-") or stem.startswith("screen-"):
            return "Device screens/Website menu art and screen photos"
        if stem.startswith(("studio-", "device-")) or stem in ("og", "funny-voice-pink"):
            return "Device/Product photos"
        if stem == "s2-manage-content":
            return "Parent app/Website screenshot"
        return "Photos/Kids and families (Bengaluru shoot)"
    if stem.startswith("card_"):
        return "Old website cards (DO NOT USE - not shipping)"
    if stem.startswith(("device", "colour")) or stem in ("hero", "hero_v2", "hero_mobile"):
        return "Device/Renders and colourways"
    if stem.startswith(("problem", "phone_problem")):
        return "Photos/Phone problem scenes"
    if stem in ("logo",):
        return "Brand/Logo"
    if stem in ("fox", "askcheeko"):
        return "Characters/Website art"
    if stem == "parent_app":
        return "Parent app/Website screenshot"
    if name.endswith(".pdf"):
        return "Docs"
    return "Worlds and backgrounds"


for f in sorted((WEB / "img").iterdir()):
    if f.is_file():
        c = web_category(f.name, live=False)
        if c: put(f, c)
for f in sorted((WEB / "img/live").iterdir()):
    c = web_category(f.name, live=True)
    if c: put(f, c)
put_tree(WEB / "img/imagine", "Imagine drawings/Website")
put_tree(WEB / "img/partners", "Brand/Partner logos (Backed by)")
put_tree(WEB / "fonts", "Brand/Fonts")
put_tree(WEB / "vid", "Videos/Website")
put(WEB / "img/device_live_screen_mask.png", "Device", "device screen mask.png")

# ---------- firmware (cheeko-os-v2, branch fix/quizzy-field-fixes) ----------
H = FW / "design_handoff_cheeko_os_1b"
# Ravi, 2026-09-28: the design-handoff screenshots are the OLD UI, not what ships. Kept only in a do-not-use folder.
put_tree(H / "screenshots", "Old UI (DO NOT USE - not current)/Cheeko OS screenshots (July 2026 design handoff)")
put_tree(H / "icons", "Old UI (DO NOT USE - not current)/Cheeko OS icons (July 2026 design handoff)")
SD = FW / "CHEEKO_SD_CARD_COPY/cheeko"
# The on-device art ships only as LVGL v9 .bin (RGB565 = cf 0x12, RGB565 + A8 plane = cf 0x14); decode to PNG.
LVGL_DEST = {"chars": "Characters/On-device art (connect, listen, think, talk)", "heroes": "Device screens/On-device hero art",
             "menu": "Device screens/On-device menu art", "wall": "Device screens/Wallpapers (time of day)",
             "voices": "Device screens/Funny Voice icons", "themes": "Device screens/Themes (Dinku dino, Robu robot)"}


def lvgl_to_png(f: Path, dst: Path):
    import struct, numpy as np
    from PIL import Image
    b = f.read_bytes(); cf = b[1]; w, h, stride = struct.unpack("<HHH", b[4:10]); d = b[12:]
    px = np.frombuffer(d[:h*stride], dtype="<u2").reshape(h, stride//2)[:, :w]
    rgb = np.dstack([((px >> 11) & 31)*255//31, ((px >> 5) & 63)*255//63, (px & 31)*255//31]).astype(np.uint8)
    if cf == 0x14:
        a = np.frombuffer(d[h*stride:h*stride + w*h], dtype=np.uint8).reshape(h, w)
        Image.fromarray(np.dstack([rgb, a]), "RGBA").save(dst)
    else:
        Image.fromarray(rgb, "RGB").save(dst)


for f in sorted(SD.rglob("*.bin")):
    rel = f.relative_to(SD); top = rel.parts[0]
    if top not in LVGL_DEST: continue
    d = OUT / LVGL_DEST[top] / Path(*rel.parts[1:-1]); d.mkdir(parents=True, exist_ok=True)
    dst = d / (f.stem + ".png"); lvgl_to_png(f, dst)
    rows.append((str(dst.relative_to(OUT)), str(f.relative_to(ROOT)) + " (decoded from LVGL .bin)", dst.stat().st_size))
put_tree(FW / "art", "Old UI (DO NOT USE - not current)/Art research (July 2026 - incl. unused mascots Sheru, Toffee)")
put_tree(SD / "assets/animals", "Sounds/Animal sounds and pictures")
put_tree(SD / "assets/animal_cards", "Sounds/Animal sounds and pictures/cards")
put_tree(FW / "sd_card_assets/cheeko/apps/hometown", "Sounds/Sounds Around Me game (cooker, doorbell, ...)")
put_tree(FW / "main/assets/common", "Sounds/Device UI sounds (boot, card insert, knob, charging)")
put_tree(FW / "main/assets/locales/en-US", "Sounds/Device voice prompts/English")
put_tree(FW / "main/assets/locales/hi-IN", "Sounds/Device voice prompts/Hindi")

# ---------- parent app (CheekoAI-Parent-App, branch feat/daily-streak) ----------
A = APP / "assets"
put_tree(A / "Cheeko_PlayStore_Ready_1080x1920", "Parent app/Store screenshots/Play Store 1080x1920")
put_tree(A / "Cheeko_AppStore_Ready_1284x2778", "Parent app/Store screenshots/App Store 1284x2778")
put_tree(A / "Cheeko_iPad_Ready_2064x2752", "Parent app/Store screenshots/iPad 2064x2752")
put_tree(A / "images/onboarding_tour", "Parent app/Onboarding tour")
for f in sorted((A / "images").glob("*")):
    if f.is_file(): put(f, "Parent app/Illustrations")
put_tree(A / "icons/characters", "Characters/Parent app icons")
for f in sorted((A / "icons").glob("*")):
    if f.is_file() and f.stem not in ("apple_logo", "google_logo"):
        put(f, "Parent app/Icons")
put(A / "icon/icon.png", "Brand/Logo", "parent-app-icon.png")
put(A / "icon/icon_foreground.png", "Brand/Logo", "parent-app-icon-foreground.png")
put(A / "videos/animated-logo.gif", "Brand/Logo", "animated-logo.gif")
put_tree(A / "fonts", "Brand/Fonts")
put_tree(APP / "design", "Parent app/Design concepts")

# ---------- docs ----------
put(ROOT / "tender/Cheeko_Technical_Specifications_Tender.pdf", "Docs")

with open(OUT / "MANIFEST.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["file", "source", "bytes"]); w.writerows(sorted(rows))
total = sum(r[2] for r in rows)
print(f"{len(rows)} files, {total/1e6:.1f} MB")
