"""Build the voice track and line timings for the one-feature Reels (V11-V18).

usage: build_feature.py <clips dir> [VID ...] [--lines feature_lines.json] [--suffix -hi]
Clips are <VID>_<nn>.mp3, one per line of feature_lines.json. fx:<effect> lines are made here from line <src>
(the Funny Voice playback effects). Writes into cheeko-v2-website/brag-output-2026-09-29-<slug><suffix>/work/:
  vo/vo-tight.wav   the voice track
  timing.js         window.TIMING = {dur, lines: [{s, e, spk, text, show, emoji, hl}]}  (used by compose.html)
  timing.json       the same, for synth.py
"""
import json, subprocess, sys, wave, shutil, argparse
from pathlib import Path
import numpy as np

SR = 44100
TOOLS = Path(__file__).parent
REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
OUTRO_HOLD = 3.4   # seconds after the last line for the price, pill and "send this" to read
TEMPO = {"mitthu": 1.15, "quizzy": 1.08}   # the Qwen voices speak slowly; speed up without changing pitch

ap = argparse.ArgumentParser()
ap.add_argument("clips"); ap.add_argument("vids", nargs="*")
ap.add_argument("--lines", default="feature_lines.json"); ap.add_argument("--suffix", default="")
a = ap.parse_args()
CLIPS = Path(a.clips); J = json.loads((TOOLS / a.lines).read_text())


def load(path, trim=True):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
    if trim:
        env = np.convolve(np.abs(x), np.ones(441) / 441, mode="same"); on = np.nonzero(env > 0.006)[0]
        x = x[max(0, on[0] - int(.03 * SR)): min(len(x), on[-1] + int(.06 * SR))].copy()
    n = int(.008 * SR); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    return x


def ff(x, filt):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", filt,
                        "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], input=(np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes(),
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.int16).astype(float) / 32768


def effect(x, kind):
    """Approximations of the device's five Funny Voice effects, applied to the kid's recording."""
    if kind == "chipmunk": y = ff(x, f"asetrate={int(SR*1.55)},aresample={SR}")
    elif kind == "monster": y = ff(x, f"asetrate={int(SR*0.68)},aresample={SR},lowpass=f=2500")
    elif kind == "robot":
        t = np.arange(len(x)) / SR; y = 0.35 * x + 0.9 * x * np.sin(2 * np.pi * 55 * t); y = ff(y, "acrusher=bits=8:mix=0.3")
    elif kind == "echo": y = ff(np.concatenate([x, np.zeros(int(.9 * SR))]), "aecho=0.8:0.75:220|440:0.5|0.3")
    elif kind == "speedy": y = ff(x, "atempo=1.9")
    else: raise ValueError(kind)
    return y / (np.abs(y).max() + 1e-9) * np.abs(x).max()


for vid, spec in J.items():
    if not vid.startswith("V") or (a.vids and vid not in a.vids): continue
    base = spec.get("dir", f"brag-output-2026-09-29-{spec['slug']}")   # "dir" for videos made on a later day
    work = REPO / f"{base}{a.suffix}" / "work"; (work / "vo/clips").mkdir(parents=True, exist_ok=True)
    clips, out, lines, t = {}, [], [], 0.0
    for i, (spk, emo, text, gap, opt) in enumerate(spec["lines"]):
        if spk.startswith("fx:"):
            y = effect(clips[opt["src"]], spk[3:])
        else:
            src = CLIPS / f"{vid}_{i:02d}.mp3"; y = load(src)
            tempo = {**TEMPO, **spec.get("tempo", {})}   # per-video override, e.g. {"N": 1.1}
            if spk in tempo and tempo[spk] != 1: y = ff(y, f"atempo={tempo[spk]}")
            clips[i] = y
            shutil.copy2(src, work / f"vo/clips/{vid}_{i:02d}.mp3")
        out.append(np.zeros(int(gap * SR))); t += gap
        s = t; out.append(y); t += len(y) / SR
        lines.append({"s": round(s, 3), "e": round(t, 3), "spk": spk, "text": text, "show": opt.get("show", text),
                      "emoji": opt.get("emoji", {}), "hl": opt.get("hl", [])})
    vo = np.concatenate(out); vo = vo / np.abs(vo).max() * .92
    with wave.open(str(work / "vo/vo-tight.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
    timing = {"vid": vid + a.suffix.upper().replace("-", "-"), "dur": round(t + OUTRO_HOLD, 2), "lines": lines}
    (work / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
    (work / "timing.js").write_text("window.TIMING = " + json.dumps(timing, ensure_ascii=False) + ";\n")
    print(vid, spec["slug"], "voice", round(t, 2), "s  video", timing["dur"], "s")
