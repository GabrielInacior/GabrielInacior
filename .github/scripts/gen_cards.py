#!/usr/bin/env python3
"""Bespoke project "dossier" cards — custom noir-neon containers with
ornate corner brackets (nod to Fortress Chaos frames), the screenshot framed
inside, a display title and tech chips. Image-less projects get a handmade
terminal/voice illustration. Visual-first, little text."""
import base64, io, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets/svg/fonts"; PROJ = ROOT / "assets/projects"; OUT = ROOT / "assets/svg"

NIGHT="#05091a"; PANEL="#070e24"; INNER="#0a1026"; TITLEBAR="#0b1226"; TEXT="#eaf0ff"
MUTED="#9fb0dc"; COMMENT="#55659a"; ACCENT="#ffc83d"; PINK="#ff4fa3"; CYAN="#5aaadc"
GREEN="#8ef0b5"; PURPLE="#c7b3ff"; GOLD="#e0b43c"; BORDER="#1b2550"; CW=8.2

def b64(n): return base64.b64encode((FONTS/n).read_bytes()).decode()
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def img_uri(name, maxw, jpeg=True):
    im = Image.open(PROJ/name).convert("RGB" if jpeg else "RGBA")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if jpeg: im.save(buf, "JPEG", quality=82, optimize=True); mime="jpeg"
    else: im.save(buf, "PNG", optimize=True); mime="png"
    return f"data:image/{mime};base64,{base64.b64encode(buf.getvalue()).decode()}", im.height/im.width

FONTDEF = (f"@font-face{{font-family:'Bebas';src:url(data:font/woff2;base64,{b64('bebas-neue-latin-400-normal.woff2')}) format('woff2')}}"
           f"@font-face{{font-family:'JBM';src:url(data:font/woff2;base64,{b64('jetbrains-mono-latin-400-normal.woff2')}) format('woff2')}}"
           f"@font-face{{font-family:'JBMB';src:url(data:font/woff2;base64,{b64('jetbrains-mono-latin-700-normal.woff2')}) format('woff2');font-weight:700}}")

W = 760; PAD = 20; IW = W - 2*PAD

def corner(x, y, flip_x, flip_y, acc):
    L = 22; dx = -1 if flip_x else 1; dy = -1 if flip_y else 1
    return (f'<path d="M {x} {y+dy*L} L {x} {y} L {x+dx*L} {y}" stroke="{acc}" '
            f'stroke-width="2.4" fill="none" stroke-linecap="round"/>')

def chips(tags, x, y, acc):
    out=[]; cx=x
    for tgname in tags:
        w=int(len(tgname)*CW)+22
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="26" rx="7" fill="#0e1636" stroke="{acc}" stroke-opacity="0.5"/>')
        out.append(f'<text x="{cx+11}" y="{y+17.5}" font-family="JBM,monospace" font-size="12.5" fill="{MUTED}">{esc(tgname)}</text>')
        cx += w+8
    return "".join(out), cx

def terminal_illu(x, y, w, h, acc, lines):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03060f" stroke="{BORDER}"/>']
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="10" fill="#060c1c"/><rect x="{x}" y="{y+16}" width="{w}" height="14" fill="#060c1c"/>')
    for i,c in enumerate(["#e2384f",ACCENT,GREEN]): s.append(f'<circle cx="{x+16+i*16}" cy="{y+15}" r="4" fill="{c}"/>')
    s.append(f'<text x="{x+w-14}" y="{y+19}" text-anchor="end" font-family="JBM,monospace" font-size="11" fill="{COMMENT}">blackwall ~ root</text>')
    ty=y+54
    for col,txt in lines:
        s.append(f'<text x="{x+18}" y="{ty}" font-family="JBM,monospace" font-size="13.5" fill="{col}">{esc(txt)}</text>'); ty+=24
    s.append(f'<rect x="{x+18}" y="{ty-13}" width="9" height="15" fill="{acc}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>')
    return "".join(s)

