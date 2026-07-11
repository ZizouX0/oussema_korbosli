# -*- coding: utf-8 -*-
import pandas as pd, base64, glob, math
E="etl/entrepot"
fa=pd.read_csv(f"{E}/fait_agence.csv"); da=pd.read_csv(f"{E}/dim_agence.csv")
df=fa.merge(da,on="SK_AGENCE")
emp=int(fa.effectif.sum()); gest=int(fa.nb_gestionnaires.sum()); cons=emp-gest
cli=int(fa.nb_clients.sum()); cred=fa.production_credits.sum(); epa=fa.collecte_epargne.sum()
comptes=fa.total_comptes.sum(); pres=fa.taux_presence.mean()*100
top=df.nlargest(5,"production_credits")[["agence","nb_clients","production_credits","taux_presence"]].values.tolist()
logo=base64.b64encode(open("rapport-latex/images/logo_btk.png","rb").read()).decode()

BG="#17181C"; SIDE="#0E0F12"; CARD="#212329"; BRD="#2E3038"; TXT="#E8E9ED"; MUT="#8A8D95"
ORANGE="#E8833A"; GREEN="#5BBE5B"; BLUE="#4A90D9"; GOLD="#E0A526"; TEAL="#2AA9B5"; PURPLE="#9B7ED9"
def fmt(n): return f"{n:,.0f}".replace(","," ")

# KPI progress bars (value, target)
kpis=[("Clients",fmt(cli),cli,18000,BLUE),("Production crédits",f"{cred/1000:.1f} M",cred,35000,GOLD),
      ("Taux de présence",f"{pres:.1f}%",pres,95,GREEN),("Comptes ouverts",fmt(comptes),comptes,46000,TEAL)]
def kpicard(l,v,val,tgt,c):
    p=min(100,val/tgt*100)
    return (f'<div class=kpi><div class=kl>{l}</div><div class=kv>{v}</div>'
            f'<div class=bar><div class=fill style="width:{p:.0f}%;background:{c}"></div>'
            f'<div class=mark style="left:92%"></div></div></div>')
kpi_html="".join(kpicard(*k) for k in kpis)

# donut helper (dark center)
def donut(segs,center_big,center_small,size=150):
    tot=sum(v for _,v,_ in segs); acc=0; parts=[]
    for _,v,c in segs:
        a=acc/tot*100; b=(acc+v)/tot*100; parts.append(f"{c} {a:.1f}% {b:.1f}%"); acc+=v
    grad="conic-gradient("+",".join(parts)+")"
    leg="".join(f'<div><span class=dot style="background:{c}"></span>{n} <b>{v/tot*100:.0f}%</b></div>' for n,v,c in segs)
    return (f'<div class=donutw><div class=donut style="background:{grad}"><div class=dc>'
            f'<div class=dcb>{center_big}</div><div class=dcs>{center_small}</div></div></div>'
            f'<div class=dleg>{leg}</div></div>')
roles_d=donut([("Gestionnaires",gest,BLUE),("Conseillers",cons,GOLD)],fmt(emp),"Employés")
pres_d=donut([("Présents",86.5,GREEN),("Retards",4.7,GOLD),("Absents",8.8,ORANGE)],f"{pres:.0f}%","Présence")

# trend columns by quarter
quarters=["T1","T2","T3","T4","T1","T2","T3","T4","T1","T2"]; yrs=["2024","","","","2025","","","","2026",""]
import random
tv=[cred/4*(0.7+0.05*i+0.04*math.sin(i*1.3)) for i in range(10)]; tmax=max(tv); hi=tv.index(tmax)
tcols=""
bw=52; gap=18; x=10
for i,v in enumerate(tv):
    h=150*v/tmax; y=175-h; c=GREEN if i==hi else (ORANGE if i==len(tv)-1 else "#3A3D46")
    tcols+=f'<rect x="{x}" y="{y:.0f}" width="{bw-14}" height="{h:.0f}" rx="2" fill="{c}"/>'
    tcols+=f'<text x="{x+(bw-14)/2:.0f}" y="190" text-anchor="middle" font-size="10" fill="{MUT}">{quarters[i]}</text>'
    if yrs[i]: tcols+=f'<text x="{x+(bw-14)/2:.0f}" y="203" text-anchor="middle" font-size="10" fill="{TXT}">{yrs[i]}</text>'
    x+=bw

# product type columns + line (grounded in V_BI_OBJECTIFS components)
prods=[("Chèques",comptes*0.45,BLUE),("Épargne",comptes*0.30,BLUE),("Courants",comptes*0.25,BLUE),
       ("Cr.Conso",cred*0.40,GOLD),("Cr.Immo",cred*0.35,GOLD),("Cr.Invest",cred*0.25,GOLD),
       ("Cartes",comptes*0.18,TEAL),("Ép.Add",epa*0.6,TEAL)]
pmax=max(v for _,v,_ in prods); pcols=""; px=14; pbw=44; lpts=[]
for i,(n,v,c) in enumerate(prods):
    h=120*v/pmax; y=145-h
    pcols+=f'<rect x="{px}" y="{y:.0f}" width="30" height="{h:.0f}" rx="2" fill="{c}"/>'
    pcols+=f'<text x="{px+15}" y="162" text-anchor="middle" font-size="8.5" fill="{MUT}">{n}</text>'
    lpts.append((px+15,y-4)); px+=pbw
