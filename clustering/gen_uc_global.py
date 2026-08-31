# -*- coding: utf-8 -*-
"""Génère le diagramme de cas d'utilisation global (figure 2.1).

Le placement est maîtrisé à la main afin d'obtenir un tracé lisible :
  - l'administrateur à gauche, ses 13 associations en éventail ;
  - « S'authentifier » à droite, relié aux 13 cas par une relation «include» ;
  - le directeur commercial en haut à droite et l'utilisateur en bas à droite,
    chacun en vis-à-vis des cas d'utilisation qui le concernent.
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

# ------------------------------------------------------------- cas d'utilisation
# ordonnés pour rapprocher chaque cas de l'acteur qui le déclenche
LABELS = [
    ("employes",  "Gérer les employés"),
    ("objectifs", "Suivre les objectifs\ncommerciaux"),
    ("valider",   "Valider une demande"),
    ("tdb",       "Consulter le\ntableau de bord"),
    ("roles",     "Gérer les rôles et\nles droits d'accès"),
    ("agences",   "Gérer les agences"),
    ("clients",   "Gérer les clients"),
    ("audit",     "Consulter le\njournal d'audit"),
    ("etl",       "Alimenter le\ndatamart (ETL)"),
    ("segment",   "Segmenter les agences"),
    ("soumettre", "Soumettre une demande"),
    ("pointer",   "Pointer la présence\n(arrivée / départ)"),
    ("notif",     "Recevoir des\nnotifications"),
]
STEP = 1.20
Y = {k: 7.20 - i * STEP for i, (k, _) in enumerate(LABELS)}   # 7.20 .. -7.20

XU, RW, RH = 0.0, 2.20, 0.46          # colonne des cas
XS, YS, SW, SH = 5.55, 0.0, 1.80, 0.48  # « S'authentifier »
XA, YA = -8.9, 0.0                    # administrateur
XD, YD = 10.6, 6.8                    # directeur commercial
XV, YV = 10.6, -6.8                   # utilisateur
BOXL, BOXR, BOXB, BOXT = -2.80, 7.75, -8.35, 8.35

fig, ax = plt.subplots(figsize=(16.2, 12.6))
fig.patch.set_facecolor("white")
ax.set_xlim(-11.3, 14.9)
ax.set_ylim(-9.0, 9.3)
ax.set_aspect("equal")
ax.axis("off")

# ------------------------------------------------------------ frontière système
ax.add_patch(FancyBboxPatch(
    (BOXL, BOXB), BOXR - BOXL, BOXT - BOXB,
    boxstyle="round,pad=0.02,rounding_size=0.20",
    facecolor=BOX, edgecolor=BORD, lw=1.7, zorder=0))
ax.text((BOXL + BOXR) / 2, BOXT - 0.48, "Application de gestion des agences bancaires",
        ha="center", va="center", color=NAVY, fontsize=14, fontweight="bold", zorder=1)


def usecase(x, y, label, w=RW, h=RH, fs=11.5):
    ax.add_patch(Ellipse((x, y), 2 * w, 2 * h, facecolor=FILL, edgecolor=BORD,
                         lw=1.5, zorder=3))
    ax.text(x, y, label, ha="center", va="center", color=NAVY, fontsize=fs,
            zorder=4, linespacing=1.22)


def acteur(x, y, nom, va="top"):
    s = 0.34
    ax.add_patch(Circle((x, y + 1.05 * s), 0.38 * s, facecolor="white",
                        edgecolor=NAVY, lw=1.8, zorder=4))
    ax.plot([x, x], [y + 0.67 * s, y - 0.58 * s], color=NAVY, lw=1.8, zorder=4)
    ax.plot([x - 0.75 * s, x + 0.75 * s], [y + 0.26 * s, y + 0.26 * s],
            color=NAVY, lw=1.8, zorder=4)
    ax.plot([x, x - 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=1.8, zorder=4)
    ax.plot([x, x + 0.62 * s], [y - 0.58 * s, y - 1.50 * s], color=NAVY, lw=1.8, zorder=4)
    ax.text(x, y - 1.95 * s, nom, ha="center", va="top", color=NAVY,
            fontsize=12.5, fontweight="bold", zorder=4)


def bord(cx, cy, w, h, vers):
    """Point du bord de l'ellipse dans la direction de `vers`."""
    dx, dy = vers[0] - cx, vers[1] - cy
    n = np.hypot(dx / w, dy / h)
    return (cx + dx / n, cy + dy / n) if n else (cx, cy)


