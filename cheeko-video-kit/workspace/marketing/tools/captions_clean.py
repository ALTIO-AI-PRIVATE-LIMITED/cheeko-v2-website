"""Clean the on-screen text of the Reel compositions and add emojis to the word captions.

Ravi, 2026-09-28: no em dashes, no "…", no curly quotes anywhere people can read (they read as AI-written),
and use emojis to make the captions more fun. Emojis go on screen only, never in the voice text.

Usage: python captions_clean.py            # English compositions (V01-V05)
       make_hindi.py imports add_emojis() for the Hindi ones.
"""
import json, re
from pathlib import Path

REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
EMOJI = {  # normalised word -> emoji shown right after it (once per caption line, after the last match)
    "tantrum": "😳", "cheeko": "🦊", "time": "📖", "back": "🗣️", "languages": "💬", "tiger": "🐯", "bicycle": "🚲",
    "boom": "💥", "draws": "🎨", "end": "📱", "scroll": "😵", "playing": "🧸", "sleep": "😴", "itself": "🌙", "stop": "✋",
    "sound": "👂", "card": "🎴", "whistle": "♨️", "doorbell": "🔔", "nani": "👵", "listens": "💛", "rickshaw": "🛺",
    "moon": "🌙", "english": "🙌", "parents": "🧡",
    # Hindi
    "नहीं": "😳", "शुरू": "📖", "जवाब": "🗣️", "भाषाएँ": "💬", "तैयार": "🎨", "ख़त्म": "📱", "सो": "😴", "आप": "🌙",
    "सिखाती": "✋", "पहचानो": "👂", "कार्ड": "🎴", "सीटी": "♨️", "घंटी": "🔔", "नानी": "👵", "सुनती": "💛", "इंग्लिश": "🙌",
    "बनाया": "🧡", "खेल": "🧸", "स्क्रोल": "😵", "टाइगर": "🐯", "साइकिल": "🚲", "रिक्शा": "🛺", "चाँद": "🌙",
}
PUNCT = ",.!?।:;\"'"


def norm(w):
    return w.strip(PUNCT).lower()


def add_emojis(caps):
    """caps: [[start, end, [[word, t, (hl)], ...]], ...] -> same with emoji tokens inserted."""
    for c in caps:
        words, seen = c[2], {}
        for i, w in enumerate(words):
            k = norm(w[0])
            if k in EMOJI: seen[k] = i
        for k, i in sorted(seen.items(), key=lambda kv: -kv[1]):
            e = EMOJI[k]
            if i == 0 and len(words) > 1 and k not in ("nani", "नानी"): continue   # never on a line's first word
            if any(x[0] == e for x in words): continue
            words.insert(i + 1, [e, round(words[i][1] + .12, 2)])
    return caps


def clean_word(w, last):
    w = w.replace("“", "").replace("”", "").replace("’", "'").replace("‘", "'")
    if w.endswith("…"):
        w = w[:-1] + ("" if last else ",")
    return w.replace("…", "")


def js_to_caps(block):
    j = re.sub(r"'((?:[^'\\]|\\.)*)'", lambda m: json.dumps(m.group(1), ensure_ascii=False), block)
    j = re.sub(r"(?<![0-9])\.([0-9])", r"0.\1", j)
    j = re.sub(r",\s*\]", "]", j).rstrip().rstrip(",")
    return json.loads("[" + j + "]")


CSS_EMO = "#caps .w.emo{-webkit-text-stroke:0;text-shadow:none;background:none;box-shadow:none;transform-origin:50% 60%}"
JS_EMO_OLD = "const s = document.createElement('span'); s.className = 'w' + (hl ? ' hl' : '');"
JS_EMO_NEW = ("const s = document.createElement('span'); const emo = /\\p{Extended_Pictographic}/u.test(w) && !/[\\p{L}\\p{N}]/u.test(w);"
              " s.className = 'w' + (emo ? ' emo' : hl ? ' hl' : '');")


def process(path: Path, fixed_text=()):
    s = path.read_text()
    m = re.search(r"const CAPS = \[\n(.*?)\n\];", s, re.S)
    if m:
        caps = js_to_caps(m.group(1))
        for c in caps:
            ws = [w for w in c[2] if w[0].strip() not in ("—", "–")]
            for i, w in enumerate(ws): w[0] = clean_word(w[0], i == len(ws) - 1)
            c[2] = [w for w in ws if w[0]]
        add_emojis(caps)
        s = s.replace(m.group(0), "const CAPS = [\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in caps) + ",\n];")
        if CSS_EMO not in s:
            s = s.replace("#caps .w.hl{", CSS_EMO + "\n#caps .w.hl{", 1)
        s = s.replace(JS_EMO_OLD, JS_EMO_NEW)
    # the Imagine wish bubble: no quote marks, an emoji instead; slice by characters so emojis never split
    s = s.replace("const QUOTE = '“a tiger on a bicycle”';", "const QUOTE = 'a tiger on a bicycle 🐯🚲';")
    s = s.replace("const QUOTE = '“an auto rickshaw flying to the moon”';", "const QUOTE = 'an auto rickshaw flying to the moon 🛺🌙';")
    s = s.replace("const n = Math.round(QUOTE.length * prog(", "const Q = [...new Intl.Segmenter().segment(QUOTE)].map(g => g.segment), n = Math.round(Q.length * prog(")
    s = s.replace("$('g-qt').textContent = QUOTE.slice(0, Math.max(1, n));", "$('g-qt').textContent = Q.slice(0, Math.max(1, n)).join('');")
    for a, b in fixed_text:
        if a in s: s = s.replace(a, b)
    # anything left (code comments) becomes plain punctuation
    s = s.replace(" — ", " - ").replace("—", "-").replace("–", "-").replace("…", "...").replace("“", '"').replace("”", '"')
    path.write_text(s)


FIXED = {
    "brag-output-2026-09-28-095057": [(">Insert a card…<", ">Insert a card<"), (">…a story plays.<", ">and a story plays 📖<"),
                                      (">…a rhyme starts.<", ">and a rhyme starts 🎵<"), (">…a game begins.<", ">and a game begins 🎮<")],
    "brag-output": [("<p>“a tiger riding a bicycle”</p>", "<p>a tiger riding a bicycle 🐯</p>"),
                    ("<p>“an auto rickshaw to the moon”</p>", "<p>an auto rickshaw to the moon 🛺</p>"),
                    ("<p>“a robot cooking dosa”</p>", "<p>a robot cooking dosa 🤖</p>")],
    "brag-output-2026-09-28-reel": [(">Just…</div>", ">Just</div>"), (">play!</div>", ">play! 🎉</div>")],
    "brag-output-2026-09-28-made-to-end": [(">That's it!</div>", ">That's it! 🙌</div>")],
    "brag-output-2026-09-28-made-in-india": [],
}
OUTRO = [('More <span class="hl">childhood.<b id="o-hl"></b></span>', 'More <span class="hl">childhood.<b id="o-hl"></b></span> 🧡')]

if __name__ == "__main__":
    for d, fx in FIXED.items():
        p = REPO / d / "work/compose.html"
        process(p, fx + OUTRO)
        left = sum(p.read_text().count(ch) for ch in "—–…“”")
        print(d, "leftover dash/ellipsis/curly:", left)
