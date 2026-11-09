#!/usr/bin/env python3
"""Custom elements for the Software Engineering section — so it carries the
same handcrafted noir-neon weight as the rest of the profile instead of being
plain markdown. Writes two SVGs (fonts embedded):
  - arch_diagram.svg : an animated multi-tier systems architecture ("I design
    systems"), with data flowing along the connectors.
  - prod_apps.svg    : a dossier panel of the apps that serve real users
    (BarberCore, Orbix, AirMessage, ATN360) with status + tech chips.
"""
import base64, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets/svg/fonts"; OUT = ROOT / "assets/svg"

NIGHT="#05091a"; PANEL="#070e24"; BOARD="#0a1026"; TITLE="#0b1226"; TEXT="#eaf0ff"
MUTED="#9fb0dc"; COMMENT="#55659a"; ACCENT="#ffc83d"; PINK="#ff4fa3"; CYAN="#5aaadc"
GREEN="#8ef0b5"; PURPLE="#c7b3ff"; ORANGE="#ff8a5c"; BORDER="#1b2550"
MONO="JBM,ui-monospace,monospace"; CW=8.2

def b64(n): return base64.b64encode((FONTS/n).read_bytes()).decode()
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

FONTDEF = ("<style>"
  f"@font-face{{font-family:'Bebas';src:url(data:font/woff2;base64,{b64('bebas-neue-latin-400-normal.woff2')}) format('woff2')}}"
  f"@font-face{{font-family:'JBM';src:url(data:font/woff2;base64,{b64('jetbrains-mono-latin-400-normal.woff2')}) format('woff2')}}"
  f"@font-face{{font-family:'JBMB';src:url(data:font/woff2;base64,{b64('jetbrains-mono-latin-700-normal.woff2')}) format('woff2');font-weight:700}}"
  ".flow{animation:f 2.4s linear infinite}@keyframes f{to{stroke-dashoffset:-26}}"
  ".cin{animation:c .6s ease both}@keyframes c{from{opacity:0;transform:translateY(5px)}}"
  "</style>")

def chips(tags, x, y, acc, size=12.5, h=25):
    out=[]; cx=x
    for t in tags:
        w=int(len(t)*CW*(size/14))+20
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" rx="7" fill="#0e1636" stroke="{acc}" stroke-opacity="0.5"/>')
        out.append(f'<text x="{cx+10}" y="{y+h/2+4.4}" font-family="{MONO}" font-size="{size}" fill="{MUTED}">{esc(t)}</text>')
        cx+=w+8
    return "".join(out)

def titlebar(w, label):
    s=[f'<rect x="1" y="1" width="{w-2}" height="44" rx="15" fill="{TITLE}"/><rect x="1" y="30" width="{w-2}" height="15" fill="{TITLE}"/>']
    for i,c in enumerate(["#e2384f",ACCENT,GREEN]): s.append(f'<circle cx="{26+i*20}" cy="23" r="5.5" fill="{c}"/>')
    s.append(f'<text x="{w/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="13.5" fill="{MUTED}">{esc(label)}</text>')
    return "".join(s)

