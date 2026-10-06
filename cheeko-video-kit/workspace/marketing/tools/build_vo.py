"""Assemble per-line voice clips into one voiceover per video and write the time-warp anchors.

Input: vo_lines.json (lines with emotion, old start time, gap) and clips <VID>_<nn>.mp3 in CLIPS.
Output per video (in <repo dir>/work/): vo/vo-tight.wav (the new VO; the previous one is kept as
vo/vo-tight-previous.wav once) and warp.json = {"new": [...], "old": [...], "dur": new_duration}.
compose.html and synth.py map every scene/SFX time through these anchors, so the video follows the new voice.
"""
import json, os, subprocess, sys, wave, shutil
from pathlib import Path
import numpy as np

SR = 44100
TOOLS = Path(__file__).parent
REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
# usage: build_vo.py <clips dir> [lines json] [dir suffix]   e.g. build_vo.py clips vo_lines_hi.json -hi
CLIPS = Path(sys.argv[1])
J = json.loads((TOOLS / (sys.argv[2] if len(sys.argv) > 2 else "vo_lines.json")).read_text())
SUFFIX = sys.argv[3] if len(sys.argv) > 3 else ""


def load_trimmed(mp3, tempo=1.0):
    af = ["-af", f"atempo={tempo}"] if tempo != 1.0 else []
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", str(mp3), *af, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"])
    x = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
    env = np.convolve(np.abs(x), np.ones(441) / 441, mode="same")
    on = np.nonzero(env > 0.006)[0]
    a, b = max(0, on[0] - int(.03 * SR)), min(len(x), on[-1] + int(.06 * SR))
    y = x[a:b].copy(); n = int(.008 * SR); y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n)
    return y


# VIDS=V06 limits the run to some videos (default: the Reels re-voiced on 2026-09-28)
for vid in (os.environ["VIDS"].split(",") if os.environ.get("VIDS") else ("V03", "V04", "V05")):
    spec = J[vid]; work = REPO / (spec["dir"] + SUFFIX) / "work"
    out, t, new, old = [], 0.0, [], []
    for i, line in enumerate(spec["lines"]):
        old_t, gap = line[-2], line[-1]
        # optional "tempo" speeds up the main voice; lines with their own voice (e.g. Nani) keep theirs
        tempo = spec.get("voices_tempo", 1.0) if str(i) in spec.get("voices", {}) else spec.get("tempo", 1.0)   # voices_tempo: other characters (default: natural speed)
        y = load_trimmed(CLIPS / f"{vid}_{i:02d}.mp3", tempo)
        out.append(np.zeros(int(gap * SR))); t += gap
        new.append(round(t, 3)); old.append(old_t)
        out.append(y); t += len(y) / SR
    vo = np.concatenate(out); vo = vo / np.abs(vo).max() * .92
    new.append(round(t, 3)); old.append(spec["old_vo_end"])
    dur = round(t + (spec["old_dur"] - spec["old_vo_end"]), 2)
    new.append(dur); old.append(spec["old_dur"])
    prev = work / "vo/vo-tight-previous.wav"
    if not prev.exists() and (work / "vo/vo-tight.wav").exists(): shutil.copy2(work / "vo/vo-tight.wav", prev)
    with wave.open(str(work / "vo/vo-tight.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((vo * 32767).astype(np.int16).tobytes())
    (work / "warp.json").write_text(json.dumps({"new": new, "old": old, "dur": dur}))
    (work / "vo/clips").mkdir(exist_ok=True)
    for i in range(len(spec["lines"])): shutil.copy2(CLIPS / f"{vid}_{i:02d}.mp3", work / f"vo/clips/{vid}_{i:02d}.mp3")
    print(vid, "VO", round(t, 2), "s  video", dur, "s  (was", spec["old_dur"], ")")
