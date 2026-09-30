"""Build the portable Cheeko Video Kit: skills, tools, docs, every video's source and the core assets, laid out
exactly like "Cheeko Master" (under workspace/) so every path in the docs and scripts still lines up.

    python3 make_video_kit.py            -> marketing/cheeko-video-kit/  + cheeko-video-kit.zip
                                            + cheeko-video-kit-extra-assets.zip (big, optional images)
No API keys are copied: voice recording reads keys from environment variables (tools/voice/rec_anywhere.py).
The hand-written kit docs (START-HERE.md, AGENTS.md, CLAUDE.md, setup.sh) live in tools/kit/ and are copied in.
"""
from pathlib import Path
import os, re, shutil, subprocess, zipfile

ROOT = Path("/Users/ravikumar/Cheeko Master")
SITE, MKT, TOOLS = ROOT / "cheeko-v2-website", ROOT / "marketing", ROOT / "marketing/tools"
DRIVE_PLAN = Path.home() / "Library/CloudStorage/GoogleDrive-ravi.ramp36@gmail.com/My Drive/cheeko ai videos/00 Plan"
MEM = Path.home() / ".claude/projects/-Users-ravikumar-Cheeko-Master/memory"
OUT = MKT / "cheeko-video-kit"
WS = OUT / "workspace"
TEXT = {".html", ".js", ".mjs", ".py", ".json", ".md", ".txt", ".sh", ".css", ".csv"}
SKIP_DIRS = {"node_modules", "__pycache__", ".venv", ".git"}
# decisions Ravi made, kept as memory notes; none of these hold keys or passwords
DECISIONS = ["cheeko-marketing-videos", "feedback-video-style", "cheeko-shipping-cards", "cheeko-new-design-2026-09",
             "cheeko-sticker-ad", "cheeko-bachpan-film", "cheeko-device-modes", "envato-mcp", "cheeko-certification-positioning"]
PORTABLE_NOTE = """

## Using this skill outside Ravi's Mac (Cheeko Video Kit)

- Paths above that start with `/Users/ravikumar/Cheeko Master` mean the kit's `workspace/` folder (`bash setup.sh` rewrites them).
- The dev box and its recorders (`vo_rec.py`, `feature_rec.py`) are not available. Record with `workspace/marketing/tools/voice/rec_anywhere.py`, which takes `MINIMAX_API_KEY`, `QWEN_API_KEY` and `SARVAM_API_KEY` from environment variables.
- Google Drive publishing, the master sheet and the team page only work on Ravi's Mac. Hand over the finished video, thumbnail and caption instead.
- The render scripts are in `scripts/` next to this file (`render.mjs`, `stills.mjs`, `sheet.py`, `finish.sh`, `pw.mjs`).
"""
SECRET = re.compile(r"(sk-[A-Za-z0-9]{16,}|sk-ws-[A-Za-z0-9]{8,}|Bearer [A-Za-z0-9._\-]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}"
                    r"|api[_-]?key\s*[=:]\s*['\"][A-Za-z0-9_\-]{12,}|password\s*[=:]\s*['\"][^'\"]{4,})", re.I)


