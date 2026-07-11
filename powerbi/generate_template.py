# -*- coding: utf-8 -*-
# Génère l'IMAGE DE FOND (template) Power BI : canvas sombre + sidebar + zones de cartes vides.
import base64, glob
logo=base64.b64encode(open("rapport-latex/images/logo_btk.png","rb").read()).decode()
BG="#17181C"; SIDE="#0E0F12"; CARD="#212329"; BRD="#2E3038"; TXT="#E8E9ED"; MUT="#8A8D95"; ORANGE="#E8833A"

def zone(title,hint):
    return (f'<div class=card><div class=ct>{title}</div>'
            f'<div class=hint>{hint}</div></div>')

html=f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,sans-serif}}
body{{width:1280px;height:720px;background:{BG};display:flex;color:{TXT}}}
.side{{width:172px;background:{SIDE};display:flex;flex-direction:column;align-items:center;padding:22px 0;border-right:1px solid {BRD}}}
.logo{{width:78px;height:78px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;margin-bottom:6px}}
.logo img{{width:60px}}
.nm{{font-size:13px;font-weight:600;margin-top:4px}}.rl{{font-size:10px;color:{MUT};margin-bottom:26px}}
.nav{{width:100%;padding:0 14px}}
.nav a{{display:flex;gap:10px;align-items:center;padding:11px 14px;font-size:13px;color:{MUT};border-radius:7px;margin-bottom:4px}}
.nav a.on{{background:{CARD};color:{TXT}}}
.av{{margin-top:auto;text-align:center;color:{MUT};font-size:11px}}.av .c{{width:34px;height:34px;border-radius:50%;background:{ORANGE};margin:0 auto 5px}}
.main{{flex:1;padding:18px 22px}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px}}
.top h1{{font-size:22px;letter-spacing:.5px;font-weight:700}}.top .sb{{font-size:11px;color:{MUT};margin-top:3px}}
.slic{{display:flex;gap:10px;align-items:center}}
.sl{{background:{CARD};border:1px solid {BRD};border-radius:6px;padding:6px 12px;font-size:11px;color:{MUT};min-width:74px}}
.rst{{background:#33353D;border-radius:6px;padding:9px 16px;font-size:11px;letter-spacing:1px;color:{TXT};font-weight:600}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:0;background:{CARD};border:1px solid {BRD};border-radius:10px;padding:16px 18px;margin-bottom:14px;height:96px}}
.kpi{{border-right:1px dashed {BRD};display:flex;align-items:center;justify-content:center;color:{MUT};font-size:11px}}
.kpi:last-child{{border:none}}
.grid{{display:grid;grid-template-columns:200px 200px 1fr;gap:14px;margin-bottom:14px}}
.card{{background:{CARD};border:1px solid {BRD};border-radius:10px;padding:13px 15px;position:relative}}
.ct{{font-size:12.5px;color:{TXT};font-weight:600}}
.hint{{position:absolute;inset:32px 0 12px 0;display:flex;align-items:center;justify-content:center;color:#4a4d57;font-size:11px;border:1px dashed #33363F;border-radius:8px;margin:0 14px}}
.g1 .card{{height:340px}}
.row2{{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}}
.row2 .card{{height:250px}}
</style></head><body>
<div class=side>
  <div class=logo><img src="data:image/png;base64,{logo}"></div>
  <div class=nm>BTK Bank</div><div class=rl>Décisionnel</div>
  <div class=nav><a class=on>📊 &nbsp;Résumé</a><a>🔎 &nbsp;Analyses</a><a>📈 &nbsp;Suivi</a></div>
  <div class=av><div class=c></div>Analyste BI</div>
</div>
<div class=main>
  <div class=top>
    <div><h1>ANALYSE DE PERFORMANCE — RÉSEAU BTK</h1>
      <div class=sb>Synthèse de l'activité du réseau d'agences</div></div>
    <div class=slic><div class=sl>District ▾</div><div class=sl>Année ▾</div><div class=sl>Type ▾</div><div class=rst>RESET</div></div>
  </div>
  <div class=kpis><div class=kpi>KPI — Clients</div><div class=kpi>KPI — Crédits</div><div class=kpi>KPI — Présence</div><div class=kpi>KPI — Comptes</div></div>
  <div class="grid g1">
    {zone("Rôles","Donut")}{zone("Présence","Donut")}{zone("Évolution de la production","Histogramme")}
  </div>
  <div class=row2>{zone("Production par type de produit","Colonnes + courbe")}{zone("Top 5 agences","Tableau")}</div>
</div></body></html>"""
open("/tmp/pbi_template.html","w").write(html)
from playwright.sync_api import sync_playwright
exe=glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome')[0]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=exe)
    pg=b.new_page(viewport={"width":1280,"height":720},device_scale_factor=2)
    pg.goto("file:///tmp/pbi_template.html"); pg.wait_for_timeout(300)
    pg.screenshot(path="/tmp/pbi_template_bg.png")
    b.close()
from PIL import Image; print("template bg:",Image.open("/tmp/pbi_template_bg.png").size)
