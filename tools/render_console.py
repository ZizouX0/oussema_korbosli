# -*- coding: utf-8 -*-
"""Rend la sortie console d'un script en une image pour le rapport.

Le script est réellement exécuté ; sa sortie est capturée telle quelle puis
mise en page dans une image PNG (fenêtre de terminal). Rien n'est saisi à la
main : ce qui figure sur l'image est ce que la commande a produit.

Usage :
    python3 tools/render_console.py <image.png> <commande...>
Exemple :
    python3 tools/render_console.py rapport-latex/images/etl/etl_execution.png \
        python3 etl/etl_agences.py
"""
import os
import subprocess
import sys

import matplotlib
from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOND, BARRE, TEXTE = "#FBFCFE", "#14507A", "#1B2A44"
TAG, BORD, INVITE = "#1B6CA8", "#C9D6E4", "#8FA8C4"
TAILLE, INTERLIGNE, MARGE = 17, 25, 22
POLICE = os.path.join(os.path.dirname(matplotlib.__file__),
                      "mpl-data", "fonts", "ttf", "DejaVuSansMono.ttf")
POLICE_GRAS = os.path.join(os.path.dirname(matplotlib.__file__),
                           "mpl-data", "fonts", "ttf", "DejaVuSansMono-Bold.ttf")


def executer(commande):
    """Exécute la commande depuis la racine du projet et renvoie sa sortie."""
    res = subprocess.run(commande, cwd=RACINE, capture_output=True, text=True)
    sortie = (res.stdout + res.stderr).rstrip("\n")
    if res.returncode != 0:
        print(sortie, file=sys.stderr)
        sys.exit(f"[render] la commande a échoué (code {res.returncode})")
    return sortie


def rendre(sortie, commande, chemin):
    police = ImageFont.truetype(POLICE, TAILLE)
    gras = ImageFont.truetype(POLICE_GRAS, TAILLE)
    invite = "$ " + " ".join(commande)
    lignes = sortie.split("\n")

    largeur_car = police.getlength("0")
    n_col = max([len(l) for l in lignes] + [len(invite)])
    largeur = int(n_col * largeur_car) + 2 * MARGE
    hauteur_barre = INTERLIGNE + 16
    hauteur = hauteur_barre + len(lignes) * INTERLIGNE + 2 * MARGE

    im = Image.new("RGB", (largeur, hauteur), FOND)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, largeur - 1, hauteur_barre], fill=BARRE)
    d.text((MARGE, hauteur_barre / 2), invite, font=gras, fill="#EAF3FA", anchor="lm")

    y = hauteur_barre + MARGE
    for ligne in lignes:
        # le préfixe [étape] est mis en évidence, comme dans la console
        if ligne.startswith("[") and "]" in ligne:
            fin = ligne.index("]") + 1
            d.text((MARGE, y), ligne[:fin], font=gras, fill=TAG)
            d.text((MARGE + police.getlength(ligne[:fin]), y), ligne[fin:],
                   font=police, fill=TEXTE)
        else:
            d.text((MARGE, y), ligne, font=police,
                   fill=INVITE if not ligne.strip() else TEXTE)
        y += INTERLIGNE

    d.rectangle([0, 0, largeur - 1, hauteur - 1], outline=BORD, width=1)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    im.save(chemin)
    print(f"[render] {chemin}  ({largeur}x{hauteur}, {len(lignes)} lignes)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cible, cmd = sys.argv[1], sys.argv[2:]
    rendre(executer(cmd), cmd, os.path.join(RACINE, cible))