def voice_illu(x, y, w, h, acc):
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#03060f" stroke="{BORDER}"/>']
    import math
    cy=y+h*0.42; n=46; bw=(w-60)/n
    for i in range(n):
        amp=(math.sin(i*0.5)*0.5+0.5)*(h*0.22)+6
        bx=x+30+i*bw
        s.append(f'<rect x="{bx:.1f}" y="{cy-amp:.1f}" width="{bw*0.55:.1f}" height="{2*amp:.1f}" rx="2" fill="{CYAN if i%2 else acc}" opacity="{0.5+0.5*(i/n):.2f}"/>')
    s.append(f'<text x="{x+30}" y="{y+h-54}" font-family="JBM,monospace" font-size="13" fill="{GREEN}">voice  →  Whisper  →  GPT-4</text>')
    s.append(f'<rect x="{x+30}" y="{y+h-40}" width="{w-60}" height="26" rx="6" fill="#0a1226"/>')
    s.append(f'<text x="{x+40}" y="{y+h-22}" font-family="JBM,monospace" font-size="12.5" fill="{MUTED}">› formatted document ✓</text>')
    return "".join(s)

def card(key, title, kind, acc, tagline, tags, status, img=None, jpeg=True, illu=None):
    ix,iy = PAD, PAD+56
    if img:
        uri,ratio = img_uri(img, 720, jpeg)
        ih = int(IW*ratio)
    else:
        ih = 220; uri=None
    H = iy + ih + 16 + 26 + 18 + 26 + PAD
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="{esc(title)} — {esc(tagline)}">']
    s.append(f'<defs><style>{FONTDEF}</style>'
             f'<linearGradient id="g{key}" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{acc}"/><stop offset=".55" stop-color="#7b86ff"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
             f'<linearGradient id="t{key}" x1="0" x2="1"><stop offset="0" stop-color="{acc}"/><stop offset="1" stop-color="#fff4d6"/></linearGradient>'
             f'<linearGradient id="bgc{key}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1233"/><stop offset=".5" stop-color="#0c0a22"/><stop offset="1" stop-color="#0a1a26"/></linearGradient>'
             f'<clipPath id="ic{key}"><rect x="{ix}" y="{iy}" width="{IW}" height="{ih}" rx="10"/></clipPath>'
             f'<filter id="sh{key}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#000" flood-opacity="0.5"/></filter></defs>')
    # panel
    s.append(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="url(#bgc{key})" stroke="url(#g{key})" stroke-width="1.5"/>')
    s.append(f'<rect x="2" y="2" width="{W-4}" height="92" rx="16" fill="url(#g{key})" opacity="0.06"/>')
    # ornate corners
    s.append(corner(14,14,False,False,acc)+corner(W-14,14,True,False,acc)+corner(14,H-14,False,True,acc)+corner(W-14,H-14,True,True,acc))
    # header: title + kind tag + status
    s.append(f'<text x="{PAD}" y="{PAD+42}" font-family="Bebas,JBMB,sans-serif" font-size="40" letter-spacing="1.5" fill="url(#t{key})">{esc(title)}</text>')
    kw=int(len(kind)*7.6)+22
    s.append(f'<rect x="{W-PAD-kw}" y="{PAD+8}" width="{kw}" height="24" rx="12" fill="{acc}" opacity="0.14" stroke="{acc}" stroke-opacity="0.5"/>')
    s.append(f'<text x="{W-PAD-kw/2}" y="{PAD+24.5}" text-anchor="middle" font-family="JBMB,monospace" font-size="11.5" font-weight="700" fill="{acc}" letter-spacing="1">{esc(kind)}</text>')
    stt = {"private":("private",COMMENT),"live":("● live",GREEN),"repo":("‹ repo ›",CYAN),"wip":("◴ WIP",ACCENT),"alpha":("α Alpha",ACCENT)}.get(status,(status,MUTED))
    s.append(f'<text x="{W-PAD-kw-14}" y="{PAD+24.5}" text-anchor="end" font-family="JBM,monospace" font-size="12" fill="{stt[1]}">{esc(stt[0])}</text>')
    # image / illustration (framed)
    if uri:
        s.append(f'<g filter="url(#sh{key})"><image x="{ix}" y="{iy}" width="{IW}" height="{ih}" href="{uri}" preserveAspectRatio="xMidYMid slice" clip-path="url(#ic{key})"/>'
                 f'<rect x="{ix}" y="{iy}" width="{IW}" height="{ih}" rx="10" fill="none" stroke="{acc}" stroke-opacity="0.35"/></g>')
        s.append(f'<linearGradient id="vg{key}" x1="0" y1="0" x2="0" y2="1"><stop offset="0.65" stop-color="{NIGHT}" stop-opacity="0"/><stop offset="1" stop-color="{NIGHT}" stop-opacity="0.55"/></linearGradient>')
        s.append(f'<rect x="{ix}" y="{iy}" width="{IW}" height="{ih}" rx="10" fill="url(#vg{key})"/>')
    elif illu=="terminal":
        s.append(terminal_illu(ix,iy,IW,ih,acc,[(GREEN,"$ recon --target $OWNED_HOST"),(MUTED,"[*] enumerating services ..."),(CYAN,"[*] 3 findings · 1 critical"),(ACCENT,"[agent] chaining next tool"),(MUTED,"[*] fully local · offline · authorized")]))
    elif illu=="voice":
        s.append(voice_illu(ix,iy,IW,ih,acc))
    # tagline + chips
    ty = iy+ih+32
    s.append(f'<text x="{PAD}" y="{ty}" font-family="JBM,monospace" font-size="13.5" fill="{MUTED}">{esc(tagline)}</text>')
    ch,_ = chips(tags, PAD, ty+16, acc)
    s.append(ch)
    s.append("</svg>")
    (OUT/f"card_{key}.svg").write_text("".join(s),encoding="utf-8")
    return key

cards = [
 dict(key="buscavagas", title="BuscaVagas", kind="AI JOB ENGINE", acc=ACCENT, status="private",
      tagline="Local HF embeddings rank jobs by real fit · realtime · 100% local",
      tags=["TypeScript","Nuxt","Fastify","HF","Docker"], img="buscavagas.png", jpeg=True),
 dict(key="labia", title="LÁBIA", kind="VOICE AI GAME", acc=PINK, status="private",
      tagline="Co-op heist you play with your real voice · local-LLM NPCs",
      tags=["Godot","Local LLM","Whisper","multiplayer"], img="labia_scene.png", jpeg=True),
 dict(key="inaciocyber", title="InacioCyber", kind="PENTEST AGENT", acc=GREEN, status="private",
      tagline="Autonomous, 100% local pentest agent · authorized targets only",
      tags=["Python","Ollama","Qwen","Docker"], img="inaciocyber_matrix.png", jpeg=False),
 dict(key="formataai", title="FormataAI", kind="VOICE → TEXT", acc=CYAN, status="repo",
      tagline="Whisper + GPT-4 turn your voice into formatted docs · TCC",
      tags=["Flutter","Whisper","GPT-4","Node"], illu="voice"),
 dict(key="fortress", title="Fortress Chaos", kind="3D ROGUELITE", acc=GOLD, status="alpha",
      tagline="Base-building × tower-defense · hundreds of units · Godot 4.7",
      tags=["Godot","GDScript","3D"], img="fortresschaos.png", jpeg=False),
 dict(key="rumor", title="RUMOR", kind="DETECTIVE GAME", acc=ACCENT, status="live",
      tagline="Multiplayer comic-noir detective for the classroom",
      tags=["Godot","multiplayer","web"], img="rumor_banner.png", jpeg=True),
 dict(key="portfolio", title="inaciodev.online", kind="PORTFOLIO = 3D GAME", acc=PURPLE, status="wip",
      tagline="My portfolio is a first-person 3D noir game you walk through",
      tags=["Godot","web"], img="portfolio_elenco.png", jpeg=True),
]
for c in cards: card(**c); print("card_"+c["key"]+".svg")
