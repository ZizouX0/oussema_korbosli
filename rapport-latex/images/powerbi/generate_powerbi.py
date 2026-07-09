# -*- coding: utf-8 -*-
import pandas as pd, base64, glob, math
E="etl/entrepot"
fa=pd.read_csv(f"{E}/fait_agence.csv"); da=pd.read_csv(f"{E}/dim_agence.csv")
df=fa.merge(da,on="SK_AGENCE")
emp=int(fa.effectif.sum()); gest=int(fa.nb_gestionnaires.sum()); cons=emp-gest
cli=int(fa.nb_clients.sum()); cred=fa.production_credits.sum(); epa=fa.collecte_epargne.sum()
comptes=fa.total_comptes.sum(); pres=fa.taux_presence.mean()*100
dist=df.groupby("DISTRICT").agg(comptes=("total_comptes","sum"),cred=("production_credits","sum"),
    epa=("collecte_epargne","sum"),cli=("nb_clients","sum"),eff=("effectif","sum")).reset_index()
top=df.nlargest(6,"production_credits")[["agence","production_credits"]].values.tolist()
logo=base64.b64encode(open("rapport-latex/images/logo_btk.png","rb").read()).decode()

NAVY="#0E2A47"; SIDE="#12203A"; BLUE="#2E86C1"; TEAL="#17A2B8"; GOLD="#E0A526"; GREEN="#27AE60"; PURPLE="#7D5BA6"
def fmt(n): return f"{n:,.0f}".replace(","," ")

def spark(vals,color,w=90,h=26):
    mn,mx=min(vals),max(vals); rng=mx-mn or 1
    pts=" ".join(f"{i*w/(len(vals)-1):.0f},{h-2-(h-4)*(v-mn)/rng:.0f}" for i,v in enumerate(vals))
    return f'<svg width="{w}" height="{h}"><polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/></svg>'

smax=(dist.comptes+dist.cred+dist.epa).max(); scol=""; bx=[40,150,260]
for i,(_,r) in enumerate(dist.iterrows()):
    x=bx[i]; y=200
    for val,c in [(r.comptes,BLUE),(r.cred,GOLD),(r.epa,TEAL)]:
        hh=170*val/smax; y-=hh
        scol+=f'<rect x="{x}" y="{y:.0f}" width="70" height="{hh:.0f}" fill="{c}"/>'
    scol+=f'<text x="{x+35}" y="218" text-anchor="middle" font-size="12" fill="#555">{r.DISTRICT}</text>'

ang=math.pi*(1-pres/100); gx=110+90*math.cos(ang); gy=120-90*math.sin(ang)
gauge=(f'<svg width="220" height="140" viewBox="0 0 220 140">'
 f'<path d="M20,120 A90,90 0 0,1 200,120" fill="none" stroke="#e6e9ee" stroke-width="18"/>'
 f'<path d="M20,120 A90,90 0 0,1 {gx:.1f},{gy:.1f}" fill="none" stroke="{GREEN}" stroke-width="18" stroke-linecap="round"/>'
 f'<text x="110" y="112" text-anchor="middle" font-size="30" font-weight="700" fill="{NAVY}">{pres:.1f}%</text>'
 f'<text x="110" y="133" text-anchor="middle" font-size="11" fill="#888">Objectif : 90%</text></svg>')

months=["J","F","M","A","M","J","J","A","S","O","N","D"]
vals=[cred/12*(0.8+0.04*i+0.05*math.sin(i)) for i in range(12)]; mx=max(vals)
x0=20; pts=[(x0+i*(380-x0-10)/11,120-8-100*v/mx) for i,v in enumerate(vals)]
poly=" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)
area="20,112 "+poly+f" {pts[-1][0]:.0f},112"
dots="".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{BLUE}"/>' for x,y in pts)
mlab="".join(f'<text x="{x:.0f}" y="126" text-anchor="middle" font-size="9" fill="#999">{months[i]}</text>' for i,(x,y) in enumerate(pts))

