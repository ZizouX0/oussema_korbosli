# -*- coding: utf-8 -*-
"""
Genere les 3 pages DETAILLEES du tableau de bord Power BI (maquettes / design targets)
dans le meme style sombre « ZoomCharts » que la page 1 (dashboard_apercu.png).
Les chiffres sont REPRESENTATIFS (structure reelle : gouvernorats tunisiens, types de
client, statuts POINTAGE...). Les vrais chiffres viendront des donnees Oracle dans Power BI.
Sortie : powerbi/page2_clients.png, page3_commercial.png, page4_presence.png
"""
import base64, glob
from playwright.sync_api import sync_playwright
from PIL import Image

logo = base64.b64encode(open("rapport-latex/images/logo_btk.png", "rb").read()).decode()

# --- palette (identique a generate_dashboard.py) ---
BG="#17181C"; SIDE="#0E0F12"; CARD="#212329"; BRD="#2E3038"; TXT="#E8E9ED"; MUT="#8A8D95"
ORANGE="#E8833A"; GREEN="#5BBE5B"; BLUE="#4A90D9"; GOLD="#E0A526"; TEAL="#2AA9B5"; PURPLE="#9B7ED9"; PINK="#D96BA3"
def fmt(n): return f"{n:,.0f}".replace(","," ")

CSS=f"""
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,sans-serif}}
body{{width:1280px;height:760px;background:{BG};display:flex;color:{TXT}}}
.side{{width:172px;background:{SIDE};display:flex;flex-direction:column;align-items:center;padding:22px 0;border-right:1px solid {BRD}}}
.logo{{width:78px;height:78px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;margin-bottom:6px}}
.logo img{{width:60px}}
.side .nm{{font-size:13px;font-weight:600;margin-top:4px}}.side .rl{{font-size:10px;color:{MUT};margin-bottom:26px}}
.nav{{width:100%;padding:0 14px}}
.nav a{{display:flex;gap:10px;align-items:center;padding:11px 14px;font-size:13px;color:{MUT};border-radius:7px;margin-bottom:4px}}
.nav a.on{{background:{CARD};color:{TXT}}}
.av{{margin-top:auto;text-align:center;color:{MUT};font-size:11px}}
.av .c{{width:34px;height:34px;border-radius:50%;background:{ORANGE};margin:0 auto 5px}}
.main{{flex:1;padding:18px 22px;display:flex;flex-direction:column}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px}}
.top h1{{font-size:21px;letter-spacing:.5px;font-weight:700}}.top .sb{{font-size:11px;color:{MUT};margin-top:3px}}
.slic{{display:flex;gap:9px;align-items:center}}
.sl{{background:{CARD};border:1px solid {BRD};border-radius:6px;padding:6px 11px;font-size:11px;color:{MUT}}}
.sl b{{color:{TXT};display:block;font-size:12px}}
.rst{{background:#33353D;border-radius:6px;padding:9px 15px;font-size:11px;letter-spacing:1px;color:{TXT};font-weight:600}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;background:{CARD};border:1px solid {BRD};border-radius:10px;padding:15px 18px;margin-bottom:14px}}
.kpi{{text-align:center;border-right:1px solid {BRD};padding:0 8px}}
.kpi:last-child{{border:none}}
.kl{{font-size:11px;color:{MUT}}}.kv{{font-size:26px;font-weight:700;margin:5px 0 8px}}
.bar{{height:6px;background:#31333B;border-radius:3px;position:relative}}
.fill{{height:100%;border-radius:3px}}
.card{{background:{CARD};border:1px solid {BRD};border-radius:10px;padding:13px 15px}}
.card h3{{font-size:12.5px;color:{TXT};margin-bottom:10px;font-weight:600}}
.donutw{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.donut{{width:124px;height:124px;border-radius:50%;position:relative}}
.donut .dc{{position:absolute;inset:25px;background:{CARD};border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.dcb{{font-size:18px;font-weight:700}}.dcs{{font-size:9px;color:{MUT}}}
.dleg{{font-size:11px;width:100%}}.dleg div{{display:flex;justify-content:space-between;margin:3px 0;color:{MUT}}}
.dleg b{{color:{TXT}}}.dot{{width:9px;height:9px;border-radius:2px;display:inline-block;margin-right:6px}}
.hb{{display:flex;align-items:center;gap:9px;margin:7px 0;font-size:11.5px}}
.hb .lb{{width:78px;color:{MUT};text-align:right;flex-shrink:0}}
.hb .tr{{flex:1;height:15px;background:#2A2C33;border-radius:3px;overflow:hidden}}
.hb .tf{{height:100%;border-radius:3px}}
.hb .vl{{width:52px;color:{TXT};font-weight:600;flex-shrink:0}}
table{{width:100%;border-collapse:collapse;font-size:11.5px}}
th{{text-align:left;color:{MUT};font-size:10px;font-weight:500;padding:6px 7px;border-bottom:1px solid {BRD}}}
td{{padding:7px 7px;border-bottom:1px solid #262830;color:{TXT}}}
.rk{{color:{ORANGE};font-weight:700}}
.grid3{{display:grid;gap:14px;margin-bottom:14px}}
.flex1{{flex:1}}
.tag{{display:inline-block;padding:2px 7px;border-radius:10px;font-size:9.5px;font-weight:600}}
"""

