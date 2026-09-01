# Exécuter le volet décisionnel dans Anaconda (Jupyter)

Deux notebooks reproduisent, pas à pas et avec leurs résultats, la chaîne ETL et
la segmentation des agences :

| Notebook | Ce qu'il produit |
|---|---|
| `etl/etl_btk.ipynb` | le datamart en étoile (`etl/entrepot/`) et `clustering/data/agences.csv` |
| `clustering/segmentation_btk.ipynb` | le choix de *k*, la comparaison des quatre modèles, la projection ACP et les profils des segments |

Chacun se termine par une **cellule de vérification** qui relance le script
correspondant (`etl/etl_agences.py`, `clustering/segmentation_reelle.py`) et
compare : si les résultats diffèrent, la cellule échoue.

---

## Étape 1 — Ouvrir le projet dans Jupyter

**Avec Anaconda Navigator**

1. Ouvrir **Anaconda Navigator**.
2. Cliquer sur **Launch** sous *JupyterLab* (ou *Jupyter Notebook*).
3. Dans l'arborescence, naviguer jusqu'au dossier du projet.

**Avec l'invite Anaconda** (plus direct)

```bash
cd C:\chemin\vers\oussema_korbosli     # Windows
cd ~/oussema_korbosli                  # macOS / Linux
jupyter lab                            # ou : jupyter notebook
```

> Peu importe le dossier depuis lequel Jupyter est lancé : la première cellule
> remonte l'arborescence jusqu'à la racine du projet et l'affiche.

## Étape 2 — Vérifier les bibliothèques

Anaconda installe déjà tout ce qui est nécessaire. Pour s'en assurer, dans une
cellule :

```python
import pandas, numpy, sklearn, matplotlib
print(pandas.__version__, numpy.__version__, sklearn.__version__, matplotlib.__version__)
```

En cas de manque, dans l'invite Anaconda : `conda install pandas numpy scikit-learn matplotlib`.

## Étape 3 — Lancer la chaîne ETL

1. Ouvrir **`etl/etl_btk.ipynb`**.
2. Menu **Kernel → Restart Kernel and Run All Cells** (ou `Maj + Entrée` cellule
   par cellule pour commenter chaque étape pendant la soutenance).

Les sept sections s'enchaînent : collecte, nettoyage, transformation,
intégration, contrôle de qualité, chargement, vérification. La dernière doit
afficher :

```
Notebook et script produisent le même datamart : True
```

## Étape 4 — Lancer la segmentation

1. Ouvrir **`clustering/segmentation_btk.ipynb`** — après l'étape 3, car il
   consomme le datamart écrit par l'ETL.
2. **Kernel → Restart Kernel and Run All Cells**.

Résultats attendus : *k* optimal = 3, K-Means retenu (silhouette 0,604) et trois
segments de 34, 8 et 6 entités. La dernière cellule doit afficher
`Résultats identiques.`

## Étape 5 (facultatif) — Brancher la base Oracle

Par défaut la chaîne tourne sur l'**extrait agrégé réel** des 49 entités du
réseau, livré avec le projet. Pour lire directement la base :

```bash
pip install oracledb
```

puis, dans une cellule placée **avant** la section « Collecte » :

```python
import os
os.environ["BTK_DB_USER"] = "votre_user"
os.environ["BTK_DB_PWD"]  = "votre_mot_de_passe"
os.environ["BTK_DB_DSN"]  = "localhost:1521/FREEPDB1"
```

La collecte bascule alors sur Oracle, et le datamart gagne trois éléments que
l'extrait agrégé ne porte pas : le **taux de présence** (table `POINTAGE`), le
**district** (table `AGENCE`) et l'**axe gestionnaire**
(`dim_gestionnaire`, `fait_objectif`).

*Sans connecteur Oracle :* exécuter `etl/export_sources.sql` avec SQLcl, placer
les cinq CSV produits dans `etl/source/`, et relancer — la collecte les détecte.

---

## En cas d'erreur

**`RuntimeError: Exécutez d'abord la cellule « 0. Préparation »`**
La cellule 0 n'a pas été exécutée : c'est elle qui importe `os`, `sys`, `pandas`
et `numpy` et qui repère le dossier du projet. Faire **Kernel → Restart Kernel
and Run All Cells**, ou cliquer dans la cellule 0 et faire `Maj + Entrée` avant
les suivantes.

**`NameError: name 'mode' / 'datamart' / 'pd' is not defined`**
Même cause : une cellule a été lancée sans que les précédentes aient tourné. Un
notebook se lit de haut en bas — chaque cellule réutilise les variables créées
par les précédentes.

**`FileNotFoundError: Racine du projet introuvable`**
Le notebook a été ouvert **hors du projet**. Il doit se trouver dans le dossier
du projet, à côté des dossiers `etl` et `clustering`, pour y trouver les
données : `etl/etl_btk.ipynb` et `clustering/segmentation_btk.ipynb`.

**`ModuleNotFoundError: No module named 'sklearn'`** (ou `pandas`, `matplotlib`)
Le noyau choisi n'est pas celui d'Anaconda. Menu **Kernel → Change Kernel** et
sélectionner `Python 3 (ipykernel)`. Si le paquet manque vraiment :
`conda install scikit-learn` dans l'invite Anaconda.

## Récupérer les résultats pour le rapport

**Capture d'une cellule** — clic droit sur la sortie → *Create New View for Cell
Output*, ou une capture d'écran classique (`Win + Maj + S` / `Cmd + Maj + 4`).

**Export du notebook entier**

```bash
jupyter nbconvert --to html  etl/etl_btk.ipynb
jupyter nbconvert --to pdf   clustering/segmentation_btk.ipynb
```

**Image de la sortie console** (ce qui a servi aux figures du rapport) :

```bash
python3 tools/render_console.py rapport-latex/images/etl/etl_execution.png \
    python3 etl/etl_agences.py
```

Le script exécute réellement la commande et met sa sortie en image : rien n'est
saisi à la main.

## Régénérer les notebooks

Les deux notebooks sont produits par `tools/build_notebooks.py`, ce qui les
garde alignés sur les scripts :

```bash
pip install nbformat
python3 tools/build_notebooks.py
```
