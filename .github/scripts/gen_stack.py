#!/usr/bin/env python3
"""Handcrafted "pinned notes" stack board SVG — echoes the RUMOR corkboard,
not a generic icon strip. Fonts embedded (JetBrains Mono + Permanent Marker)."""
import base64, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets/svg/fonts"; OUT = ROOT / "assets/svg"

EDITOR="#070d22"; BOARD="#0a1026"; TITLE="#0b1226"; TEXT="#e7edff"; MUTED="#8ea2d6"
COMMENT="#55659a"; ACCENT="#ffc83d"; PINK="#ff4fa3"; CYAN="#5aaadc"; GREEN="#8ef0b5"
PURPLE="#c7b3ff"; ORANGE="#ff8a5c"; BORDER="#1b2550"

def b64(n): return base64.b64encode((FONTS/n).read_bytes()).decode()
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

GROUPS = [
 ("languages", ACCENT, ["TypeScript","JavaScript","Python","C#","Dart","Java","SQL"]),
 ("frontend",  CYAN,   ["Vue","Nuxt","React","React Native","Angular","Tailwind"]),
 ("backend",   GREEN,  ["Node","Fastify","Express","FastAPI","Spring Boot","ASP.NET"]),
 ("data · msg", PINK,  ["PostgreSQL","Prisma","Redis","RabbitMQ","MongoDB"]),
 ("cloud · devops", PURPLE, ["AWS","Docker","Linux","GitHub Actions","GitLab CI"]),
 ("ai · llm",  ORANGE, ["OpenAI","Hugging Face","Ollama","Whisper","MCP","RAG","embeddings"]),
 ("gamedev",   "#9fd0ff", ["Godot"]),
]

W = 920
PADX, LABEL_W = 30, 170
CHIP_H, CHIP_GAP, ROW_GAP = 34, 11, 16
CW = 8.1  # mono char width at 14px

def chip_w(txt): return int(len(txt)*CW) + 30

# layout pass
rows=[]  # list of (group_idx, label_or_None, [(txt,x)])
y = 96
group_y=[]
for gi,(label,acc,items) in enumerate(GROUPS):
    group_y.append(y)
    x = PADX + LABEL_W
    line_items=[]
    first=True
    for it in items:
        w = chip_w(it)
        if x + w > W - PADX:
            rows.append((gi, label if first else None, line_items)); first=False
            line_items=[]; x = PADX + LABEL_W; y += CHIP_H + CHIP_GAP
        line_items.append((it,x,w)); x += w + CHIP_GAP
    rows.append((gi, label if first else None, line_items))
    y += CHIP_H + ROW_GAP
H = y + 44

s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="tech stack">']
s.append(f'''<defs><style>
@font-face{{font-family:'JBM';src:url(data:font/woff2;base64,{b64("jetbrains-mono-latin-400-normal.woff2")}) format('woff2')}}
@font-face{{font-family:'JBMB';src:url(data:font/woff2;base64,{b64("jetbrains-mono-latin-700-normal.woff2")}) format('woff2');font-weight:700}}
@font-face{{font-family:'Marker';src:url(data:font/woff2;base64,{b64("permanent-marker-latin-400-normal.woff2")}) format('woff2')}}
.chip{{animation:cin .5s ease both}}@keyframes cin{{from{{opacity:0;transform:translateY(5px)}}}}
</style>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#14204a"/></pattern>
<linearGradient id="bd" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="2.4" flood-color="#000" flood-opacity="0.45"/></filter></defs>''')
# board
s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BOARD}" stroke="url(#bd)" stroke-width="1.3"/>')
s.append(f'<rect x="1" y="44" width="{W-2}" height="{H-45}" fill="url(#dots)" opacity="0.6"/>')
# title bar
s.append(f'<rect x="1" y="1" width="{W-2}" height="44" rx="14" fill="{TITLE}"/><rect x="1" y="30" width="{W-2}" height="15" fill="{TITLE}"/>')
for i,c in enumerate(["#e2384f",ACCENT,GREEN]): s.append(f'<circle cx="{28+i*20}" cy="23" r="5.5" fill="{c}"/>')
s.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-family="JBM,monospace" font-size="14" fill="{MUTED}">~/stack · pinned, not generated</text>')
# handwritten accent note (rotated), top-right
s.append(f'<g transform="translate({W-150},70) rotate(-7)"><text font-family="Marker,cursive" font-size="20" fill="{ACCENT}">built · shipped</text><text y="22" font-family="Marker,cursive" font-size="20" fill="{PINK}">· repeated</text></g>')

def chip(txt,x,y,acc,idx):
    w=chip_w(txt); rot=((idx*37)%7-3)*0.5  # deterministic small tilt
    cx,cy=x+w/2,y+CHIP_H/2
    g=[f'<g class="chip" style="animation-delay:{idx*0.02:.2f}s" transform="rotate({rot:.2f} {cx:.1f} {cy:.1f})" filter="url(#sh)">']
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{CHIP_H}" rx="8" fill="#0e1636" stroke="{acc}" stroke-opacity="0.55"/>')
    g.append(f'<circle cx="{x+12}" cy="{y+CHIP_H/2}" r="3.2" fill="{acc}"/>')  # pin
    g.append(f'<text x="{x+24}" y="{y+CHIP_H/2+5}" font-family="JBM,monospace" font-size="14" fill="{TEXT}">{esc(txt)}</text></g>')
    return "".join(g)

idx=0
for gi,label,items in rows:
    if not items: continue
    yy=items_y=0
    # y for this row: recompute from group start — easier: track via first item baseline
    # we stored y implicitly; recompute: use group_y mapping by counting — instead store y in layout
    pass

# redo with stored y: rebuild layout capturing y per row
rows=[]; y=96
for gi,(label,acc,items) in enumerate(GROUPS):
    x=PADX+LABEL_W; line=[]; first=True; row_y=y
    for it in items:
        w=chip_w(it)
        if x+w > W-PADX:
            rows.append((gi,acc,label if first else None,row_y,line)); first=False
            line=[]; x=PADX+LABEL_W; y+=CHIP_H+CHIP_GAP; row_y=y
        line.append((it,x)); x+=w+CHIP_GAP
    rows.append((gi,acc,label if first else None,row_y,line))
    y+=CHIP_H+ROW_GAP

for gi,acc,label,row_y,line in rows:
    if label:
        s.append(f'<text x="{PADX}" y="{row_y+CHIP_H/2+5}" font-family="JBMB,monospace" font-size="14" font-weight="700" fill="{acc}">{esc(label)}</text>')
        s.append(f'<text x="{PADX}" y="{row_y+CHIP_H/2+21}" font-family="JBM,monospace" font-size="10" fill="{COMMENT}">&#47;&#47; {len(GROUPS[gi][2])}</text>')
    for it,x in line:
        s.append(chip(it,x,row_y,acc,idx)); idx+=1

s.append("</svg>")
(OUT/"stack_board.svg").write_text("".join(s),encoding="utf-8")
print("stack_board.svg", H, "px,", idx, "chips")
