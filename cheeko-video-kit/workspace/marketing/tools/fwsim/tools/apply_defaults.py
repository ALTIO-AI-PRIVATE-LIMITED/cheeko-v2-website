#!/usr/bin/env python3
"""Build config/sdkconfig.h for the commit being rendered.

Base: config/sdkconfig.base.h (a real cheeko-v2 build's generated header).
On top: the commit's own sdkconfig.defaults(+.esp32s3) for CONFIG_CHEEKO_*,
and CHEEKO_* bools that main/Kconfig.projbuild defaults to y but the base
lacks (new options). Prints what changed so drift is visible."""
import re, sys, os
fw, base, out = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(base).read()
defs = {}
for m in re.finditer(r'^#define (CONFIG_\w+) (.*)$', text, re.M):
    defs[m.group(1)] = m.group(2)
changes = []
over = {}
for f in ("sdkconfig.defaults", "sdkconfig.defaults.esp32s3"):
    p = os.path.join(fw, f)
    if not os.path.exists(p):
        continue
    for ln in open(p):
        m = re.match(r'^(CONFIG_CHEEKO_\w+)=(.*)$', ln.strip())
        if m:
            over[m.group(1)] = m.group(2)
        m = re.match(r'^# (CONFIG_CHEEKO_\w+) is not set', ln.strip())
        if m:
            over[m.group(1)] = "n"
kc = os.path.join(fw, "main", "Kconfig.projbuild")
if os.path.exists(kc):
    cur = None; is_bool = False
    for ln in open(kc):
        m = re.match(r'^\s*config (CHEEKO_\w+)', ln)
        if m:
            cur = "CONFIG_" + m.group(1); is_bool = False; continue
        if cur and re.match(r'^\s*bool', ln):
            is_bool = True
        if cur and is_bool and re.match(r'^\s*default y\s*$', ln):
            if cur not in defs and cur not in over:
                over[cur] = "y"
            cur = None
for k, v in over.items():
    if v == "n":
        if k in defs:
            del defs[k]; changes.append(f"-{k}")
    else:
        nv = "1" if v == "y" else v
        if defs.get(k) != nv:
            defs[k] = nv; changes.append(f"+{k}={nv}")
# rewrite: drop all old CONFIG defines and emit ours
body = re.sub(r'^#define CONFIG_\w+ .*\n', '', text, flags=re.M)
with open(out, "w") as f:
    f.write(body.rstrip() + "\n\n/* fwsim: resolved config */\n")
    for k in sorted(defs):
        f.write(f"#define {k} {defs[k]}\n")
print("config changes vs base:", " ".join(changes) if changes else "(none)")