def sidebar(active):
    def a(icon, name):
        cls=" on" if name==active else ""
        return f'<a class="{cls.strip()}">{icon} &nbsp;{name}</a>'
    return f"""<div class=side>
      <div class=logo><img src="data:image/png;base64,{logo}"></div>
      <div class=nm>BTK Bank</div><div class=rl>Décisionnel</div>
      <div class=nav>{a('📊','Résumé')}{a('👥','Clients')}{a('💼','Commercial')}{a('🕒','Présence')}</div>
      <div class=av><div class=c></div>Analyste BI</div>
    </div>"""

def header(title, sub, slicers):
    sl="".join(f'<div class=sl>{n}<b>{v} ▾</b></div>' for n,v in slicers)
    return f"""<div class=top>
      <div><h1>{title}</h1><div class=sb>{sub}</div></div>
      <div class=slic>{sl}<div class=rst>RESET</div></div></div>"""

def kpirow(items):
    def c(l,v,col):
        return f'<div class=kpi><div class=kl>{l}</div><div class=kv style="color:{col}">{v}</div><div class=bar><div class=fill style="width:{80}%;background:{col}"></div></div></div>'
    return f'<div class=kpis>{"".join(c(*i) for i in items)}</div>'

def donut(segs, big, small):
    tot=sum(v for _,v,_ in segs); acc=0; parts=[]
    for _,v,col in segs:
        a=acc/tot*100; b=(acc+v)/tot*100; parts.append(f"{col} {a:.1f}% {b:.1f}%"); acc+=v
    grad="conic-gradient("+",".join(parts)+")"
    leg="".join(f'<div><span class=dot style="background:{col}"></span>{n} <b>{v/tot*100:.0f}%</b></div>' for n,v,col in segs)
    return (f'<div class=donutw><div class=donut style="background:{grad}"><div class=dc>'
            f'<div class=dcb>{big}</div><div class=dcs>{small}</div></div></div>'
            f'<div class=dleg>{leg}</div></div>')

def hbars(rows, unit=""):
    mx=max(v for _,v,_ in rows)
    out=""
    for lab,v,col in rows:
        w=v/mx*100
        out+=(f'<div class=hb><div class=lb>{lab}</div><div class=tr>'
              f'<div class=tf style="width:{w:.0f}%;background:{col}"></div></div>'
              f'<div class=vl>{fmt(v)}{unit}</div></div>')
    return out

def vbars(rows, h=150, w=None, unit=""):
    n=len(rows); mx=max(v for _,v,_ in rows)
    bw=40; gap=18; W=w or n*(bw+gap)+10; x=10; out=""
    for lab,v,col in rows:
        bh=(h-40)*v/mx; y=h-25-bh
        out+=f'<rect x="{x}" y="{y:.0f}" width="{bw}" height="{bh:.0f}" rx="2" fill="{col}"/>'
        out+=f'<text x="{x+bw/2:.0f}" y="{h-10}" text-anchor="middle" font-size="9" fill="{MUT}">{lab}</text>'
        out+=f'<text x="{x+bw/2:.0f}" y="{y-4:.0f}" text-anchor="middle" font-size="9" fill="{TXT}">{v/mx*100:.0f}</text>' if False else ""
        x+=bw+gap
    return f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}">{out}</svg>'