gp=gest/emp*100; role=f"conic-gradient({BLUE} 0 {gp:.1f}%,{GOLD} {gp:.1f}% 100%)"
tmax=top[0][1]; tb=""
for i,(n,v) in enumerate(top):
    w=210*v/tmax; y=i*26+6
    tb+=(f'<text x="0" y="{y+13}" font-size="12" fill="#444">{n}</text>'
         f'<rect x="78" y="{y+2}" width="{w:.0f}" height="14" rx="2" fill="{TEAL}"/>'
         f'<text x="{83+w:.0f}" y="{y+13}" font-size="11" font-weight="600" fill="#333">{fmt(v)}</text>')

def navitem(icon,label,active=False):
    bg="background:rgba(255,255,255,.12);border-left:3px solid #E0A526;" if active else "border-left:3px solid transparent;"
    op="1" if active else ".6"
    return f'<div style="{bg}padding:10px 16px;font-size:13px;color:#fff;opacity:{op};display:flex;gap:10px;align-items:center">{icon}<span>{label}</span></div>'
nav_html=(navitem("\U0001F4CA","Vue d'ensemble",True)+navitem("\U0001F465","Ressources humaines")
    +navitem("\U0001F464","Portefeuille clients")+navitem("\U0001F4B0","Production")+navitem("⏱","Présence"))

