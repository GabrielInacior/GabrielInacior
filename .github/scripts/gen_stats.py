#!/usr/bin/env python3
"""Custom noir-neon GitHub-stats SVGs (KPI card + language bar).
Runs standalone (baked real numbers) or live in CI (GH_TOKEN set) — the
scheduled workflow regenerates it so the numbers stay current, with no
dependency on third-party stat services (which rate-limit / go down)."""
import base64, json, os, pathlib, urllib.request, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets/svg/fonts"
OUT = ROOT / "assets/svg"
USER = "GabrielInacior"

# ---- palette
NIGHT="#05091a"; EDITOR="#060c1f"; TITLE="#0b1226"; TEXT="#e7edff"; MUTED="#8ea2d6"
COMMENT="#55659a"; ACCENT="#ffc83d"; PINK="#ff4fa3"; CYAN="#5aaadc"; GREEN="#8ef0b5"; BORDER="#1b2550"
LANG_COLORS={"TypeScript":"#3178c6","Dart":"#00B4AB","Vue":"#41b883","Python":"#3572A5",
             "HTML":"#e34c26","GDScript":"#478cbf","Java":"#f89820","C#":"#8a56cf","CSS":"#8a73ff","JavaScript":"#f1e05a"}

DEFAULTS = {
    "commits": 1234, "contributions": 1324, "prs": 79, "repos": 40, "contributed": 11,
    "langs": [("TypeScript",40.5),("Dart",13.5),("Vue",10.8),("Python",8.1),
              ("GDScript",5.4),("Java",5.4),("C#",5.4)],
}

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def b64(n): return base64.b64encode((FONTS/n).read_bytes()).decode()

def fetch():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok: return DEFAULTS
    def gql(q, v):
        req=urllib.request.Request("https://api.github.com/graphql",
            data=json.dumps({"query":q,"variables":v}).encode(),
            headers={"Authorization":f"bearer {tok}","Content-Type":"application/json","User-Agent":USER})
        return json.load(urllib.request.urlopen(req, timeout=30))["data"]
    try:
        d=gql("""query($l:String!){user(login:$l){
            repositories(first:100,ownerAffiliations:OWNER,isFork:false){totalCount nodes{primaryLanguage{name}}}
            contributionsCollection{totalCommitContributions restrictedContributionsCount
              totalPullRequestContributions contributionCalendar{totalContributions}}}}""",{"l":USER})
        u=d["user"]; c=u["contributionsCollection"]
        cnt=collections.Counter((n.get("primaryLanguage") or {}).get("name") for n in u["repositories"]["nodes"])
        cnt.pop(None,None)
        for k in ("LLVM","Wolfram Language","Other"): cnt.pop(k,None)
        tot=sum(cnt.values()) or 1
        langs=[(k,round(100*v/tot,1)) for k,v in cnt.most_common(7)]
        return {"commits":c["totalCommitContributions"]+c["restrictedContributionsCount"],
                "contributions":c["contributionCalendar"]["totalContributions"],
                "prs":c["totalPullRequestContributions"],"repos":u["repositories"]["totalCount"],
                "contributed":DEFAULTS["contributed"],"langs":langs or DEFAULTS["langs"]}
    except Exception as e:
        print("fetch failed, using defaults:",e); return DEFAULTS

def fonts_defs():
    m,mb=b64("jetbrains-mono-latin-400-normal.woff2"),b64("jetbrains-mono-latin-700-normal.woff2")
    return (f"@font-face{{font-family:'JBM';src:url(data:font/woff2;base64,{m}) format('woff2')}}"
            f"@font-face{{font-family:'JBMB';src:url(data:font/woff2;base64,{mb}) format('woff2');font-weight:700}}")