def line_chart(pts, w=560, h=180, col=GREEN, labels=None):
    mx=max(pts); mn=min(pts)*0.9; n=len(pts)
    pad=30; iw=w-2*pad; ih=h-40
    xs=[pad+iw*i/(n-1) for i in range(n)]
    ys=[h-25-ih*(v-mn)/(mx-mn) for v in pts]
    poly=" ".join(f"{x:.0f},{y:.0f}" for x,y in zip(xs,ys))
    area=f"{pad},{h-25} "+poly+f" {pad+iw},{h-25}"
    dots="".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="{col}"/>' for x,y in zip(xs,ys))
    labs=""
    if labels:
        labs="".join(f'<text x="{xs[i]:.0f}" y="{h-8}" text-anchor="middle" font-size="9" fill="{MUT}">{labels[i]}</text>' for i in range(n))
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<polygon points="{area}" fill="{col}" opacity="0.12"/>'
            f'<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="2.5"/>{dots}{labs}</svg>')

def render(name, body_html):
    html=f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{body_html}</body></html>"
    open(f"/tmp/{name}.html","w").write(html)
    exe=glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')[0]
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=exe)
        pg=b.new_page(viewport={"width":1280,"height":760},device_scale_factor=2)
        pg.goto(f"file:///tmp/{name}.html"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"powerbi/{name}.png")
        b.close()
    print(name, Image.open(f"powerbi/{name}.png").size)

# =====================================================================
# PAGE 2 — CLIENTS (segmentation & territoire)
# =====================================================================
gouv=[("Tunis",3120,BLUE),("Sfax",2280,BLUE),("Ariana",1840,TEAL),("Sousse",1640,TEAL),
      ("Ben Arous",1560,GOLD),("Nabeul",1180,GOLD),("Bizerte",720,ORANGE),("Monastir",640,ORANGE)]
secteur=[("Commerce",4200,BLUE),("Services",3600,TEAL),("Industrie",2800,GOLD),
         ("Santé",1900,GREEN),("BTP",1500,ORANGE),("Tourisme",1300,PURPLE),("Agriculture",980,PINK)]
p2=sidebar("Clients")+"<div class=main>"+header(
    "CLIENTS — SEGMENTATION & TERRITOIRE",
    "Répartition du portefeuille client · 24 gouvernorats",
    [("Gouvernorat","Tous"),("Type","Tous"),("Secteur","Tous")])
p2+=kpirow([("Nb Clients","16 878",BLUE),("Particuliers","68 %",TEAL),
            ("Professionnels","24 %",GOLD),("Secteurs d'activité","7",GREEN)])
p2+=f"""<div class=grid3 style="grid-template-columns:200px 200px 1fr">
  <div class=card><h3>Type de client</h3>{donut([("Particulier",68,BLUE),("Professionnel",24,GOLD),("Entreprise",8,TEAL)],"16 878","Clients")}</div>
  <div class=card><h3>Sexe</h3>{donut([("Homme",58,TEAL),("Femme",42,PINK)],"58/42","H / F")}</div>
  <div class=card><h3>Répartition par gouvernorat (top 8)</h3>{hbars(gouv)}</div>
</div>"""
p2+=f"""<div class=grid3 style="grid-template-columns:1.35fr 1fr;flex:1;margin-bottom:0">
  <div class=card><h3>Clients par secteur d'activité</h3>{hbars(secteur)}</div>
  <div class=card><h3>Statut du portefeuille</h3>
    {donut([("Actif",82,GREEN),("Inactif",13,ORANGE),("Prospect",5,GOLD)],"82 %","Actifs")}</div>
</div>"""
p2+="</div>"
render("page2_clients", p2)

# =====================================================================
# PAGE 3 — PERFORMANCE COMMERCIALE (objectifs)
# =====================================================================
comptes=[("Chèques",19400,BLUE),("Épargne",12900,TEAL),("Courants",10700,GOLD)]
credits=[("Conso",13.0,GOLD),("Immo",11.3,ORANGE),("Invest",8.1,TEAL)]
months=["Jan","Fév","Mar","Avr","Mai","Juin"]
trend=[24.1,26.5,28.0,29.8,31.2,32.4]
byag=[("Agence 03","2 411","1 969","312"),("Agence 04","2 260","1 864","298"),
      ("Agence 02","2 090","1 819","276"),("Agence 05","1 998","1 744","254"),("Agence 07","1 870","1 627","231")]
p3=sidebar("Commercial")+"<div class=main>"+header(
    "PERFORMANCE COMMERCIALE — OBJECTIFS",
    "Souscriptions & production · exercice 2026",
    [("Agence","Toutes"),("Année-Mois","2026"),("Gestionnaire","Tous")])
