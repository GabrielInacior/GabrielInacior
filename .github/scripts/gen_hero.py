#!/usr/bin/env python3
"""Generates the IDE-window hero SVG for the GitHub profile README.
Noir-neon palette (shared with the user's RUMOR game + portfolio)."""
import base64, pathlib

REPO = pathlib.Path(r"C:\Project\GabrielInacior")
FONTS = REPO / "assets/svg/fonts"

def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()

mono = b64("jetbrains-mono-latin-400-normal.woff2")
monob = b64("jetbrains-mono-latin-700-normal.woff2")
bebas = b64("bebas-neue-latin-400-normal.woff2")

# ---- palette
NIGHT   = "#05091a"
EDITOR  = "#060c1f"
SIDEBAR = "#080f26"
ACTBAR  = "#070b1c"
TITLE   = "#0b1226"
BORDER1 = "#5aaadc"  # cyan
BORDER2 = "#ff4fa3"  # pink
LINENO  = "#2f3c66"
TEXT    = "#c9d4f0"
MUTED   = "#8ea2d6"
COMMENT = "#55659a"
KEYWORD = "#ff4fa3"  # pink
ACCENT  = "#ffc83d"  # amber
STRING  = "#8ef0b5"  # green
CYAN    = "#5aaadc"
PUNCT   = "#6b7aa8"
PROP    = "#9fd0ff"

W, H = 1280, 566

def t(x, y, spans, size=17, weight=400, anchor="start", extra=""):
    f = "JBM" if weight < 700 else "JBMB"
    inner = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in spans)
    return (f'<text x="{x}" y="{y}" font-family="{f},ui-monospace,monospace" '
            f'font-size="{size}" text-anchor="{anchor}" {extra}>{inner}</text>')

def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# editor code lines (x of code start = 360, gutter numbers at 338)
CX = 362
code_lines = [
    [("// who am i ", COMMENT), (": a software engineer who treats AI as a system, not a toy", COMMENT)],
    [("const ", KEYWORD), ("gabriel", ACCENT), (" = ", PUNCT), ("{", PUNCT)],
    [("  role", PROP), (": ", PUNCT), ('"Software Engineer"', STRING), (",  ", PUNCT), ("// 4+ yrs · tech lead · production architecture", COMMENT)],
    [("  stack", PROP), (": [", PUNCT), ('"TypeScript"', STRING), (", ", PUNCT), ('"Vue"', STRING), (", ", PUNCT), ('"Node"', STRING), (", ", PUNCT), ('"Flutter"', STRING), (", ", PUNCT), ('"PostgreSQL"', STRING), (", ", PUNCT), ('"AWS"', STRING), ("],", PUNCT)],
    [("  ai", PROP), (": ", PUNCT), ("{ ", PUNCT), ("orchestrates", CYAN), (": ", PUNCT), ('"multi-agent"', STRING), (", ", PUNCT), ("mcp", CYAN), (": ", PUNCT), ("true", KEYWORD), (", ", PUNCT), ("localLLMs", CYAN), (": ", PUNCT), ('"HF + Ollama"', STRING), (" },", PUNCT)],
    [("  automates", PROP), (": ", PUNCT), ('"wires AI into the OS, pipelines & processes"', STRING), (",", PUNCT)],
    [("  alsoInto", PROP), (": [", PUNCT), ('"game dev"', STRING), (", ", PUNCT), ('"cybersecurity"', STRING), ("],", PUNCT)],
    [("}", PUNCT)],
]

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="Gabriel Inácio — Software Engineer and AI Systems Builder">')

