# -*- coding: utf-8 -*-
"""Génère le diagramme de cas d'utilisation global (figure 2.1).

Le rendu reprend la présentation PlantUML habituelle — acteurs à gauche, cas
d'utilisation en colonne, « S'authentifier » à droite, associations en traits
pleins et relations «include» en pointillés — mais le placement est maîtrisé,
ce que le moteur graphviz ne permet pas : celui-ci centre systématiquement
l'acteur relié aux treize cas, alors que l'administrateur doit figurer en haut.

Ordre retenu : administrateur en haut, directeur commercial au milieu,
utilisateur en bas ; chaque acteur est placé à la hauteur moyenne des cas
auxquels il est associé, ce qui évite les croisements inutiles.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch, Circle

OUT = "/home/user/oussema_korbosli/rapport-latex/diagrams/uc_global.png"

# palette identique à celle du rendu PlantUML du rapport
NAVY, BORD, LITE = "#14507A", "#1B6CA8", "#4A7FB5"
FILL, BOX, ACT = "#EAF3FA", "#FBFCFE", "#EAF3FA"

# --------------------------------------------------------- cas d'utilisation
# ordre : cas propres à l'administrateur, puis ceux partagés avec le directeur
# commercial, puis ceux partagés avec l'utilisateur.
LABELS = [
    ("roles",     "Gérer les rôles et\nles droits d'accès"),
    ("agences",   "Gérer les agences"),
    ("clients",   "Gérer les clients"),
    ("audit",     "Consulter le\njournal d'audit"),
    ("etl",       "Alimenter le\ndatamart (ETL)"),
    ("segment",   "Segmenter\nles agences"),
    ("employes",  "Gérer les employés"),
    ("objectifs", "Suivre les objectifs\ncommerciaux"),
    ("valider",   "Valider une\ndemande"),
    ("tdb",       "Consulter le\ntableau de bord"),
    ("soumettre", "Soumettre une\ndemande"),
    ("pointer",   "Pointer la présence\n(arrivée / départ)"),
    ("notif",     "Recevoir des\nnotifications"),
]
STEP = 2.45
Y = {k: 14.70 - i * STEP for i, (k, _) in enumerate(LABELS)}

XU, RW, RH = 0.0, 3.55, 0.85             # colonne des cas d'utilisation
XS, SW, SH = 8.90, 2.55, 0.82           # « S'authentifier »
YS = 14.70 - 6 * STEP                    # centré sur la colonne
XACT = -10.00                            # abscisse commune aux trois acteurs
XLAB = 5.10                              # colonne des étiquettes «include»

# associations acteur -> cas d'utilisation
ADM = [k for k, _ in LABELS]
DIR = ["employes", "objectifs", "valider", "tdb", "soumettre"]
USR = ["soumettre", "pointer", "notif"]

# chaque acteur est placé à la hauteur moyenne des cas qui lui sont associés,
# l'administrateur étant remonté en tête du diagramme.
YACT = {
    "ADM": Y["agences"],
    "DIR": float(np.mean([Y[k] for k in DIR])),
    "USR": float(np.mean([Y[k] for k in USR])),
}

BOXL, BOXR = -5.60, 12.50
BOXB, BOXT = Y["notif"] - 1.90, Y["roles"] + 3.30

fig, ax = plt.subplots(figsize=(11.0, 14.0))
fig.patch.set_facecolor("white")
ax.set_xlim(-13.10, 13.00)
ax.set_ylim(BOXB - 0.6, BOXT + 0.5)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(FancyBboxPatch(
    (BOXL, BOXB), BOXR - BOXL, BOXT - BOXB,
    boxstyle="round,pad=0.02,rounding_size=0.18",
    facecolor=BOX, edgecolor=BORD, lw=1.6, zorder=0))
ax.text((BOXL + BOXR) / 2, BOXT - 1.10, "Application de gestion des agences bancaires",
        ha="center", va="center", color=NAVY, fontsize=14, fontweight="bold", zorder=1)


def usecase(x, y, label, w=RW, h=RH, fs=14):
    ax.add_patch(Ellipse((x, y), 2 * w, 2 * h, facecolor=FILL, edgecolor=BORD,
                         lw=1.4, zorder=3))
    ax.text(x, y, label, ha="center", va="center", color="#1B2A44", fontsize=fs,
            zorder=4, linespacing=1.25)


def acteur(x, y, nom):
    """Pictogramme « awesome » : tête et buste, comme le rendu PlantUML."""
    s = 0.70
    ax.add_patch(FancyBboxPatch(
        (x - 0.95 * s, y - 0.62 * s), 1.90 * s, 0.86 * s,
        boxstyle="round,pad=0.02,rounding_size=0.28",
        facecolor=ACT, edgecolor=NAVY, lw=1.6, zorder=4))
    ax.add_patch(Circle((x, y + 0.72 * s), 0.62 * s, facecolor=ACT,
                        edgecolor=NAVY, lw=1.6, zorder=5))
    ax.text(x, y - 1.15 * s, nom, ha="center", va="top", color="#12324F",
            fontsize=15, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))


def bord(cx, cy, w, h, vers):
    """Point du contour de l'ellipse (cx, cy) dans la direction de « vers »."""
    dx, dy = vers[0] - cx, vers[1] - cy
    n = np.hypot(dx / w, dy / h)
    return (cx + dx / n, cy + dy / n) if n else (cx, cy)


