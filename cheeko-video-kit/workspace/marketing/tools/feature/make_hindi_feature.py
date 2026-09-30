"""Make the Hindi version of a feature Reel: <dir>-hi/work gets the template, the Hindi voice (build_feature.py
--lines feature_lines_hi.json --suffix -hi) and a spec.js that reuses the English shot list with Hindi on-screen text.
usage: make_hindi_feature.py <slug> [...]"""
import json, re, subprocess, sys
from pathlib import Path

R = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
T = Path(__file__).parent
COMMON = {
    "'8 games 🎮'": "'8 गेम्स 🎮'", "'Animal sounds 🐮'": "'जानवर 🐮'", "'Numbers 🔢'": "'गिनती 🔢'", "'Space 🚀'": "'स्पेस 🚀'", "'Jump 🦘'": "'जंप 🦘'",
    "'Paint 🎨'": "'पेंट 🎨'", "'Trace ✏️'": "'ट्रेस ✏️'", "'Memory 🧠'": "'मेमोरी 🧠'", "'Piano 🎹'": "'पियानो 🎹'",
    "'No<br>ads.'": "'ना<br>ऐड्स।'", "'No in-app<br>purchases.', '#6C3DFF'": "'ऐप में कोई<br>खरीदारी नहीं।', '#6C3DFF', 130", "'Just<br>play! 🎉'": "'बस<br>खेलो! 🎉'",
    "html: 'WARNING <span class=\"e\">⚠️</span>'": "html: 'चेतावनी <span class=\"e\">⚠️</span>'",
    "html: 'Record 10 clips.<br>Play them <span class=\"hl\">forever</span> <span class=\"e\">❤️</span>'": "html: '10 क्लिप रिकॉर्ड करो।<br><span class=\"hl\">हमेशा</span> सुनो <span class=\"e\">❤️</span>'",
    "html: '\"Girgit\" <span class=\"e\">🦎</span><br>= <span class=\"hl\">chameleon</span> <span class=\"e\">✅</span>'": "html: '\"गिरगिट\" <span class=\"e\">🦎</span><br>= <span class=\"hl\">chameleon</span> <span class=\"e\">✅</span>'",
}
OUTRO = {"l1": "कम स्क्रीन।", "l2": 'ज़्यादा <span class="hlb">बचपन।<b></b></span> 🧡', "price": "₹5,999 · डिवाइस + 10 कार्ड", "pill": "लिंक बायो में 👆",
         "send": "ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀"}
OUTRO_TALK = {"l1": "कुछ भी पूछो।", "l2": 'Cheeko से <span class="hlb">पूछो।<b></b></span> 🦊'}
WHO = "{kid: ['🧒 बच्चा', '#FFFFFF', '#6C3DFF'], cheeko: ['🦊 Cheeko', '#FFE3B8', '#F0521D'], nani: ['👵 नानी', '#EBDDFF', '#6C3DFF'], mitthu: ['🦜 मिट्ठू', '#D8F5D0', '#2F6B4F'], quizzy: ['🐝 क्विज़ी', '#FFF1B0', '#231A10'], grandma: ['👵 दादी', '#FFE0EC', '#C2185B']}"

for slug in sys.argv[1:]:
    en = R / f"brag-output-2026-09-29-{slug}/work/spec.js"; name = f"brag-output-2026-09-29-{slug}-hi"
    subprocess.run([str(T / "setup.sh"), name], check=True, capture_output=True)
    s = en.read_text().replace("window.SPEC =", "window.SPEC_EN =", 1)
    for a, b in COMMON.items(): s = s.replace(a, b)
    # Imagine: the firmware shows Hindi text blank, so use the *_hi_* renders and skip the transcript screen (only quote marks)
    s = re.sub(r"imagine_(dosa|peacock|mango)_2_listening_transcript", r"imagine_\1_hi_1_listening", s)
    s = re.sub(r"imagine_(dosa|peacock|mango)_([135])_", r"imagine_\1_hi_\2_", s)
    outro = dict(OUTRO, **(OUTRO_TALK if slug == "talk" else {}))
    s += ("\n// Hindi overrides (make_hindi_feature.py)\nwindow.SPEC = h => { const s = window.SPEC_EN(h); s.outro = Object.assign({}, s.outro || {}, "
          + json.dumps(outro, ensure_ascii=False) + "); s.who = " + WHO + "; return s; };\n")
    (R / name / "work/spec.js").write_text(s)
    print("hindi spec", name)