# defs: fonts, gradients, filters
svg.append(f'''<defs>
<style>
@font-face {{ font-family:'JBM'; src:url(data:font/woff2;base64,{mono}) format('woff2'); font-weight:400; }}
@font-face {{ font-family:'JBMB'; src:url(data:font/woff2;base64,{monob}) format('woff2'); font-weight:700; }}
@font-face {{ font-family:'Bebas'; src:url(data:font/woff2;base64,{bebas}) format('woff2'); font-weight:400; }}
text {{ dominant-baseline:alphabetic; }}
.cur {{ animation:blink 1.05s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity:0; }} }}
.glow {{ animation:pulse 3.2s ease-in-out infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:.55}} 50%{{opacity:1}} }}
.float {{ animation:float 6s ease-in-out infinite; }}
@keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-6px)}} }}
</style>
<linearGradient id="bord" x1="0" y1="0" x2="1" y2="1">
 <stop offset="0" stop-color="{BORDER1}"/><stop offset=".5" stop-color="#8b7bff"/><stop offset="1" stop-color="{BORDER2}"/>
</linearGradient>
<linearGradient id="namegrad" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="{ACCENT}"/><stop offset=".55" stop-color="#ffd877"/><stop offset="1" stop-color="{BORDER2}"/>
</linearGradient>
<radialGradient id="glowbg" cx="50%" cy="0%" r="90%">
 <stop offset="0" stop-color="#15245a" stop-opacity=".8"/><stop offset="1" stop-color="{NIGHT}" stop-opacity="0"/>
</radialGradient>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="nglow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="win"><rect x="20" y="16" width="{W-40}" height="{H-36}" rx="14"/></clipPath>
<clipPath id="typeclip"><rect x="{CX}" y="506" width="0" height="30"><animate attributeName="width" values="0;45;100;155;200;255;315;360;405;445" dur="2.4s" begin="0.5s" fill="freeze" calcMode="discrete" keyTimes="0;0.1;0.2;0.3;0.4;0.5;0.62;0.74;0.86;1"/></rect></clipPath>
</defs>''')