def assoc(x_act, y_act, cle):
    """Association acteur — cas d'utilisation.

    En UML, une association est un simple trait : elle ne porte pas de pointe
    de flèche, contrairement à la dépendance «include».
    """
    depart = (x_act + 0.80, y_act)
    arrivee = bord(XU, Y[cle], RW, RH, depart)
    ax.plot([depart[0], arrivee[0]], [depart[1], arrivee[1]],
            color=NAVY, lw=1.15, solid_capstyle="round", zorder=2)


# ------------------------------------------------------------- les 14 bulles
for k, lab in LABELS:
    usecase(XU, Y[k], lab)
usecase(XS, YS, "S'authentifier", w=SW, h=SH, fs=15)

acteur(XACT, YACT["ADM"], "Administrateur")
acteur(XACT, YACT["DIR"], "Directeur commercial")
acteur(XACT, YACT["USR"], "Utilisateur")

# ------------------- «include» : les 13 cas vers « S'authentifier »
for k, _ in LABELS:
    a = bord(XU, Y[k], RW, RH, (XS, YS))
    b = bord(XS, YS, SW, SH, (XU, Y[k]))
    # dépendance «include» : trait pointillé terminé par une flèche ouverte
    ax.add_patch(FancyArrowPatch(
        a, b, arrowstyle="->", mutation_scale=15, lw=1.0, color=LITE,
        linestyle=(0, (5, 3.5)), shrinkA=0, shrinkB=0, zorder=2))
    # étiquette du stéréotype, alignée en colonne entre les deux ellipses
    t = (XLAB - a[0]) / (b[0] - a[0])
    ax.text(XLAB, a[1] + (b[1] - a[1]) * t, "«include»", ha="center", va="center",
            color=LITE, fontsize=12, zorder=6,
            bbox=dict(boxstyle="round,pad=0.10", fc="white", ec="none"))

# ------------------------------------------------- associations des acteurs
for k in ADM:
    assoc(XACT, YACT["ADM"], k)
for k in DIR:
    assoc(XACT, YACT["DIR"], k)
for k in USR:
    assoc(XACT, YACT["USR"], k)

# rôle porté par l'association « directeur commercial -> gérer les employés »
xm = XACT + (XU - RW - XACT) * 0.55
ym = YACT["DIR"] + (Y["employes"] - YACT["DIR"]) * 0.55
ax.text(xm, ym + 0.22, "consultation", ha="center", va="bottom", color=NAVY,
        fontsize=13, zorder=6,
        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=170, bbox_inches="tight", facecolor="white", pad_inches=0.10)
print("OK ->", OUT)
