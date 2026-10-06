"""Stitch a series of vertical parts into one film: vertical (1080x1920) and 16:9 (1920x1080, the vertical video in the
middle with a Cheeko frame: title on the left, chapter list on the right, current chapter lit).

usage: stitch_series.py <config.json>
config: {"out": "brag-output-...-full", "parts": ["brag-output-...-app-home", ...], "chapters": [...], "title", "sub", "pill",
         "hook", "thumbPill", "thumbShots": [3 app-shot paths], "hi": 0|1, "tail": 1.2}
Each part except the last is cut `tail` seconds after its last voice line (its "Next" card stays on screen that long);
the last part plays to the end. Parts are joined with short audio fades so the music restarts cleanly.
"""
import html, json, subprocess, sys
from pathlib import Path

REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website"); HERE = Path(__file__).parent
C = json.loads(Path(sys.argv[1]).read_text()); OUT = REPO / C["out"]; W = OUT / "work"; W.mkdir(parents=True, exist_ok=True)
run = lambda *a: subprocess.run([str(x) for x in a], check=True)
FF = ["ffmpeg", "-y", "-loglevel", "error"]
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]

run("node", HERE / "stitch/frames.mjs", sys.argv[1], W)
segs, segs16, marks, t = [], [], [], 0.0
for k, p in enumerate(C["parts"]):
    tm = json.loads((REPO / p / "work/timing.json").read_text())
    end = tm["dur"] if k == len(C["parts"]) - 1 else round(tm["lines"][-1]["e"] + C.get("tail", 1.2), 2)
    s, s16 = W / f"seg_{k}.mp4", W / f"seg16_{k}.mp4"
    run(*FF, "-i", REPO / p / "brag.mp4", "-t", end, "-af", f"afade=t=in:d=0.06,afade=t=out:st={end - .3:.2f}:d=0.3", *ENC, s)
    run(*FF, "-loop", "1", "-i", W / f"ch_{k}.png", "-i", s, "-filter_complex",
        "[1:v]scale=608:1080[v];[0:v][v]overlay=656:0:shortest=1,format=yuv420p[o]", "-map", "[o]", "-map", "1:a", *ENC, s16)
    segs.append(s); segs16.append(s16); marks.append((round(t, 2), html.unescape(C["chapters"][k]))); t += end
for lst, name in ((segs, "brag.mp4"), (segs16, "brag-16x9.mp4")):
    (W / "list.txt").write_text("".join(f"file '{x}'\n" for x in lst))
    run(*FF, "-f", "concat", "-safe", "0", "-i", W / "list.txt", "-c", "copy", "-movflags", "+faststart", OUT / name)
run(*FF, "-ss", "3", "-i", OUT / "brag.mp4", "-frames:v", "1", "-q:v", "3", OUT / "brag.jpg")
(OUT / "work/chapters.txt").write_text("".join(f"{int(a // 60)}:{int(a % 60):02d} {c}\n" for a, c in marks))   # YouTube chapter list
(OUT / "work/stitch.json").write_text(json.dumps(C, ensure_ascii=False, indent=1))
print(OUT, round(t, 2), "s"); print((OUT / "work/chapters.txt").read_text())
