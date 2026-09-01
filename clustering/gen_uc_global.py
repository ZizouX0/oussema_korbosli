# -*- coding: utf-8 -*-
"""Génère le diagramme de cas d'utilisation global (figure 2.1).

Parti pris de tracé, pour que chaque association reste lisible :
  - les trois acteurs sont alignés à gauche et nettement espacés ;
  - chaque acteur dispose de son propre couloir vertical, celui de
    l'administrateur étant le plus proche des cas d'utilisation : ses treize
    associations ne croisent donc aucune autre ;
  - les associations sont tracées à angle droit, les rares croisements étant
    perpendiculaires, donc immédiatement lisibles ;
  - les relations «include» restent en diagonale pointillée vers
    « S'authentifier » : rien ne traverse ce faisceau.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.path import Path

OUT = "/home/user/oussema_korbosli/rapport-latex/diagrams/uc_global.png"

NAVY, BORD, LITE = "#14507A", "#1B6CA8", "#6C97C9"
FILL, BOX = "#EAF3FA", "#FBFCFE"

# --------------------------------------------------------- cas d'utilisation
# ordre : cas propres à l'administrateur, puis ceux du directeur commercial,
# puis ceux de l'utilisateur ; « Soumettre une demande » est à la charnière.
LABELS = [
    ("roles",     "Gérer les rôles et\nles droits d'accès"),
    ("agences",   "Gérer les agences"),
    ("clients",   "Gérer les clients"),
    ("audit",     "Consulter le\njournal d'audit"),
    ("etl",       "Alimenter le\ndatamart (ETL)"),
    ("segment",   "Segmenter les agences"),
    ("employes",  "Gérer les employés"),
    ("objectifs", "Suivre les objectifs\ncommerciaux"),
    ("valider",   "Valider une demande"),
    ("tdb",       "Consulter le\ntableau de bord"),
    ("soumettre", "Soumettre une demande"),
    ("pointer",   "Pointer la présence\n(arrivée / départ)"),
    ("notif",     "Recevoir des\nnotifications"),
]
STEP = 1.10
Y = {k: 6.60 - i * STEP for i, (k, _) in enumerate(LABELS)}

XU, RW, RH = 0.0, 2.40, 0.45            # colonne des cas d'utilisation
XS, YS, SW, SH = 7.30, 0.0, 1.95, 0.50  # « S'authentifier »
XACT = -9.80                            # abscisse commune aux trois acteurs
LANE = {"ADM": -4.70, "DIR": -6.15, "USR": -7.60}   # couloirs verticaux
YACT = {"ADM": 5.30, "DIR": -2.20, "USR": -5.90}    # acteurs bien espacés
BOXL, BOXR, BOXB, BOXT = -3.10, 9.60, -7.55, 8.05

fig, ax = plt.subplots(figsize=(16.0, 12.4))
fig.patch.set_facecolor("white")
ax.set_xlim(-11.6, 10.1)
ax.set_ylim(-8.3, 8.5)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(FancyBboxPatch(
    (BOXL, BOXB), BOXR - BOXL, BOXT - BOXB,
    boxstyle="round,pad=0.02,rounding_size=0.20",
    facecolor=BOX, edgecolor=BORD, lw=1.7, zorder=0))
ax.text((BOXL + BOXR) / 2, BOXT - 0.45, "Application de gestion des agences bancaires",
        ha="center", va="center", color=NAVY, fontsize=14, fontweight="bold", zorder=1)


def usecase(x, y, label, w=RW, h=RH, fs=11.5):
    ax.add_patch(Ellipse((x, y), 2 * w, 2 * h, facecolor=FILL, edgecolor=BORD,
                         lw=1.5, zorder=3))
    ax.text(x, y, label, ha="center", va="center", color=NAVY, fontsize=fs,
            zorder=4, linespacing=1.22)


def acteur(x, y, nom):
    s = 0.36
    ax.add_patch(Circle((x, y + 1.05 * s), 0.38 * s, facecolor="white",
                        edgecolor=NAVY, lw=1.9, zorder=4))
    ax.plot([x, x], [y + 0.67 * s, y - 0.58 * s], color=NAVY, lw=1.9, zorder=4)
    ax.plot([x - 0.75 * s, x + 0.75 * s], [y + 0.26 * s, y + 0.26 * s],
            color=NAVY, lw=1.9, zorder=4)
    ax.plot([x, x - 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=1.9, zorder=4)
    ax.plot([x, x + 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=1.9, zorder=4)
    ax.text(x, y - 1.95 * s, nom, ha="center", va="top", color=NAVY,
            fontsize=12.5, fontweight="bold", zorder=4)


def bord(cx, cy, w, h, vers):
    dx, dy = vers[0] - cx, vers[1] - cy
    n = np.hypot(dx / w, dy / h)
    return (cx + dx / n, cy + dy / n) if n else (cx, cy)


def assoc(acteur_cle, cle_cas, dy=0.0):
    """Association acteur -> cas d'utilisation, tracée à angle droit."""
    xl, ya = LANE[acteur_cle], YACT[acteur_cle]
    yc = Y[cle_cas] + dy
    xe = XU - RW * np.sqrt(max(0.0, 1 - (dy / RH) ** 2))   # bord de l'ellipse
    verts = [(XACT + 0.62, ya), (xl, ya), (xl, yc), (xe, yc)]
    ax.add_patch(FancyArrowPatch(
        path=Path(verts, [Path.MOVETO] + [Path.LINETO] * 3),
        arrowstyle="-|>", mutation_scale=12, lw=1.25, color=NAVY,
        shrinkA=0, shrinkB=0, zorder=2, joinstyle="miter"))


# ------------------------------------------------------------- les 14 bulles
for k, lab in LABELS:
    usecase(XU, Y[k], lab)
usecase(XS, YS, "S'authentifier", w=SW, h=SH, fs=12)

acteur(XACT, YACT["ADM"], "Administrateur")
acteur(XACT, YACT["DIR"], "Directeur commercial")
acteur(XACT, YACT["USR"], "Utilisateur")

# ------------------- «include» : les 13 cas vers « S'authentifier »
for k, _ in LABELS:
    ax.add_patch(FancyArrowPatch(
        bord(XU, Y[k], RW, RH, (XS, YS)), bord(XS, YS, SW, SH, (XU, Y[k])),
        arrowstyle="-|>", mutation_scale=12, lw=1.05, color=LITE,
        linestyle=(0, (5, 3.5)), shrinkA=0, shrinkB=0, zorder=2))
ax.text(3.80, 0.22, "«include»", ha="center", va="bottom", color=LITE,
        fontsize=11.5, style="italic", zorder=6)

# ------- associations : décalées quand plusieurs acteurs partagent un cas ---
SEUL, DUO, TRIO = 0.0, 0.17, 0.24
for k in ["roles", "agences", "clients", "audit", "etl", "segment"]:
    assoc("ADM", k, SEUL)
for k in ["employes", "objectifs", "valider", "tdb"]:
    assoc("ADM", k, +DUO)
    assoc("DIR", k, -DUO)
assoc("ADM", "soumettre", +TRIO)
assoc("DIR", "soumettre", 0.0)
assoc("USR", "soumettre", -TRIO)
for k in ["pointer", "notif"]:
    assoc("ADM", k, +DUO)
    assoc("USR", k, -DUO)

ax.text(-3.55, Y["employes"] - DUO, "consultation", ha="center", va="center",
        color=NAVY, fontsize=10.5, style="italic", zorder=6,
        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=190, bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("OK ->", OUT)
