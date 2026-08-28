# -*- coding: utf-8 -*-
"""Génère le cycle CRISP-DM (6 phases) aux couleurs du projet."""
import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = "/home/user/oussema_korbosli/rapport-latex/images/crispdm.png"
NAVY, MID, LITE, BG, EDGE = "#0A2558", "#1D4EA0", "#3C6FC3", "#F4F5FA", "#C9D6EA"

PHASES = [
    ("1", "Compréhension\nmétier",        90),
    ("2", "Compréhension\ndes données",   30),
    ("3", "Préparation\ndes données",    -30),
    ("4", "Modélisation",                -90),
    ("5", "Évaluation",                 -150),
    ("6", "Déploiement",                 150),
]
RX, RY = 1.80, 1.38          # rayons de l'ellipse portant les phases
BW, BH = 0.60, 0.33          # demi-largeur / demi-hauteur des boîtes

fig, ax = plt.subplots(figsize=(9.0, 7.2))
fig.patch.set_facecolor("white")
ax.set_xlim(-2.65, 2.65); ax.set_ylim(-2.15, 2.15)
ax.set_aspect("equal"); ax.axis("off")

# anneau extérieur : caractère itératif du cycle
from matplotlib.patches import Ellipse
ax.add_patch(Ellipse((0, 0), 2 * RX, 2 * RY, fill=False, lw=11, color=BG, zorder=0))

def pos(a):
    r = np.deg2rad(a)
    return RX * np.cos(r), RY * np.sin(r)

# centre : les données
ax.add_patch(Circle((0, 0), 0.40, color=NAVY, zorder=3))
ax.text(0, 0.06, "DONNÉES", ha="center", va="center", color="white",
        fontsize=11, fontweight="bold", zorder=4)
ax.text(0, -0.13, "du réseau BTK", ha="center", va="center", color="#9FB6DC",
        fontsize=8, zorder=4)

# flèches du cycle (sens horaire), le long du cercle
for i in range(6):
    a1 = PHASES[i][2]
    a2 = PHASES[(i + 1) % 6][2]
    p1, p2 = pos(a1), pos(a2)
    # aller-retour entre 1-2 et 3-4 (phases en va-et-vient dans CRISP-DM)
    both = i in (0, 2)
    ax.add_patch(FancyArrowPatch(
        p1, p2, connectionstyle="arc3,rad=-0.28",
        arrowstyle="<|-|>" if both else "-|>",
        mutation_scale=16, lw=2.1, color=LITE, zorder=1,
        shrinkA=46, shrinkB=46))

# boîtes des phases
for num, nom, ang in PHASES:
    x, y = pos(ang)
    ax.add_patch(FancyBboxPatch(
        (x - BW, y - BH), 2 * BW, 2 * BH,
        boxstyle="round,pad=0.02,rounding_size=0.09",
        facecolor="white", edgecolor=MID, lw=1.8, zorder=5))
    ax.add_patch(Circle((x - BW + 0.14, y + BH - 0.12), 0.095,
                        color=NAVY, zorder=6))
    ax.text(x - BW + 0.14, y + BH - 0.125, num, ha="center", va="center",
            color="white", fontsize=8.5, fontweight="bold", zorder=7)
    ax.text(x, y - 0.045, nom, ha="center", va="center", color=NAVY,
            fontsize=10, fontweight="bold", zorder=7, linespacing=1.35)

ax.text(0, 2.02, "Le cycle CRISP-DM", ha="center", va="center",
        color=NAVY, fontsize=15, fontweight="bold")
ax.text(0, -2.0, "Un processus itératif : chaque phase peut ramener à la précédente",
        ha="center", va="center", color="#6B7A90", fontsize=9.5, style="italic")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=170, bbox_inches="tight", facecolor="white", pad_inches=0.15)
print("OK ->", OUT)
