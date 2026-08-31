# -*- coding: utf-8 -*-
"""Version « écran » du diagramme de cas d'utilisation (slide de soutenance).

Même contenu UML que la figure 2.1 du rapport, mais dans des proportions
larges : bulles allongées, libellés sur une seule ligne et typographie
nettement plus grande, pour rester lisible depuis le fond d'une salle.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.path import Path

OUT = "/home/user/oussema_korbosli/presentation/uc_global_slide.png"

NAVY, BORD, LITE = "#14507A", "#1B6CA8", "#7BA3D0"
FILL, BOX = "#EAF3FA", "#FBFCFE"

LABELS = [
    ("employes",  "Gérer les employés"),
    ("objectifs", "Suivre les objectifs commerciaux"),
    ("valider",   "Valider une demande"),
    ("tdb",       "Consulter le tableau de bord"),
    ("roles",     "Gérer les rôles et les droits d'accès"),
    ("agences",   "Gérer les agences"),
    ("clients",   "Gérer les clients"),
    ("audit",     "Consulter le journal d'audit"),
    ("etl",       "Alimenter le datamart (ETL)"),
    ("segment",   "Segmenter les agences"),
    ("soumettre", "Soumettre une demande"),
    ("pointer",   "Pointer la présence (arrivée / départ)"),
    ("notif",     "Recevoir des notifications"),
]
STEP = 1.05
Y = {k: 6.30 - i * STEP for i, (k, _) in enumerate(LABELS)}   # 6.30 .. -6.30

XU, RW, RH = 0.0, 5.00, 0.360         # colonne des cas (bulles larges)
XS, YS, SW, SH = 10.20, 0.0, 2.90, 0.46
XA, YA = -12.60, 0.0                  # administrateur
XD, YD = 17.60, 5.60                  # directeur commercial
XV, YV = 17.60, -5.60                 # utilisateur
BOXL, BOXR, BOXB, BOXT = -6.05, 14.00, -7.40, 7.70

fig, ax = plt.subplots(figsize=(20.0, 9.6))
fig.patch.set_facecolor("#F4F5FA")   # fond identique aux slides
ax.set_xlim(-15.5, 21.6)
ax.set_ylim(-9.2, 8.1)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(FancyBboxPatch(
    (BOXL, BOXB), BOXR - BOXL, BOXT - BOXB,
    boxstyle="round,pad=0.02,rounding_size=0.18",
    facecolor=BOX, edgecolor=BORD, lw=2.0, zorder=0))
ax.text((BOXL + BOXR) / 2, BOXT - 0.52, "Application de gestion des agences bancaires",
        ha="center", va="center", color=NAVY, fontsize=19, fontweight="bold", zorder=1)


def usecase(x, y, label, w=RW, h=RH, fs=14.5):
    ax.add_patch(Ellipse((x, y), 2 * w, 2 * h, facecolor=FILL, edgecolor=BORD,
                         lw=1.9, zorder=3))
    ax.text(x, y, label, ha="center", va="center", color=NAVY, fontsize=fs, zorder=4)


def acteur(x, y, nom):
    s = 0.42
    ax.add_patch(Circle((x, y + 1.05 * s), 0.38 * s, facecolor="white",
                        edgecolor=NAVY, lw=2.3, zorder=4))
    ax.plot([x, x], [y + 0.67 * s, y - 0.58 * s], color=NAVY, lw=2.3, zorder=4)
    ax.plot([x - 0.75 * s, x + 0.75 * s], [y + 0.26 * s, y + 0.26 * s],
            color=NAVY, lw=2.3, zorder=4)
    ax.plot([x, x - 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=2.3, zorder=4)
    ax.plot([x, x + 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=2.3, zorder=4)
    ax.text(x, y - 1.95 * s, nom, ha="center", va="top", color=NAVY,
            fontsize=18, fontweight="bold", zorder=4)


def bord(cx, cy, w, h, vers):
    dx, dy = vers[0] - cx, vers[1] - cy
    n = np.hypot(dx / w, dy / h)
    return (cx + dx / n, cy + dy / n) if n else (cx, cy)


def fleche(p1, p2, rad=0.0, dashed=False, lw=1.5):
    ax.add_patch(FancyArrowPatch(
        p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
        mutation_scale=15, lw=lw, color=LITE if dashed else NAVY,
        linestyle=(0, (5, 3.5)) if dashed else "-",
        shrinkA=0, shrinkB=0, zorder=2))


for k, lab in LABELS:
    usecase(XU, Y[k], lab)
usecase(XS, YS, "S'authentifier", w=SW, h=SH, fs=17.5)

acteur(XA, YA, "Administrateur")
acteur(XD, YD, "Directeur commercial")
acteur(XV, YV, "Utilisateur")

# Administrateur : les 13 cas
for k, _ in LABELS:
    fleche((XA + 0.72, YA), bord(XU, Y[k], RW, RH, (XA, YA)))

# «include» vers « S'authentifier »
for k, _ in LABELS:
    fleche(bord(XU, Y[k], RW, RH, (XS, YS)),
           bord(XS, YS, SW, SH, (XU, Y[k])), dashed=True, lw=1.35)
ax.text(XS, -1.45, "«include»", ha="center", va="center", color=LITE,
        fontsize=16, style="italic", zorder=6)

# Directeur commercial : 5 cas
for k, rad in [("employes", 0.04), ("objectifs", 0.09), ("valider", 0.13), ("tdb", 0.17)]:
    fleche((XD - 0.78, YD - 0.34), bord(XU, Y[k], RW, RH, (XU + 1.6, Y[k] + 2.0)), rad=rad)
ax.text(12.30, 5.40, "consultation", ha="center", va="center", color=NAVY,
        fontsize=15, style="italic", zorder=6,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
ys = Y["soumettre"]
verts = [(XD - 0.30, YD - 2.30),
         (20.3, 0.6), (19.0, -7.0), (12.8, -8.5),
         (8.4, -8.4), (5.7, -6.3), (RW + 0.04, ys - 0.14)]
ax.add_patch(FancyArrowPatch(
    path=Path(verts, [Path.MOVETO] + [Path.CURVE4] * 6), arrowstyle="-|>",
    mutation_scale=15, lw=1.5, color=NAVY, shrinkA=0, shrinkB=0, zorder=2))

# Utilisateur : 3 cas
for k, rad in [("soumettre", -0.20), ("pointer", -0.12), ("notif", -0.05)]:
    fleche((XV - 0.78, YV + 0.34), bord(XU, Y[k], RW, RH, (XU + 2.0, Y[k] - 2.0)), rad=rad)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="#F4F5FA", pad_inches=0.10)
print("OK ->", OUT)