def copy(src, dst, text_only=False, skip=()):
    src, dst = Path(src), Path(dst)
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); return
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        if not p.is_file() or SKIP_DIRS & set(rel.parts) or any(str(rel).startswith(s) for s in skip):
            continue
        if text_only and p.suffix.lower() not in TEXT:
            continue
        q = dst / rel; q.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, q)


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    # kit front door
    copy(TOOLS / "kit", OUT)
    # skills to install (user level) + the website's project skills stay inside the repo copy
    copy(Path.home() / ".claude/skills/cheeko-video", OUT / "skills/cheeko-video")
    copy(SITE / ".claude/skills/cheeko-video/scripts", OUT / "skills/cheeko-video/scripts")
    with open(OUT / "skills/cheeko-video/SKILL.md", "a") as f:
        f.write(PORTABLE_NOTE)
    copy(SITE / ".claude/skills/brag-slim", OUT / "skills/brag-slim")
    copy(SITE / ".claude/skills", WS / "cheeko-v2-website/.claude/skills")
    # docs
    for f in DRIVE_PLAN.glob("*"):
        if f.is_file() and f.suffix in {".md", ".csv"}:
            copy(f, OUT / "docs/plan" / f.name)
    for n in DECISIONS:
        if (MEM / f"{n}.md").exists():
            copy(MEM / f"{n}.md", OUT / "docs/decisions" / f"{n}.md")
    # marketing: plans, tools (no firmware copies or build output), web components
    for f in MKT.glob("*.md"):
        copy(f, WS / "marketing" / f.name)
    copy(TOOLS, WS / "marketing/tools", skip=("fwsim/deps", "fwsim/build", "fwsim/src", "fwsim/out", "fwsim/sdcard", "kit"))
    copy(MKT / "web-components/cheeko-device-animation", WS / "marketing/web-components/cheeko-device-animation")
    # website: every video's source (text only), thumbnail tools, core assets
    for d in sorted(SITE.glob("brag-output*")):
        copy(d, WS / "cheeko-v2-website" / d.name, text_only=True)
    for f in ["make_dev_v2.py", "make_thumbs.mjs", "make_thumbs_feature.mjs", "thumb.html"]:
        copy(SITE / "thumbs-work" / f, WS / "cheeko-v2-website/thumbs-work" / f)
    # thumbs-work/dev (old device) is retired; dev2/ is rebuilt by make_dev_v2.py from the extra assets
    img = SITE / "assets/img"
    for d in ["fw-screens", "cards-shipping", "myo", "app"]:
        copy(img / d, WS / "cheeko-v2-website/assets/img" / d)
    copy(img / "device-v2", WS / "cheeko-v2-website/assets/img/device-v2", skip=("full",))
    for f in ["device_current.png", "device_live_screen_mask.png"]:
        copy(img / f, WS / "cheeko-v2-website/assets/img" / f)
    copy(SITE / "server.py", WS / "cheeko-v2-website/server.py")
    # real Cheeko sounds (card insert, knob click...) read by the feature template's synth.py
    copy(ROOT / "cheeko-os-v2/main/assets/common", WS / "cheeko-os-v2/main/assets/common")

    # safety: refuse to ship anything that looks like a key or password
    hits = [str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file() and p.suffix in TEXT
            and SECRET.search(p.read_text(errors="ignore"))]
    if hits:
        raise SystemExit("Possible secrets, not zipping:\n  " + "\n  ".join(hits))


def zipdir(src_dirs, zpath, arc_root):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for src, arc in src_dirs:
            for p in sorted(Path(src).rglob("*")):
                if p.is_file() and p.name != ".DS_Store":
                    z.write(p, f"{arc_root}/{arc}/{p.relative_to(src)}" if arc else f"{arc_root}/{p.relative_to(src)}")


if __name__ == "__main__":
    build()
    for p in (OUT / "setup.sh",):
        os.chmod(p, 0o755)
    zipdir([(OUT, "")], MKT / "cheeko-video-kit.zip", "cheeko-video-kit")
    img = SITE / "assets/img"
    zipdir([(img / "device-v2/full", "workspace/cheeko-v2-website/assets/img/device-v2/full"),
            (img / "app-shots-ios", "workspace/cheeko-v2-website/assets/img/app-shots-ios"),
            (img / "app-shots", "workspace/cheeko-v2-website/assets/img/app-shots")],
           MKT / "cheeko-video-kit-extra-assets.zip", "cheeko-video-kit")
    for z in ("cheeko-video-kit.zip", "cheeko-video-kit-extra-assets.zip"):
        print(z, round((MKT / z).stat().st_size / 1e6, 1), "MB")
    print(subprocess.run(["du", "-sh", str(OUT)], capture_output=True, text=True).stdout.strip())
