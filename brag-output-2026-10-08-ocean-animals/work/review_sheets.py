"""Contact-sheet HTML of Envato candidates (hot-linked watermarked previews) for checking species.
Usage: python3 review_sheets.py <out.html> <candidate index> <first n> <last n> [cols]"""
import json, sys, html
C = json.load(open('envato_candidates.json'))
out, ci, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); cols = int(sys.argv[5]) if len(sys.argv) > 5 else 5
cells = []
for x in C:
    if not a <= x['n'] <= b: continue
    c = x['candidates'][ci] if len(x['candidates']) > ci else None
    img = f'<img src="{html.escape(c["preview"])}">' if c else '<div class="none">none</div>'
    t = html.escape(c['title'][:60]) if c else ''
    cells.append(f'<div class="c">{img}<b>{x["n"]}. {html.escape(x["name"])}</b><i>{t}</i></div>')
open(out, 'w').write(f'''<!doctype html><meta charset="utf-8"><style>body{{margin:0;background:#222;color:#fff;font:14px/1.2 -apple-system}}
.g{{display:grid;grid-template-columns:repeat({cols},360px);gap:6px;padding:6px}}.c img,.none{{width:360px;height:240px;object-fit:contain;background:#000;display:block}}
b{{display:block;font-size:17px;margin-top:2px}}i{{display:block;color:#aaa;font-size:12px;height:15px;overflow:hidden}}</style><div class="g">{"".join(cells)}</div>''')