p3+=kpirow([("Total Comptes","43 032",BLUE),("Total Crédits","32,4 M",GOLD),
            ("Collecte Épargne","18,7 M",TEAL),("Packs & Cartes","9 240",GREEN)])
credit_bars="".join(f'<div class=hb><div class=lb>{n}</div><div class=tr><div class=tf style="width:{v/13*100:.0f}%;background:{c}"></div></div><div class=vl>{v} M</div></div>' for n,v,c in credits)
p3+=f"""<div class=grid3 style="grid-template-columns:1fr 1fr 1fr">
  <div class=card><h3>Souscriptions par type de compte</h3>{hbars(comptes)}</div>
  <div class=card><h3>Production de crédits (M DT)</h3>{credit_bars}</div>
  <div class=card><h3>EER — Effort équipement</h3>
    {donut([("Particulier",64,BLUE),("Hors particulier",36,PURPLE)],"64 %","Particulier")}</div>
</div>"""
rows="".join(f'<tr><td class=rk>{i+1}</td><td>{a}</td><td>{c}</td><td style="color:{GOLD};font-weight:600">{cr}</td><td>{pk}</td></tr>' for i,(a,c,cr,pk) in enumerate(byag))
p3+=f"""<div class=grid3 style="grid-template-columns:1.3fr 1fr;flex:1;margin-bottom:0">
  <div class=card><h3>Évolution mensuelle de la production (M DT)</h3>{line_chart(trend,w=560,h=190,col=GOLD,labels=months)}</div>
  <div class=card><h3>Objectifs par agence (top 5)</h3>
    <table><tr><th>#</th><th>Agence</th><th>Comptes</th><th>Crédits</th><th>Packs</th></tr>{rows}</table></div>
</div>"""
p3+="</div>"
render("page3_commercial", p3)

# =====================================================================
# PAGE 4 — PRÉSENCE / RH (pointage)
# =====================================================================
pmonths=["Jan","Fév","Mar","Avr","Mai","Juin"]
ptrend=[89.4,90.1,88.7,91.6,92.3,91.2]
byag_p=[("Agence 12","Sfax","96 %",GREEN),("Agence 03","Tunis","95 %",GREEN),
        ("Agence 21","Sousse","88 %",GOLD),("Agence 09","Gabès","84 %",ORANGE),
        ("Agence 17","Kairouan","79 %",ORANGE)]
p4=sidebar("Présence")+"<div class=main>"+header(
    "PRÉSENCE & ASSIDUITÉ — RH",
    "Suivi du pointage des employés · 2 143 employés",
    [("Agence","Toutes"),("Mois","Juin"),("Statut","Tous")])
p4+=kpirow([("Taux de présence","91,2 %",GREEN),("Présences","5 480",GREEN),
            ("Retards","298",GOLD),("Absences","557",ORANGE)])
p4+=f"""<div class=grid3 style="grid-template-columns:1.3fr 190px 190px">
  <div class=card><h3>Évolution du taux de présence (%)</h3>{line_chart(ptrend,w=520,h=190,col=GREEN,labels=pmonths)}</div>
  <div class=card><h3>Statuts</h3>{donut([("Présent",86.5,GREEN),("Retard",4.7,GOLD),("Absent",8.8,ORANGE)],"91 %","Présence")}</div>
  <div class=card><h3>Source</h3>{donut([("Auto",78,TEAL),("Manuel",22,PURPLE)],"78 %","Auto")}</div>
</div>"""
rows_p="".join(f'<tr><td class=rk>{i+1}</td><td>{a}</td><td>{d}</td><td><span class=tag style="background:{c}22;color:{c}">{t}</span></td></tr>' for i,(a,d,t,c) in enumerate(byag_p))
p4+=f"""<div class=grid3 style="grid-template-columns:1fr 1fr;flex:1;margin-bottom:0">
  <div class=card><h3>Taux de présence par agence</h3>
    {hbars([("Sfax",96,GREEN),("Tunis",95,GREEN),("Ariana",92,GREEN),("Sousse",88,GOLD),("Gabès",84,ORANGE),("Kairouan",79,ORANGE)],unit=" %")}</div>
  <div class=card><h3>Agences à surveiller</h3>
    <table><tr><th>#</th><th>Agence</th><th>District</th><th>Présence</th></tr>{rows_p}</table></div>
</div>"""
p4+="</div>"
render("page4_presence", p4)

print("OK — 3 pages generees.")