def fleche(p1, p2, rad=0.0, dashed=False, lw=1.2):
    ax.add_patch(FancyArrowPatch(
        p1, p2, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
        mutation_scale=12, lw=lw, color=LITE if dashed else NAVY,
        linestyle=(0, (5, 3.5)) if dashed else "-",
        shrinkA=0, shrinkB=0, zorder=2))


# --------------------------------------------------------------- les 14 bulles
for k, lab in LABELS:
    usecase(XU, Y[k], lab)
usecase(XS, YS, "S'authentifier", w=SW, h=SH, fs=12)

acteur(XA, YA, "Administrateur")
acteur(XD, YD, "Directeur commercial")
acteur(XV, YV, "Utilisateur")

# ------------------- Administrateur : les 13 cas (éventail, sans croisement)
for k, _ in LABELS:
    fleche((XA + 0.60, YA), bord(XU, Y[k], RW, RH, (XA, YA)))

# ------------------- «include» : les 13 cas vers « S'authentifier »
for k, _ in LABELS:
    p1 = bord(XU, Y[k], RW, RH, (XS, YS))
    p2 = bord(XS, YS, SW, SH, (XU, Y[k]))
    fleche(p1, p2, dashed=True, lw=1.05)
ax.text(3.02, 0.24, "«include»", ha="center", color=LITE,
        fontsize=11, style="italic", zorder=6, va="bottom")

# ------------------- Directeur commercial : 5 cas
#   les quatre premiers sont abordés par le haut de la bulle : le tracé passe
#   au-dessus du faisceau «include» sans jamais le croiser
for k, rad in [("employes", 0.04), ("objectifs", 0.09), ("valider", 0.13), ("tdb", 0.17)]:
    cible = bord(XU, Y[k], RW, RH, (XU + 1.05, Y[k] + 2.0))
    fleche((XD - 0.62, YD - 0.28), cible, rad=rad)
ax.text(7.35, 6.28, "consultation", ha="center", va="center", color=NAVY,
        fontsize=10.5, style="italic", zorder=6,
        bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none"))

#   « Soumettre une demande » : contournement par la droite, hors de la
#   frontière du système, pour n'entrer dans aucune autre bulle
ys = Y["soumettre"]
verts = [(XD + 0.15, YD - 1.55),
         (13.4, 4.2), (13.4, -4.4), (11.2, -5.05),   # couloir vertical à droite
         (8.6, -5.6), (5.2, -5.35), (RW + 0.03, ys - 0.16)]
codes = [Path.MOVETO] + [Path.CURVE4] * 6
ax.add_patch(FancyArrowPatch(
    path=Path(verts, codes), arrowstyle="-|>", mutation_scale=12,
    lw=1.2, color=NAVY, shrinkA=0, shrinkB=0, zorder=2))

# ------------------- Utilisateur : 3 cas (abordés par le bas de la bulle)
for k, rad in [("soumettre", -0.20), ("pointer", -0.12), ("notif", -0.05)]:
    cible = bord(XU, Y[k], RW, RH, (XU + 1.35, Y[k] - 1.9))
    fleche((XV - 0.62, YV + 0.30), cible, rad=rad)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=190, bbox_inches="tight", facecolor="white", pad_inches=0.12)
print("OK ->", OUT)