def window(W,H,title,accent):
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-label="{esc(title)}">']
    s.append(f'<defs><style>{fonts_defs()}'
             f'.pop{{animation:pop .9s ease both}}@keyframes pop{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1}}}}'
             f'.bar{{animation:bg 1.2s cubic-bezier(.2,.9,.2,1) both}}@keyframes bg{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}</style>'
             f'<linearGradient id="bd" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{accent}"/></linearGradient>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1233"/><stop offset=".5" stop-color="#0d0a26"/><stop offset="1" stop-color="#0a1a28"/></linearGradient></defs>')
    s.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)" stroke="url(#bd)" stroke-width="1.3"/>')
    s.append(f'<rect x="1" y="1" width="{W-2}" height="38" rx="14" fill="{TITLE}"/><rect x="1" y="26" width="{W-2}" height="14" fill="{TITLE}"/>')
    for i,c in enumerate(["#e2384f",ACCENT,GREEN]): s.append(f'<circle cx="{26+i*20}" cy="20" r="5.5" fill="{c}"/>')
    s.append(f'<text x="{W/2}" y="25" text-anchor="middle" font-family="JBM,monospace" font-size="13.5" fill="{MUTED}">{esc(title)}</text>')
    s.append(f'<circle cx="{W-24}" cy="20" r="4" fill="{accent}"/>')
    return s

def kpi_card(st):
    W,H=500,308; s=window(W,H,"github_stats.sql",ACCENT)
    s.append(f'<text x="26" y="72" font-family="JBM,monospace" font-size="13.5"><tspan fill="{PINK}">SELECT</tspan><tspan fill="{MUTED}"> * </tspan><tspan fill="{PINK}">FROM</tspan><tspan fill="{CYAN}"> gabriel.activity</tspan><tspan fill="{MUTED}"> WHERE </tspan><tspan fill="{GREEN}">shipped</tspan><tspan fill="{MUTED}"> = </tspan><tspan fill="{ACCENT}">true</tspan><tspan fill="{MUTED}">;</tspan></text>')
    tiles=[(f"{st['commits']:,}","commits · last yr",ACCENT),
           (f"{st['contributions']:,}","contributions",GREEN),
           (f"{st['prs']}","pull requests",CYAN),
           (f"{st['repos']}","repositories",PINK),
           ("4+","years in prod",ACCENT),
           (f"{st['contributed']}","repos contributed",CYAN)]
    cw,ch=148,66; x0,y0,gx,gy=26,92,12,12
    for i,(val,lab,col) in enumerate(tiles):
        cx=x0+(i%3)*(cw+gx); cy=y0+(i//3)*(ch+gy)
        s.append(f'<g class="pop" style="animation-delay:{i*0.07}s"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="9" fill="#0a1230" stroke="{BORDER}"/>')
        s.append(f'<text x="{cx+16}" y="{cy+34}" font-family="JBMB,monospace" font-size="26" font-weight="700" fill="{col}">{esc(val)}</text>')
        s.append(f'<rect x="{cx+16}" y="{cy+40}" width="28" height="3" rx="1.5" fill="{col}"/>')
        s.append(f'<text x="{cx+16}" y="{cy+54}" font-family="JBM,monospace" font-size="12" fill="{MUTED}">{esc(lab)}</text></g>')
    s.append(f'<text x="26" y="296" font-family="JBM,monospace" font-size="11.5" fill="{COMMENT}">{st["commits"]:,} commits this year · public + private · auto-updated daily</text>')
    s.append("</svg>"); (OUT/"stats_card.svg").write_text("".join(s),encoding="utf-8")

def langs_card(st):
    W,H=500,308; s=window(W,H,"languages.json",CYAN)
    s.append(f'<text x="26" y="72" font-family="JBM,monospace" font-size="13.5"><tspan fill="{COMMENT}">// most used languages · by project</tspan></text>')
    langs=st["langs"][:7]; total=sum(p for _,p in langs) or 1
    # stacked bar
    bx,by,bw,bh=26,88,W-52,26; x=bx
    s.append(f'<clipPath id="bc"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8"/></clipPath><g clip-path="url(#bc)">')
    for name,pct in langs:
        w=bw*pct/total; col=LANG_COLORS.get(name,"#8892b0")
        s.append(f'<rect class="bar" x="{x:.1f}" y="{by}" width="{w:.1f}" height="{bh}" fill="{col}" style="transform-origin:{x:.1f}px"/>')
        x+=w
    s.append('</g>')
    # legend 2 cols
    lx,ly=26,150; cw=228
    for i,(name,pct) in enumerate(langs):
        col=LANG_COLORS.get(name,"#8892b0"); px=lx+(i%2)*cw; py=ly+(i//2)*34
        s.append(f'<g class="pop" style="animation-delay:{i*0.06}s"><circle cx="{px+6}" cy="{py-5}" r="6" fill="{col}"/>')
        s.append(f'<text x="{px+22}" y="{py}" font-family="JBMB,monospace" font-size="14" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
        s.append(f'<text x="{px+cw-26}" y="{py}" text-anchor="end" font-family="JBM,monospace" font-size="13" fill="{MUTED}">{pct:.1f}%</text></g>')
    s.append("</svg>"); (OUT/"stats_langs.svg").write_text("".join(s),encoding="utf-8")

if __name__=="__main__":
    st=fetch(); kpi_card(st); langs_card(st); print("stats svgs written:", st.get("commits"), len(st["langs"]), "langs")
