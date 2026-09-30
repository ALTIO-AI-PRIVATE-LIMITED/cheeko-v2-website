"""Cheeko Video Library: a web page for the team with every video (thumbnail, links, caption), built from the same
data as the master sheet (master_sheet.collect()). Publish the output as an Artifact.
usage: library_page.py <out.html>
"""
import base64, datetime, html, io, json, sys
from pathlib import Path
from PIL import Image
import master_sheet as M

PUBLIC = "--site" in sys.argv   # the public page (GitHub Pages): only the final videos and captions, played from Drive "Public videos"
rows = [r for r in M.collect() if not (PUBLIC and r["series"] == "Archive")]
SERIES_NOTE = {
    "Brand and ads": "Hooks, ads and brand films for Reels.",
    "One feature per video": "One Cheeko feature per Reel, 25 to 40 seconds.",
    "Parent app": "Safety and control from the parent's phone.",
    "Onboarding Cheeko": "Getting started, in four parts: meet, switch on, connect, first five minutes.",
    "Cheeko App Guide": "The parent app, tab by tab, on an iPhone with the real app screens. Five parts and a full film.",
    "Archive": "Rejected, kept for reference.",
}


def thumb(r):
    src = M.P.REPO / r["repo_dir"]
    f = next((p for p in (src / "thumbnail.jpg", src / "brag.jpg") if p.exists()), None)
    if not f: return ""
    im = Image.open(f).convert("RGB"); im.thumbnail((180, 320)); b = io.BytesIO(); im.save(b, "JPEG", quality=74, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


cards = {}
for r in rows:
    base = r["vid"].replace("-HI", "")
    c = cards.setdefault(base, {"id": base, "series": r["series"], "about": r["about"], "langs": {}})
    lang = "hi" if r["lang"] == "Hindi" else "en"
    if lang == "en": c.update(title=r["title"], fmt=r["fmt"], status=r["status"], thumb=thumb(r))
    c["langs"][lang] = {k: r[k] for k in ("length", "status", "watch", "w16", "thumb", "ready", "files", "script", "caption", "public", "public16")}
data = [c for c in cards.values()]
if PUBLIC:   # the public page's source carries only what it shows: no internal links, no status
    for c in data:
        c.pop("status", None)
        c["langs"] = {k: {f: L[f] for f in ("length", "public", "public16", "caption")} for k, L in c["langs"].items()}
series = [s for s in M.ORDER if any(c["series"] == s for c in data)]
drive = M.link(M.P.DRIVE, True); sheet = M.link(M.P.DRIVE / M.OUT_NAME)
n_en = sum("en" in c["langs"] for c in data); n_hi = sum("hi" in c["langs"] for c in data)
today = datetime.date.today().strftime("%-d %B %Y")

page = r"""<title>Cheeko Video Library</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800;900&family=Hanken+Grotesk:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--ground:#FFF7EC;--surface:#FFFFFF;--ink:#231A10;--muted:#75624E;--line:#EFE1CF;--accent:#E8491A;--accent-ink:#FFFFFF;--sun:#FFC81A;--chip:#FBEBD6;
  --ok-bg:#E1F2E6;--ok:#2F6B4F;--rev-bg:#FFF0C7;--rev:#8A5A00;--rej-bg:#EEEAE5;--rej:#6F6358;--shadow:0 1px 2px rgba(35,26,16,.06),0 8px 24px rgba(35,26,16,.06);
  --disp:"Gabarito","Hanken Grotesk",system-ui,sans-serif;--body:"Hanken Grotesk","Noto Sans Devanagari",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--ground:#15110D;--surface:#201912;--ink:#F7EEE3;--muted:#BCA992;--line:#3A2F24;--accent:#FF6B3D;--accent-ink:#1A120C;--chip:#2B2219;
  --ok-bg:#16301F;--ok:#8FD3A6;--rev-bg:#3A2C0C;--rev:#FFD479;--rej-bg:#2A2521;--rej:#B5A898;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.25)}}
:root[data-theme="dark"]{color-scheme:dark;--ground:#15110D;--surface:#201912;--ink:#F7EEE3;--muted:#BCA992;--line:#3A2F24;--accent:#FF6B3D;--accent-ink:#1A120C;--chip:#2B2219;
  --ok-bg:#16301F;--ok:#8FD3A6;--rev-bg:#3A2C0C;--rev:#FFD479;--rej-bg:#2A2521;--rej:#B5A898;--shadow:0 1px 2px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.25)}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:15px/1.5 var(--body);padding-inline:clamp(16px,4vw,48px);padding-block:32px 64px}
.wrap{max-width:1240px;margin:0 auto}
h1,h2,h3{font-family:var(--disp);text-wrap:balance;margin:0}
header{display:flex;flex-wrap:wrap;gap:16px 32px;align-items:flex-end;justify-content:space-between;padding-bottom:20px;border-bottom:2px solid var(--ink)}
.brand{display:flex;flex-direction:column;gap:6px}
.eyebrow{font:600 12px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
h1{font-size:clamp(34px,5vw,54px);font-weight:900;letter-spacing:-.02em;line-height:1}
.summary{color:var(--muted);max-width:62ch}
.summary b{color:var(--ink);font-variant-numeric:tabular-nums}
.top-links{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:9px 16px;font:600 14px/1 var(--body);text-decoration:none;border:1.5px solid var(--ink);color:var(--ink);background:transparent;cursor:pointer}
.btn.primary{background:var(--ink);color:var(--ground)}
.btn:hover{background:var(--chip)}.btn.primary:hover{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn:focus-visible,.chip:focus-visible,.act:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--sun);outline-offset:2px}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--ground);display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line)}
.bar input,.bar select{font:500 14px/1 var(--body);color:var(--ink);background:var(--surface);border:1.5px solid var(--line);border-radius:10px;padding:10px 12px}
.bar input{flex:1 1 220px;min-width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font:600 13px/1 var(--body);border-radius:999px;padding:8px 12px;border:1.5px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
.chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--ground)}
.count{margin-left:auto;color:var(--muted);font-size:13px;font-variant-numeric:tabular-nums}
section{margin-top:40px}
.sec-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin-bottom:14px}
.sec-head h2{font-size:26px;font-weight:800}
.sec-head p{margin:0;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,380px),1fr));gap:14px}
.card{display:grid;grid-template-columns:96px 1fr;gap:14px;background:var(--surface);border-radius:16px;padding:12px;box-shadow:var(--shadow)}
.thumb{width:96px;aspect-ratio:9/16;border-radius:10px;object-fit:cover;background:var(--chip);max-width:100%}
.noimg{display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:12px}
.info{display:flex;flex-direction:column;gap:6px;min-width:0}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:12px;color:var(--muted)}
.vid{font:800 12px/1 var(--disp);letter-spacing:.04em;background:var(--sun);color:#231A10;border-radius:6px;padding:4px 6px}
.pill{font:700 11px/1 var(--body);border-radius:999px;padding:5px 8px}
.pill.ok{background:var(--ok-bg);color:var(--ok)}.pill.rev{background:var(--rev-bg);color:var(--rev)}.pill.rej{background:var(--rej-bg);color:var(--rej)}
.card h3{font-size:19px;font-weight:800;line-height:1.15}
.about{margin:0;color:var(--muted);font-size:13.5px;line-height:1.45}
.langs{display:flex;flex-direction:column;gap:6px;margin-top:4px}
.lang{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.lang .tag{font:700 11px/1 var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);width:54px;font-variant-numeric:tabular-nums}
.act{font:600 12.5px/1 var(--body);text-decoration:none;color:var(--ink);background:var(--chip);border-radius:8px;padding:7px 9px;border:0;cursor:pointer;white-space:nowrap}
.act.watch{background:var(--accent);color:var(--accent-ink)}
.act:hover{filter:brightness(.95)}
details.cap{font-size:12.5px;color:var(--muted)}
details.cap summary{cursor:pointer}
details.cap textarea{width:100%;min-height:110px;margin-top:6px;font:13px/1.45 var(--body);color:var(--ink);background:var(--ground);border:1px solid var(--line);border-radius:8px;padding:8px;resize:vertical}
.next{display:grid;gap:10px}
.next div{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr) minmax(0,2fr);gap:12px;background:var(--surface);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow)}
.next b{font-family:var(--disp)}
.next span{color:var(--muted)}
@media (max-width:640px){.next div{grid-template-columns:1fr}.count{margin-left:0}}
.foot{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}
.toast{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:var(--ink);color:var(--ground);padding:10px 16px;border-radius:999px;font:600 14px/1 var(--body);opacity:0;transition:opacity .2s;pointer-events:none}
.toast.on{opacity:1}
@media (prefers-reduced-motion:reduce){.toast{transition:none}}
[hidden]{display:none!important}
</style>
<div class="wrap">
<header>
  <div class="brand"><span class="eyebrow">Altio AI · Marketing</span><h1>Cheeko Video Library</h1>
    <div class="summary">Every Cheeko video we have made: <b>__NCARDS__</b> videos, <b>__NEN__</b> in English and <b>__NHI__</b> with a Hindi version. Updated __TODAY__. Links open in Google Drive for anyone the "cheeko ai videos" folder is shared with.</div></div>
  <div class="top-links"><a class="btn primary" href="__SHEET__" target="_blank" rel="noopener">Open master sheet</a><a class="btn" href="__DRIVE__" target="_blank" rel="noopener">Drive folder</a></div>
</header>
<div class="bar" role="search">
  <label for="q" hidden>Search videos</label><input id="q" type="search" placeholder="Search by name, ID or topic">
  <div class="chips" id="series"></div>
  <label for="lang" hidden>Language</label><select id="lang"><option value="all">All languages</option><option value="hi">Has Hindi</option><option value="en-only">English only</option></select>
  <label for="status" hidden>Status</label><select id="status"><option value="all">Any status</option><option value="Final draft">Final draft</option><option value="Draft for review">Draft for review</option><option value="Rejected">Rejected</option></select>
  <span class="count" id="count"></span>
</div>
<main id="list"></main>
<section><div class="sec-head"><h2>Coming next</h2><p>Planned or in progress, not published yet.</p></div><div class="next">__NEXT__</div></section>
<p class="foot">Ready to post holds only the video, thumbnail and caption for each video. All files holds the script, voice, test frames, finals and source. Status: Final draft = ready to post; Draft for review = waiting for Ravi's review. The master sheet and this page are rebuilt from the same list each time the videos are published.</p>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
const DATA = __DATA__;
const SERIES = __SERIES__;
const NOTES = __NOTES__;
const PUBLIC = __PUBLIC__;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const cls = s => s === 'Final draft' ? 'ok' : s === 'Rejected' ? 'rej' : 'rev';
let active = 'All';
function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('on'), 1600); }
function langRow(c, key) {
  const L = c.langs[key]; if (!L) return '';
  const a = (u, t, k) => u ? `<a class="act ${k || ''}" href="${esc(u)}" target="_blank" rel="noopener">${t}</a>` : '';
  return `<div class="lang"><span class="tag">${key === 'hi' ? 'Hindi' : 'English'} ${esc(L.length)}</span>
    ${PUBLIC ? a(L.public, '▶ Watch', 'watch') + a(L.public16, '▶ 16:9 (YouTube)') : a(L.watch, '▶ Watch', 'watch') + a(L.w16, '▶ 16:9') + a(L.ready, 'Ready to post') + a(L.files, 'All files') + a(L.script, 'Script')}
    ${L.caption ? `<button class="act" type="button" data-cap="${c.id}|${key}">Copy caption</button>` : ''}</div>
    ${L.caption ? `<details class="cap" id="cap-${c.id.replace('.', '_')}-${key}"><summary>Show ${key === 'hi' ? 'Hindi' : 'English'} caption</summary><textarea readonly id="t-${c.id.replace('.', '_')}-${key}">${esc(L.caption)}</textarea></details>` : ''}`;
}
function card(c) {
  const img = c.thumb ? `<img class="thumb" src="${c.thumb}" alt="Thumbnail of ${esc(c.title)}" loading="lazy">` : `<div class="thumb noimg">No cover</div>`;
  return `<article class="card">${img}<div class="info">
    <div class="meta"><span class="vid">${esc(c.id)}</span>${PUBLIC ? '' : `<span class="pill ${cls(c.status)}">${esc(c.status)}</span>`}<span>${esc(c.fmt === 'Film' ? 'Film' : 'Reel')}</span></div>
    <h3>${esc(c.title)}</h3><p class="about">${esc(c.about)}</p>
    <div class="langs">${langRow(c, 'en')}${langRow(c, 'hi')}</div></div></article>`;
}
function render() {
  const q = $('#q').value.trim().toLowerCase(), lang = $('#lang').value, st = $('#status') ? $('#status').value : 'all';
  const show = DATA.filter(c => (active === 'All' || c.series === active)
    && (lang === 'all' || (lang === 'hi' ? !!c.langs.hi : !c.langs.hi))
    && (st === 'all' || c.status === st)
    && (!q || [c.id, c.title, c.about, c.series, c.langs.en?.caption, c.langs.hi?.caption].join(' ').toLowerCase().includes(q)));
  $('#list').innerHTML = SERIES.map(s => { const cs = show.filter(c => c.series === s); if (!cs.length) return '';
    return `<section><div class="sec-head"><h2>${esc(s)}</h2><p>${esc(NOTES[s] || '')} ${cs.length} ${cs.length === 1 ? 'video' : 'videos'}.</p></div><div class="grid">${cs.map(card).join('')}</div></section>`; }).join('')
    || '<p style="margin-top:32px;color:var(--muted)">No videos match these filters.</p>';
  $('#count').textContent = `${show.length} of ${DATA.length} shown`;
}
$('#series').innerHTML = ['All', ...SERIES].map(s => `<button class="chip" type="button" aria-pressed="${s === active}" data-s="${esc(s)}">${esc(s)}</button>`).join('');
$('#series').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; active = b.dataset.s;
  document.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x === b)); try { localStorage.setItem('cvl-series', active); } catch (_) {} render(); });
['q', 'lang', 'status'].forEach(id => $('#' + id) && $('#' + id).addEventListener('input', render));
$('#list').addEventListener('click', e => { const b = e.target.closest('[data-cap]'); if (!b) return;
  const [id, key] = b.dataset.cap.split('|'), c = DATA.find(x => x.id === id), text = c.langs[key].caption, safe = id.replace('.', '_');
  const fallback = () => { const d = document.getElementById(`cap-${safe}-${key}`); d.open = true; const t = document.getElementById(`t-${safe}-${key}`); t.focus(); t.select(); toast('Caption selected. Copy it with your keyboard.'); };
  try { navigator.clipboard.writeText(text).then(() => toast('Caption copied'), fallback); } catch (_) { fallback(); } });
try { const s = localStorage.getItem('cvl-series'); if (s && SERIES.includes(s)) { active = s; document.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x.dataset.s === s)); } } catch (_) {}
render();
</script>
"""
nxt = "".join(f"<div><b>{html.escape(a)}</b><span>{html.escape(b)}</span><span>{html.escape(c)}</span></div>" for a, b, c in M.COMING)
page = (page.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__SERIES__", json.dumps(series, ensure_ascii=False))
        .replace("__NOTES__", json.dumps(SERIES_NOTE, ensure_ascii=False)).replace("__PUBLIC__", "true" if PUBLIC else "false").replace("__NEXT__", nxt)
        .replace("__NCARDS__", str(len(data))).replace("__NEN__", str(n_en)).replace("__NHI__", str(n_hi)).replace("__TODAY__", today)
        .replace("__SHEET__", sheet or "#").replace("__DRIVE__", drive or "#"))
if PUBLIC:   # public page: no internal status, file links, sheet or plans; a complete document kept out of search engines
    import re
    page = re.sub(r'<div class="summary">.*?</div></div>', f'<div class="summary">Every Cheeko marketing video: <b>{len(data)}</b> videos, <b>{n_hi}</b> of them also in Hindi. Tap Watch to play one; Copy caption gives you the post text with emojis and hashtags. Updated {today}.</div></div>', page, count=1, flags=re.S)
    page = re.sub(r'\s*<div class="top-links">.*?</div>\n', '\n', page, count=1, flags=re.S)
    page = re.sub(r'\s*<label for="status" hidden>Status</label><select id="status">.*?</select>', '', page, count=1, flags=re.S)
    page = re.sub(r'<section><div class="sec-head"><h2>Coming next</h2>.*?</section>\n', '', page, count=1, flags=re.S)
    page = re.sub(r'<p class="foot">.*?</p>', '<p class="foot">Videos play in Google Drive. Vertical videos are for Reels, Shorts and WhatsApp; the 16:9 versions are for YouTube and the website. Altio AI.</p>', page, count=1, flags=re.S)
    page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="robots" content="noindex,nofollow"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
            + page + '\n</head></html>').replace('<div class="wrap">', '</head><body><div class="wrap">', 1).replace('\n</head></html>', '\n</body></html>')
out = Path(sys.argv[1]); out.write_text(page)
print(out, f"{out.stat().st_size / 1e6:.2f} MB", len(data), "cards")