def shell(w, h, label):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-label="{esc(label)}">']
    s.append(f'<defs>{FONTDEF}'
      f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#14204a"/></pattern>'
      f'<linearGradient id="bd" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
      f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1233"/><stop offset=".5" stop-color="#0d0a26"/><stop offset="1" stop-color="#0a1a28"/></linearGradient>'
      f'<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="2.6" flood-color="#000" flood-opacity="0.45"/></filter></defs>')
    s.append(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="url(#bg)" stroke="url(#bd)" stroke-width="1.3"/>')
    s.append(f'<rect x="1" y="44" width="{w-2}" height="{h-45}" fill="url(#dots)" opacity="0.55"/>')
    s.append(titlebar(w, label))
    return s

# ───────────────────────── arch_diagram.svg ─────────────────────────
def node(x, y, w, h, acc, lines, delay=0.0):
    s=[f'<g class="cin" style="animation-delay:{delay:.2f}s" filter="url(#sh)">']
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#0e1636" stroke="{acc}" stroke-opacity="0.6"/>')
    # handcrafted dossier corner ticks instead of a left accent bar
    s.append(f'<path d="M {x+3} {y+13} L {x+3} {y+7} Q {x+3} {y+3} {x+7} {y+3} L {x+13} {y+3}" stroke="{acc}" stroke-width="1.7" fill="none" stroke-linecap="round"/>')
    s.append(f'<path d="M {x+w-3} {y+h-13} L {x+w-3} {y+h-7} Q {x+w-3} {y+h-3} {x+w-7} {y+h-3} L {x+w-13} {y+h-3}" stroke="{acc}" stroke-width="1.7" fill="none" stroke-linecap="round" opacity="0.7"/>')
    ty=y+(h-len(lines)*16)/2+13
    for i,(txt,strong) in enumerate(lines):
        fam="JBMB" if strong else "JBM"; col=TEXT if strong else MUTED; sz=13 if strong else 11.5
        s.append(f'<text x="{x+16}" y="{ty+i*16}" font-family="{fam},monospace" font-size="{sz}" fill="{col}">{esc(txt)}</text>')
    s.append("</g>")
    return "".join(s)

def connect(x1,y1,x2,y2,acc,delay=0.0):
    mx=(x1+x2)/2
    d=f"M {x1} {y1} C {mx} {y1} {mx} {y2} {x2} {y2}"
    return (f'<path d="{d}" stroke="{acc}" stroke-width="1.6" stroke-opacity="0.35" fill="none"/>'
            f'<path d="{d}" stroke="{acc}" stroke-width="2" fill="none" stroke-dasharray="5 21" class="flow" style="animation-delay:{delay:.2f}s"/>')

def arch():
    W,H=900,372
    s=shell(W,H,"~/architecture · systems I design and ship")
    cols=[("CLIENTS",CYAN,74,214),("API · BFF",ACCENT,296,436),("SERVICES",GREEN,520,660),("DATA",PINK,716,872)]
    # tier labels
    for name,acc,x0,x1 in cols:
        s.append(f'<text x="{(x0+x1)/2}" y="72" text-anchor="middle" font-family="JBMB,monospace" font-size="12" font-weight="700" fill="{acc}" letter-spacing="1.5">{name}</text>')
    NH=46
    # node geometry: (x0,x1) and y tops
    T1=[(74,214,92),(74,214,152)]
    T2=[(296,436,92),(296,436,152)]
    T3=[(520,660,92),(520,660,152),(520,660,212)]
    T4=[(716,872,92),(716,872,152),(716,872,212)]
    def cy(n): return n[2]+NH/2
    # connectors (behind nodes)
    for a in T1:
        s.append(connect(a[1],cy(a),T2[0][0],cy(T2[0]),CYAN,delay=(a[2]%7)*0.1))
    for b in T3:
        s.append(connect(T2[0][1],cy(T2[0]),b[0],cy(b),ACCENT,delay=(b[2]%7)*0.12))
    for i,c in enumerate(T4):
        src=T3[i] if i<len(T3) else T3[-1]
        s.append(connect(src[1],cy(src),c[0],cy(c),GREEN,delay=i*0.12))
    # nodes
    labels={
      id(T1[0]):[("Web",True),("Nuxt · React",False)], id(T1[1]):[("Mobile",True),("Flutter · RN",False)],
      id(T2[0]):[("API / BFF",True),("Fastify · Spring",False)], id(T2[1]):[("Auth",True),("OAuth2 · JWT · 2FA",False)],
      id(T3[0]):[("Realtime",True),("WebSockets",False)], id(T3[1]):[("Billing",True),("Stripe",False)], id(T3[2]):[("Queue · Jobs",True),("SQS · RabbitMQ",False)],
      id(T4[0]):[("PostgreSQL",True),("Prisma",False)], id(T4[1]):[("Redis",True),("cache",False)], id(T4[2]):[("MongoDB",True),("docs",False)],
    }
    d=0
    for tier,acc in [(T1,CYAN),(T2,ACCENT),(T3,GREEN),(T4,PINK)]:
        for n in tier:
            s.append(node(n[0],n[2],n[1]-n[0],NH,acc,labels[id(n)],delay=d*0.06)); d+=1
    # platform bar
    by=288
    s.append(f'<rect x="28" y="{by}" width="{W-56}" height="52" rx="11" fill="#0d1430" stroke="{PURPLE}" stroke-opacity="0.5"/>')
    s.append(f'<text x="46" y="{by+22}" font-family="JBMB,monospace" font-size="12" font-weight="700" fill="{PURPLE}" letter-spacing="1.5">PLATFORM</text>')
    s.append(chips(["AWS","Docker","Linux","GitLab CI","GitHub Actions","observability"],46,by+28,PURPLE,size=12,h=20) if False else "")
    s.append(f'<text x="46" y="{by+42}" font-family="{MONO}" font-size="13" fill="{MUTED}">AWS  ·  Docker  ·  Linux  ·  GitLab / GitHub CI/CD  ·  spec-driven delivery</text>')
    s.append(f'<text x="{W-46}" y="{by+22}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{COMMENT}">multi-tenant · DDD · BFF</text>')
    s.append("</svg>")
    (OUT/"arch_diagram.svg").write_text("".join(s),encoding="utf-8")
    return "arch_diagram.svg"

# ───────────────────────── prod_apps.svg ─────────────────────────
def lock(x,y,c):
    return (f'<rect x="{x}" y="{y+4}" width="11" height="8" rx="1.5" fill="none" stroke="{c}" stroke-width="1.4"/>'
            f'<path d="M {x+2} {y+4} V {y+2.5} a 3.5 3.5 0 0 1 7 0 V {y+4}" fill="none" stroke="{c}" stroke-width="1.4"/>')

def status(x,y,kind):
    col={"clients":GREEN,"clients3":GREEN,"live":CYAN,"private":COMMENT}[kind]
    txt={"clients":"paying clients","clients3":"3 paying clients","live":"live","private":"private"}[kind]
    w=int(len(txt)*CW)+40
    s=[f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="11" fill="#0d1430" stroke="{col}" stroke-opacity="0.5"/>']
    if kind=="private": s.append(lock(x+12,y+5,col))
    else: s.append(f'<circle cx="{x+16}" cy="{y+11}" r="4" fill="{col}"><animate attributeName="opacity" values="1;.35;1" dur="2.2s" repeatCount="indefinite"/></circle>')
    s.append(f'<text x="{x+28}" y="{y+15.5}" font-family="{MONO}" font-size="12" fill="{col}">{esc(txt)}</text>')
    return "".join(s), w

APPS=[
 ("BarberCore",ACCENT,"clients","Multi-tenant barber-shop SaaS: scheduling, WhatsApp, loyalty, Stripe billing",["Node","PostgreSQL","Stripe","AWS","CI/CD"]),
 ("OrbixHub",PURPLE,"clients3","Auth + billing platform on web, desktop and mobile (Flutter), serving 3 paying clients",["Flutter","Web","Desktop","Mobile","Billing"]),
 ("AirMessage",CYAN,"private","Cross-platform messaging SaaS: WhatsApp automation and client management",["Flutter","2FA","WhatsApp","AWS"]),
 ("ATN360",GREEN,"live","Institutional site and custom CMS, from scratch: SEO 100, i18n, AI blog",["Nuxt SSR","SEO 100","i18n","Gemini"]),
]

def prod():
    W=900; RH=84; top=58; H=top+len(APPS)*RH+16
    s=shell(W,H,"~/production · apps serving real users")
    for i,(name,acc,kind,tag,tags) in enumerate(APPS):
        y=top+i*RH
        if i: s.append(f'<line x1="28" y1="{y}" x2="{W-28}" y2="{y}" stroke="{BORDER}" stroke-opacity="0.7"/>')
        s.append(f'<g class="cin" style="animation-delay:{i*0.08:.2f}s">')
        s.append(f'<text x="40" y="{y+40}" font-family="Bebas,sans-serif" font-size="27" letter-spacing="1" fill="{acc}">{esc(name.upper())}</text>')
        # hand-drawn marker underline under the name (no left bar)
        s.append(f'<path d="M 40 {y+47} q {int(len(name)*6.6)} -2 {int(len(name)*13.2)} 0" stroke="{acc}" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.8"/>')
        st,sw=status(40+int(len(name)*13.0)+18,y+18,kind)
        s.append(st)
        s.append(f'<text x="40" y="{y+58}" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{esc(tag)}</text>')
        s.append(chips(tags,40,y+64,acc,size=11.5,h=22))
        s.append("</g>")
    s.append("</svg>")
    (OUT/"prod_apps.svg").write_text("".join(s),encoding="utf-8")
    return "prod_apps.svg"

if __name__=="__main__":
    print("wrote", arch(), "+", prod())
