#!/usr/bin/env python3
"""Section-header 'editor tab' SVGs + divider for the profile README."""
import pathlib
REPO = pathlib.Path(r"C:\Project\GabrielInacior")
SVGD = REPO / "assets/svg"

NIGHT="#05091a"; EDITOR="#060c1f"; TITLE="#0b1226"; TEXT="#c9d4f0"; MUTED="#8ea2d6"
COMMENT="#55659a"; ACCENT="#ffc83d"; PINK="#ff4fa3"; CYAN="#5aaadc"; GREEN="#8ef0b5"
MONO="ui-monospace,'Cascadia Code','JetBrains Mono',Consolas,monospace"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def tab(fname, accent, comment, icon):
    W,H = 900, 62
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="{esc(fname)} {esc(comment)}">']
    s.append(f'''<defs><style>
    .fade{{animation:fade 1s ease both}} @keyframes fade{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1}}}}
    .ln{{animation:grow 1.1s ease both}} @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
    </style>
    <linearGradient id="u{accent[1:]}" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient></defs>''')
    # tab strip bg
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="9" fill="{TITLE}"/>')
    s.append(f'<rect x="0" y="{H-4}" width="{W}" height="4" rx="2" fill="#0e1738"/>')
    # active tab
    tw = 34 + len(fname)*10.4 + 26
    s.append(f'<rect x="10" y="9" width="{tw}" height="44" rx="8" fill="{EDITOR}" stroke="#1b2550"/>')
    s.append(f'<rect x="10" y="9" width="3.5" height="44" rx="2" fill="{accent}"/>')
    s.append(f'<text x="30" y="37" font-family="{MONO}" font-size="16" fill="{accent}">{icon}</text>')
    s.append(f'<text x="52" y="37" font-family="{MONO}" font-size="16.5" font-weight="700" fill="{TEXT}">{esc(fname)}</text>')
    s.append(f'<circle cx="{10+tw-18}" cy="31" r="4.2" fill="{accent}"/>')
    # inactive ghost tabs
    gx = 10+tw+12
    for lbl in ["readme","..."]:
        gw = 22+len(lbl)*9
        s.append(f'<text x="{gx+14}" y="36" font-family="{MONO}" font-size="14" fill="{COMMENT}">{lbl}</text>')
        gx += gw+10
    # right comment
    s.append(f'<text x="{W-20}" y="37" text-anchor="end" font-family="{MONO}" font-size="14.5" fill="{COMMENT}" class="fade">{esc(comment)}</text>')
    # animated underline under active tab
    s.append(f'<rect class="ln" x="10" y="{H-4}" width="{tw}" height="4" rx="2" fill="url(#u{accent[1:]})" style="transform-origin:10px"/>')
    s.append('</svg>')
    (SVGD/f"tab_{fname.split('.')[0]}.svg").write_text("".join(s),encoding="utf-8")
    return fname

tabs = [
 ("ai_orchestration.md", ACCENT, "// how I work with AI: agents, MCPs, local models in containers", "✦"),
 ("engineering.ts",      CYAN,   "// long-time dev: architecture, SaaS, production apps", "{}"),
 ("featured.ts",         "#ff8a5c", "// flagship builds — AI, agents & games", "★"),
 ("security.sh",         GREEN,  "// cybersecurity: concepts + authorized offensive automation", "⌘"),
 ("stack.json",          "#c7b3ff", "// daily drivers", "≡"),
 ("github_stats.sql",    PINK,   "// what the commits say", "∑"),
 ("repositories.sql",    "#9fd0ff", "// more on my GitHub — apps · CRUD · UIs", "⎙"),
 ("connect.json",        ACCENT, "// let's build something", "⌁"),
]
for a in tabs: tab(*a)

# divider: thin neon line with a center node
dv=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="26" viewBox="0 0 900 26" fill="none">']
dv.append(f'<defs><linearGradient id="dv" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{ACCENT}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient>')
dv.append('<style>.p{animation:p 2.6s ease-in-out infinite}@keyframes p{0%,100%{opacity:.5}50%{opacity:1}}</style></defs>')
dv.append('<rect x="0" y="12" width="900" height="2" rx="1" fill="url(#dv)"/>')
dv.append(f'<circle class="p" cx="450" cy="13" r="5" fill="{ACCENT}"/><circle cx="450" cy="13" r="2.4" fill="{NIGHT}"/>')
dv.append('</svg>')
(SVGD/"divider.svg").write_text("".join(dv),encoding="utf-8")
print("assets written:", len(tabs)+1)