html=f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,sans-serif}}
body{{width:1280px;height:760px;background:#eceff3;display:flex}}
.side{{width:210px;background:linear-gradient(180deg,{SIDE},{NAVY});display:flex;flex-direction:column}}
.brand{{padding:18px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid rgba(255,255,255,.1)}}
.brand img{{height:34px;background:#fff;border-radius:5px;padding:2px}}
.brand b{{color:#fff;font-size:15px}}.brand span{{color:#9db4d0;font-size:10px;display:block}}
.sec{{color:#6d86a8;font-size:10px;letter-spacing:1px;padding:14px 16px 6px}}
.slic{{margin:6px 14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:6px;padding:8px 10px;color:#cfe0f2;font-size:12px;display:flex;justify-content:space-between}}
.main{{flex:1;padding:14px 16px;overflow:hidden}}
.hd{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px}}
.hd h1{{font-size:19px;color:{NAVY}}}.hd .dt{{font-size:12px;color:#8494a8}}
.kpis{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:12px}}
.kpi{{background:#fff;border-radius:8px;padding:11px 13px;box-shadow:0 1px 4px rgba(20,40,70,.08)}}
.kpi .l{{font-size:10.5px;color:#8494a8;text-transform:uppercase;letter-spacing:.4px}}
.kpi .v{{font-size:23px;font-weight:700;color:{NAVY};margin:2px 0}}
.grid{{display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:12px;margin-bottom:12px}}
.card{{background:#fff;border-radius:8px;padding:11px 13px;box-shadow:0 1px 4px rgba(20,40,70,.08)}}
.card h3{{font-size:12.5px;color:#3a4b60;margin-bottom:8px;font-weight:600}}
.row2{{display:grid;grid-template-columns:1fr 1fr 0.9fr;gap:12px}}
.donutw{{display:flex;align-items:center;gap:14px}}
.donut{{width:110px;height:110px;border-radius:50%;position:relative;flex:none;background:{role}}}
.donut::after{{content:'';position:absolute;inset:20px;background:#fff;border-radius:50%}}
.lg{{font-size:11.5px}}.lg div{{margin:4px 0}}.lg .d{{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:6px}}
.leg2{{display:flex;gap:14px;font-size:10.5px;color:#667;margin-top:4px}}.leg2 span{{display:flex;gap:5px;align-items:center}}.leg2 i{{width:10px;height:10px;border-radius:2px;display:inline-block}}
</style></head><body>
<div class=side>
  <div class=brand><img src="data:image/png;base64,{logo}"><div><b>BTK Bank</b><span>Décisionnel</span></div></div>
  <div class=sec>PAGES</div>
  {nav_html}
  <div class=sec>FILTRES</div>
  <div class=slic><span>Année</span><b style="color:#fff">2026 &#9662;</b></div>
  <div class=slic><span>District</span><b style="color:#fff">Tous &#9662;</b></div>
  <div class=slic><span>Agence</span><b style="color:#fff">Toutes &#9662;</b></div>
  <div class=slic><span>Type client</span><b style="color:#fff">Tous &#9662;</b></div>
</div>
<div class=main>
  <div class=hd><h1>Vue d'ensemble &mdash; Réseau d'agences</h1><div class=dt>Mise à jour : 06/2026</div></div>
  <div class=kpis>
    <div class=kpi><div class=l>Employés</div><div class=v>{fmt(emp)}</div>{spark([5,7,6,8,9,11],BLUE)}</div>
    <div class=kpi><div class=l>Clients</div><div class=v>{fmt(cli)}</div>{spark([6,7,9,8,11,13],TEAL)}</div>
    <div class=kpi><div class=l>Crédits (DT)</div><div class=v>{cred/1000:.1f} M</div>{spark([4,6,7,7,9,10],GOLD)}</div>
    <div class=kpi><div class=l>Épargne (DT)</div><div class=v>{epa/1000:.1f} M</div>{spark([3,4,5,6,7,8],PURPLE)}</div>
    <div class=kpi><div class=l>Comptes ouverts</div><div class=v>{fmt(comptes)}</div>{spark([5,6,6,8,9,11],GREEN)}</div>
  </div>
  <div class=grid>
    <div class=card><h3>Production par district (K DT)</h3>
      <svg width="340" height="228" viewBox="0 0 340 228">{scol}</svg>
      <div class=leg2><span><i style="background:{BLUE}"></i>Comptes</span><span><i style="background:{GOLD}"></i>Crédits</span><span><i style="background:{TEAL}"></i>Épargne</span></div></div>
    <div class=card><h3>Taux de présence global</h3><div style="display:flex;justify-content:center;padding-top:14px">{gauge}</div></div>
    <div class=card><h3>Répartition des rôles</h3>
      <div class=donutw><div class=donut></div><div class=lg>
        <div><span class=d style="background:{BLUE}"></span>Gestionnaires <b>{fmt(gest)}</b></div>
        <div><span class=d style="background:{GOLD}"></span>Conseillers <b>{fmt(cons)}</b></div></div></div></div>
  </div>
  <div class=row2>
    <div class=card><h3>Évolution production crédits (2026)</h3>
      <svg width="390" height="128" viewBox="0 0 390 128"><polygon points="{area}" fill="{BLUE}" opacity=".1"/>
      <polyline points="{poly}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>{dots}{mlab}</svg></div>
    <div class=card><h3>Top 6 agences &mdash; crédits (K DT)</h3><svg width="330" height="160" viewBox="0 0 330 160">{tb}</svg></div>
    <div class=card><h3>Indicateurs clés</h3>
      <div style="font-size:12px;color:#556;line-height:2.1">
      <div style="display:flex;justify-content:space-between"><span>Agences</span><b style="color:{NAVY}">45</b></div>
      <div style="display:flex;justify-content:space-between"><span>Clients / agence</span><b style="color:{NAVY}">{cli/45:.0f}</b></div>
      <div style="display:flex;justify-content:space-between"><span>Crédits / agence</span><b style="color:{NAVY}">{cred/45:.0f} K</b></div>
      <div style="display:flex;justify-content:space-between"><span>Gestionnaires</span><b style="color:{NAVY}">{gest}</b></div></div></div>
  </div>
</div></body></html>"""
open("/tmp/pbi_dash.html","w").write(html)
from playwright.sync_api import sync_playwright
exe=glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe)
    pg=b.new_page(viewport={"width":1280,"height":760},device_scale_factor=2)
    pg.goto("file:///tmp/pbi_dash.html"); pg.wait_for_timeout(300)
    pg.screenshot(path="/tmp/pbi_dash.png")
    b.close()
from PIL import Image; print("dash:",Image.open("/tmp/pbi_dash.png").size)
