"""Turn the English Reel compositions (already copied to <dir>-hi/work) into Hindi versions.

- Devanagari fonts (Noto Sans Devanagari as fallback after Gabarito / Hanken Grotesk).
- Word captions rebuilt from vo_lines_hi.json, in the same caption windows the English video uses,
  timed on the English timeline (the warp script maps them onto the Hindi voice).
- Fixed on-screen text translated (stamps, outro, pills). Device screens and the child's Imagine wish stay English.
- Re-injects the time-warp for the Hindi voice (work/warp.json from build_vo.py).
"""
import json, re
from pathlib import Path
from captions_clean import add_emojis

REPO = Path("/Users/ravikumar/Cheeko Master/cheeko-v2-website")
J = json.loads((Path(__file__).parent / "vo_lines_hi.json").read_text())

OUTRO = [('Less screen.<', 'कम स्क्रीन।<'), ('More <span class="hl">childhood.', 'ज़्यादा <span class="hl">बचपन।'),
         ('₹5,999 · Device + 10 cards', '₹5,999 · डिवाइस + 10 कार्ड'), ('Link in bio 👆', 'लिंक बायो में 👆'),
         ('Send this to a parent who needs it 👀', 'ये उस पेरेंट को भेजो जिसे इसकी ज़रूरत है 👀')]
TEXT = {
    "V03": OUTRO + [("const QUOTE = 'a tiger on a bicycle 🐯🚲';", "const QUOTE = 'साइकिल चलाता टाइगर 🐯🚲';"),
                    # the real firmware cannot show Devanagari (no glyphs in any built-in font), so the Hindi flow uses
                    # the renders of what it actually shows: listening -> painting (blank prompt line) -> picture without caption
                    ("imagine_tiger_2_listening_transcript.png", "imagine_tiger_hi_1_listening.png"), ("imagine_tiger_1_listening.png", "imagine_tiger_hi_1_listening.png"),
                    ("imagine_tiger_3_painting.png", "imagine_tiger_hi_3_painting.png"), ("imagine_tiger_5_result.png", "imagine_tiger_hi_5_result.png")] + [('<div>No<br>videos.</div>', '<div>ना<br>वीडियो।</div>'), ('<div>No<br>reels.</div>', '<div>ना<br>रील्स।</div>'),
                    ('<div>No<br>ads.</div>', '<div>ना<br>ऐड्स।</div>'), ('>Just</div>', '>बस</div>'), ('>play! 🎉</div>', '>खेलो! 🎉</div>')],
    "V04": OUTRO + [('Built to <span>END!</span>', 'रुकना <span>जानता है!</span>'), ('Everything it<br>ever shows:', 'बस इतना ही<br>दिखाता है:'),
                    (">That's it! 🙌</div>", '>बस इतना ही! 🙌</div>')],
    "V05": OUTRO + [("const QUOTE = 'an auto rickshaw flying to the moon 🛺🌙';", "const QUOTE = 'चाँद पर उड़ता ऑटो रिक्शा 🛺🌙';"),
                    ("imagine_rickshaw_2_listening_transcript.png", "imagine_rickshaw_hi_1_listening.png"), ("imagine_rickshaw_1_listening.png", "imagine_rickshaw_hi_1_listening.png"),
                    ("imagine_rickshaw_3_painting.png", "imagine_rickshaw_hi_3_painting.png"), ("imagine_rickshaw_5_result.png", "imagine_rickshaw_hi_5_result.png")] + [('<span>PRESSURE</span><br><span>COOKER!</span>', '<span>प्रेशर</span><br><span>कुकर!</span>'),
                    ('<div style="font-size:100px">MADE IN</div><div style="font-size:160px">INDIA</div>', '<div style="font-size:92px">मेड इन</div><div style="font-size:150px">इंडिया</div>'),
                    ('letter-spacing:.12em">FOR INDIAN KIDS</div>', 'letter-spacing:.04em">भारतीय बच्चों के लिए</div>'),
                    ('<p>BACKED BY</p>', '<p>इनका साथ</p>'), ('✋ Wait, why?', '✋ रुको, क्यों?')],
}
# words that get the yellow highlight in captions
HL = {"नहीं?!", "चीको!", "शुरू!", "जवाब", "भाषाएँ!", "BOOM", "तैयार!", "NEVER", "ख़त्म", "सो", "रुकना", "पहचानो!", "कार्ड।",
      "सीटी…", "घंटी…", "नानी", "सुनती", "हिंदी,", "इंग्लिश", "भारतीय"}