# bg
svg.append(f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>')
# outer neon glow behind window
svg.append(f'<rect class="glow" x="24" y="22" width="{W-48}" height="{H-44}" rx="16" fill="url(#bord)" filter="url(#soft)" opacity=".5"/>')
# window
svg.append(f'<rect x="20" y="16" width="{W-40}" height="{H-36}" rx="14" fill="{EDITOR}" stroke="url(#bord)" stroke-width="1.4"/>')
svg.append('<g clip-path="url(#win)">')
svg.append(f'<rect x="20" y="16" width="{W-40}" height="200" fill="url(#glowbg)"/>')

# title bar
svg.append(f'<rect x="20" y="16" width="{W-40}" height="40" fill="{TITLE}"/>')
svg.append(f'<line x1="20" y1="56" x2="{W-20}" y2="56" stroke="#17204a" stroke-width="1"/>')
for i, c in enumerate(["#e2384f", "#ffc83d", "#8ef0b5"]):
    svg.append(f'<circle cx="{44+i*22}" cy="36" r="6.5" fill="{c}"/>')
# active tab
svg.append(f'<rect x="300" y="26" width="220" height="30" rx="6" fill="{EDITOR}" stroke="#1b2550" stroke-width="1"/>')
svg.append(f'<circle cx="320" cy="41" r="4" fill="{ACCENT}"/>')
svg.append(t(336, 46, [("gabriel_inacio.ts", TEXT)], 14))
svg.append(t(498, 46, [("●", ACCENT)], 13))
svg.append(t(W-44, 46, [("main ⬇ ", MUTED)], 13, anchor="end"))

# activity bar
svg.append(f'<rect x="20" y="56" width="46" height="{H-76}" fill="{ACTBAR}"/>')
acts = [
    ('M3 3h12v14l-6-4-6 4z', ACCENT),          # files (active)
    ('M6 6a4 4 0 1 1 5 5l3 3-1.5 1.5-3-3A4 4 0 0 1 6 6z', MUTED),  # search
    ('M4 2v12M4 6a3 3 0 0 0 3 3h5M14 7v7', MUTED),  # git
    ('M9 2a6 6 0 0 1 6 6v3l2 2-2 1H3l-2-1 2-2V8a6 6 0 0 1 6-6z', MUTED),  # debug/bell
    ('M3 3h5v5H3zM11 3h5v5h-5zM3 11h5v5H3zM11 11h5v5h-5z', MUTED),       # extensions
]
for i, (d, col) in enumerate(acts):
    y = 84 + i*46
    if i == 0:
        svg.append(f'<rect x="20" y="{y-14}" width="3" height="34" fill="{ACCENT}"/>')
    op = 1 if i == 0 else 0.72
    fillattr = f'fill="{col}" stroke="none"' if i in (0, 4) else ''
    svg.append(f'<g transform="translate(33,{y-9})" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"><path d="{d}" {fillattr}/></g>')

# explorer sidebar
svg.append(f'<rect x="66" y="56" width="224" height="{H-76}" fill="{SIDEBAR}"/>')
svg.append(t(84, 82, [("EXPLORER", MUTED)], 11.5, weight=700, extra='letter-spacing="1.5"'))
svg.append(t(252, 82, [("···", MUTED)], 13))
svg.append(t(82, 110, [("⌄ ", ACCENT), ("PORTFOLIO", TEXT)], 12.5, weight=700, extra='letter-spacing=".5"'))
files = [
    ("about.ts", ACCENT, True),
    ("ai-orchestration.md", CYAN, False),
    ("architecture.ts", PROP, False),
    ("gamedev.gd", "#ff8a5c", False),
    ("security.sh", "#8ef0b5", False),
    ("devops.yml", "#c7b3ff", False),
    ("contact.json", ACCENT, False),
]
for i, (fn, col, active) in enumerate(files):
    y = 138 + i*30
    if active:
        svg.append(f'<rect x="66" y="{y-15}" width="224" height="28" fill="#111a3e"/>')
        svg.append(f'<rect x="66" y="{y-15}" width="2.5" height="28" fill="{ACCENT}"/>')
    svg.append(f'<rect x="100" y="{y-10}" width="11" height="13" rx="1.5" fill="none" stroke="{col}" stroke-width="1.4"/>')
    svg.append(t(122, y+4, [(fn, TEXT if active else MUTED)], 13, weight=700 if active else 400))

# editor gutter + code
for i in range(len(code_lines)):
    y = 118 + i*30
    svg.append(t(344, y+4, [(str(i+1), LINENO)], 13.5, anchor="end"))
    svg.append(t(CX, y+4, code_lines[i], 16))

# separator + hero "output" band (clear of the code object above)
svg.append(t(CX, 408, [("// ", COMMENT), ("output", COMMENT), (" →", COMMENT)], 14.5))
svg.append(f'<text x="{CX-2}" y="482" font-family="Bebas,JBMB,sans-serif" font-size="80" letter-spacing="2.5" fill="url(#namegrad)" filter="url(#nglow)">GABRIEL INÁCIO</text>')

# typing tagline with cursor
tag = '> building AI systems that actually ship'
cur_x = CX + int(len(tag) * 10.15)
svg.append(f'<g clip-path="url(#typeclip)">{t(CX, 524, [(tag, STRING)], 17, weight=700)}</g>')
svg.append(f'<rect class="cur" x="{cur_x}" y="510" width="10" height="20" fill="{ACCENT}"/>')

# right: subtle code "minimap" bars
import random
random.seed(7)
mmx = W-70
svg.append(f'<rect x="{mmx-6}" y="70" width="52" height="{H-96}" fill="#060b1e" opacity=".7"/>')
for i in range(26):
    wd = random.randint(10, 40)
    col = random.choice([COMMENT, PUNCT, CYAN, STRING, ACCENT])
    svg.append(f'<rect x="{mmx}" y="{80+i*12}" width="{wd}" height="5" rx="2" fill="{col}" opacity=".5"/>')

svg.append('</g>')  # end clip

# status bar (bottom, VS Code style)
sy = H-20
svg.append(f'<rect x="20" y="{sy-20}" width="{W-40}" height="20" rx="0" fill="{BORDER2}"/>')
svg.append(f'<rect x="20" y="{sy-20}" width="{W-40}" height="20" fill="#0b1226"/>')
svg.append(f'<rect x="20" y="{sy-20}" width="186" height="20" fill="{ACCENT}"/>')
svg.append(t(32, sy-6, [("⎇ main", NIGHT)], 12, weight=700))
svg.append(t(118, sy-6, [("✓ 0  ✗ 0", NIGHT)], 12, weight=700))
svg.append(t(224, sy-6, [("⚡ ", ACCENT), ("4+ yrs shipping to production", MUTED)], 12))
svg.append(t(W-40, sy-6, [("TypeScript  ", CYAN), ("UTF-8  LF  ", MUTED), ("◎ Brazil", STRING)], 12, anchor="end"))

# round corners mask already applied; close
svg.append('</svg>')

out = REPO / "assets/svg/hero.svg"
out.write_text("".join(svg), encoding="utf-8")
print("wrote", out, len(("".join(svg)).encode())//1024, "KB")