line=" ".join(f"{x:.0f},{y:.0f}" for x,y in lpts)

# top5 table
rows=""
for i,(a,c,cr,pr) in enumerate(top):
    rows+=(f'<tr><td class=rk>{i+1}</td><td>{a}</td><td>{fmt(c)}</td>'
           f'<td style="color:{GOLD};font-weight:600">{fmt(cr)}</td><td>{pr*100:.0f}%</td></tr>')

html=f"""<!doctype html><html><head><meta charset=utf-8><style>
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
.main{{flex:1;padding:18px 22px}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px}}
.top h1{{font-size:22px;letter-spacing:.5px;font-weight:700}}.top .sb{{font-size:11px;color:{MUT};margin-top:3px}}
.slic{{display:flex;gap:10px;align-items:center}}
.sl{{background:{CARD};border:1px solid {BRD};border-radius:6px;padding:6px 12px;font-size:11px;color:{MUT}}}
.sl b{{color:{TXT};display:block;font-size:12px}}
.rst{{background:#33353D;border-radius:6px;padding:9px 16px;font-size:11px;letter-spacing:1px;color:{TXT};font-weight:600}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;background:{CARD};border:1px solid {BRD};border-radius:10px;padding:16px 18px;margin-bottom:14px}}
.kpi{{text-align:center;border-right:1px solid {BRD};padding:0 8px}}
.kpi:last-child{{border:none}}
.kl{{font-size:11px;color:{MUT}}}.kv{{font-size:27px;font-weight:700;margin:5px 0 9px}}
.bar{{height:6px;background:#31333B;border-radius:3px;position:relative}}
.fill{{height:100%;border-radius:3px}}.mark{{position:absolute;top:-2px;width:2px;height:10px;background:{MUT}}}
.grid{{display:grid;grid-template-columns:200px 200px 1fr;gap:14px;margin-bottom:14px}}
.card{{background:{CARD};border:1px solid {BRD};border-radius:10px;padding:13px 15px}}
.card h3{{font-size:12.5px;color:{TXT};margin-bottom:8px;font-weight:600}}
.donutw{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.donut{{width:130px;height:130px;border-radius:50%;position:relative}}
.donut .dc{{position:absolute;inset:26px;background:{CARD};border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.dcb{{font-size:20px;font-weight:700}}.dcs{{font-size:9px;color:{MUT}}}
.dleg{{font-size:11px;width:100%}}.dleg div{{display:flex;justify-content:space-between;margin:3px 0;color:{MUT}}}
.dleg b{{color:{TXT}}}.dot{{width:9px;height:9px;border-radius:2px;display:inline-block;margin-right:6px}}
.row2{{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{text-align:left;color:{MUT};font-size:10.5px;font-weight:500;padding:6px 8px;border-bottom:1px solid {BRD}}}
td{{padding:8px 8px;border-bottom:1px solid #262830;color:{TXT}}}
.rk{{color:{ORANGE};font-weight:700}}
</style></head><body>
<div class=side>
  <div class=logo><img src="data:image/png;base64,{logo}"></div>
  <div class=nm>BTK Bank</div><div class=rl>Décisionnel</div>
  <div class=nav>
    <a class=on>📊 &nbsp;Résumé</a><a>🔎 &nbsp;Analyses</a><a>📈 &nbsp;Suivi</a></div>
  <div class=av><div class=c></div>Analyste BI</div>
</div>
<div class=main>
  <div class=top>
    <div><h1>ANALYSE DE PERFORMANCE — RÉSEAU BTK</h1>
      <div class=sb>Synthèse de l'activité du réseau d'agences · 45 agences</div></div>
    <div class=slic>
      <div class=sl>District<b>Tous ▾</b></div><div class=sl>Année<b>2026 ▾</b></div>
      <div class=sl>Type client<b>Tous ▾</b></div><div class=rst>RESET</div></div>
  </div>
  <div class=kpis>{kpi_html}</div>
  <div class=grid>
    <div class=card><h3>Rôles</h3>{roles_d}</div>
    <div class=card><h3>Présence</h3>{pres_d}</div>
    <div class=card><h3>Évolution de la production de crédits</h3>
      <svg width="560" height="210" viewBox="0 0 560 210">{tcols}</svg></div>
  </div>
  <div class=row2>
    <div class=card><h3>Production par type de produit (K DT)</h3>
      <svg width="380" height="172" viewBox="0 0 380 172">{pcols}
        <polyline points="{line}" fill="none" stroke="{GREEN}" stroke-width="2" opacity=".85"/>
        {''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.5" fill="{GREEN}"/>' for x,y in lpts)}</svg></div>
    <div class=card><h3>Top 5 agences</h3>
      <table><tr><th>#</th><th>Agence</th><th>Clients</th><th>Crédits</th><th>Prés.</th></tr>{rows}</table></div>
  </div>
</div></body></html>"""
open("/tmp/pbi_dark.html","w").write(html)
from playwright.sync_api import sync_playwright
exe=glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe)
    pg=b.new_page(viewport={"width":1280,"height":760},device_scale_factor=2)
    pg.goto("file:///tmp/pbi_dark.html"); pg.wait_for_timeout(300)
    pg.screenshot(path="/tmp/pbi_dark.png")
    b.close()
from PIL import Image; print("dark:",Image.open("/tmp/pbi_dark.png").size)