def captions(spec, windows):
    lines = spec["lines"]; caps = []
    for i, line in enumerate(lines):
        text, start = line[-3], line[-2]
        nxt = lines[i + 1][-2] if i + 1 < len(lines) else spec["old_vo_end"]
        # English caption windows that touch form one stretch; a line may run across several of them
        chains = []
        for a, b in sorted(windows):
            if chains and a - chains[-1][1] < .1: chains[-1][1] = max(chains[-1][1], b)
            else: chains.append([a, b])
        win = next(((a, b) for a, b in chains if a - .05 <= start < b - .02), None)
        if not win: continue
        text = re.sub(r"\s*\((laughs|gasps)\)", "", text).replace("चीको", "Cheeko")
        words = text.split()
        span = max(.3, (min(nxt, win[1]) - start) * .85)
        tot = sum(len(w) for w in words); acc = 0; ws = []
        for w in words:
            ws.append([w, round(start + span * acc / tot, 2)] + ([1] if w.strip("—") in HL or w in HL else []))
            acc += len(w)
        caps.append([round(start - .02, 2), round(min(nxt, win[1]) if i + 1 < len(lines) else win[1], 2), ws])
    # merge consecutive caption groups that belong to one sentence window (e.g. "हिंदी, तमिल, कन्नड़ — …")
    merged = []
    for c in caps:
        if merged and any(a - .05 <= merged[-1][0] and c[0] < b and merged[-1][0] < b for a, b in windows) \
                and len(" ".join(w[0] for w in merged[-1][2] + c[2])) <= 34 and abs(merged[-1][1] - c[0]) < .6:
            merged[-1][1] = c[1]; merged[-1][2] += c[2]
        else:
            merged.append(c)
    return merged


for vid in ("V03", "V04", "V05"):
    spec = J[vid]; work = REPO / (spec["dir"] + "-hi") / "work"
    p = work / "compose.html"; s = p.read_text()
    # fonts
    if "Noto+Sans+Devanagari:wght@700;800;900" not in s:
        s = re.sub(r"family=Noto\+Sans\+Devanagari:wght@800&", "", s)
        s = s.replace("family=Gabarito:wght@700;800;900&", "family=Gabarito:wght@700;800;900&family=Noto+Sans+Devanagari:wght@700;800;900&", 1)
        s = s.replace('--disp:"Gabarito",sans-serif', '--disp:"Gabarito","Noto Sans Devanagari",sans-serif')
        s = s.replace('--body:"Hanken Grotesk",sans-serif', '--body:"Hanken Grotesk","Noto Sans Devanagari",sans-serif')
        s = s.replace("window.render(0);\n  return true;", "await document.fonts.load('900 100px \"Noto Sans Devanagari\"', 'अआ');\n  await document.fonts.load('800 40px \"Noto Sans Devanagari\"', 'अआ');\n  window.render(0);\n  return true;", 1)
    # captions
    m = re.search(r"const CAPS = \[\n(.*?)\n\];", s, re.S)
    windows = [(float(a), float(b)) for a, b in re.findall(r"^\s*\[([0-9.]+), ([0-9.]+), \[", m.group(1), re.M)]
    caps = add_emojis(captions(spec, windows))
    js = "const CAPS = [\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in caps) + ",\n];"
    s = s.replace(m.group(0), js)
    # fixed text
    for a, b in TEXT[vid]:
        if a not in s: print("  missing", vid, a[:50])
        s = s.replace(a, b)
    # warp for the Hindi voice
    w = json.loads((work / "warp.json").read_text()); old = [0.0] + w["old"]; new = [0.0] + w["new"]
    s = re.sub(r"const NEW = \[.*?\], OLD = \[.*?\];", f"const NEW = {json.dumps(new)}, OLD = {json.dumps(old)};", s, count=1)
    p.write_text(s)
    sy = work / "synth.py"; t = sy.read_text(); t = re.sub(r"^DUR = [0-9.]+", f"DUR = {w['dur']}", t, count=1, flags=re.M); sy.write_text(t)
    print(vid, "captions", len(caps), "windows", len(windows), "dur", w["dur"])
