#!/usr/bin/env python3
"""Write out/index.md from out/shots.tsv (+ a header template)."""
import sys, os
out, header = sys.argv[1], sys.argv[2]
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(out, "shots.tsv")) if l.strip()]
with open(os.path.join(out, "index.md"), "w") as f:
    import re
    here = os.path.dirname(os.path.abspath(header)) + "/.."
    commit = open(os.path.join(here, "gen/commit.txt")).read().strip()[:10] if os.path.exists(os.path.join(here, "gen/commit.txt")) else "?"
    m = re.search(r'set\(PROJECT_VER "([^"]+)"', open(os.path.join(here, "src/CMakeLists.txt")).read())
    f.write(open(header).read().replace("{{COUNT}}", str(len(rows))).replace("{{COMMIT}}", commit).replace("{{VER}}", m.group(1) if m else "?"))
    f.write("\n## Screens\n\nNative 296x240 PNG in this folder; 4x nearest-neighbour copies in `4x/`.\n\n")
    f.write("| File | Group | How it was produced | Notes |\n|---|---|---|---|\n")
    for r in rows:
        r += [""] * (4 - len(r))
        f.write("| `%s` | %s | %s | %s |\n" % (r[0], r[1], r[2].replace("|", "/"), r[3].replace("|", "/")))
print(f"index.md: {len(rows)} screens")
