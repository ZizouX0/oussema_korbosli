# -*- coding: utf-8 -*-
"""Construit les deux notebooks du volet décisionnel (ETL et segmentation).

Les notebooks sont générés à partir de ce fichier afin de rester alignés sur les
scripts `etl/etl_agences.py` et `clustering/segmentation_reelle.py` : chaque
notebook rejoue les mêmes étapes et vérifie, en dernière cellule, qu'il retrouve
exactement le résultat du script.

    python3 tools/build_notebooks.py        # génère les .ipynb
"""
import os

import nbformat as nbf

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Amorce commune : retrouve la racine du projet quel que soit le dossier depuis
# lequel Jupyter a été lancé (Anaconda ouvre souvent le notebook ailleurs).
AMORCE = '''\
import os, sys
import numpy as np
import pandas as pd

# Racine du projet : on remonte depuis le dossier courant jusqu'au dossier qui
# contient à la fois "etl" et "clustering".
RACINE = os.path.abspath(os.getcwd())
while not all(os.path.isdir(os.path.join(RACINE, d)) for d in ("etl", "clustering")):
    parent = os.path.dirname(RACINE)
    if parent == RACINE:
        raise SystemExit("Racine du projet introuvable : ouvrez le notebook "
                         "depuis le dossier du projet.")
    RACINE = parent
sys.path.insert(0, os.path.join(RACINE, "etl"))
pd.set_option("display.width", 160, "display.max_columns", 20)
print("Racine du projet :", RACINE)
print("pandas", pd.__version__, "| numpy", np.__version__)'''


def md(texte):
    return nbf.v4.new_markdown_cell(texte)


def code(source):
    return nbf.v4.new_code_cell(source)


# ======================== NOTEBOOK 1 : CHAÎNE ETL ==========================
def notebook_etl():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md("""# Chaîne ETL du datamart BTK

Consolidation des données opérationnelles en un **datamart en étoile agrégé par
agence**, qui alimente le tableau de bord, Power BI et la segmentation.

**Exécution :** menu *Kernel → Restart & Run All*, ou `Maj + Entrée` cellule par cellule.

La source est choisie automatiquement, dans cet ordre :
1. **Oracle** — si les variables `BTK_DB_USER`, `BTK_DB_PWD`, `BTK_DB_DSN` sont définies ;
2. **CSV** — si les cinq exports de `etl/export_sources.sql` sont dans `etl/source/` ;
3. **extrait agrégé réel** — le relevé des 49 entités du réseau livré avec le projet."""),

        md("## 0. Préparation"),
        code(AMORCE),

        md("""## 1. Collecte (*Extract*)

Lecture des cinq tables sources `AGENCE`, `B_UTILISATEURS`, `CLIENT_BTK`,
`B_OBJECTIF` et `POINTAGE`. La sélection de la source est déléguée au module
`etl_agences`, pour que notebook et script lisent exactement la même chose.

> **Pour lire directement votre base Oracle**, exécuter d'abord `pip install oracledb`
> puis, dans une cellule placée **avant** celle-ci :
> ```python
> import os
> os.environ["BTK_DB_USER"] = "votre_user"
> os.environ["BTK_DB_PWD"]  = "votre_mot_de_passe"
> os.environ["BTK_DB_DSN"]  = "localhost:1521/FREEPDB1"
> ```
> La cellule suivante basculera d'elle-même sur Oracle, et le datamart gagnera
> le taux de présence, le district et l'axe gestionnaire."""),
        code('''import etl_agences as etl

mode, tables = etl.extract("auto")
if mode == "brut":
    print(" | ".join(f"{n} : {len(tables[n])}" for n in etl.TABLES))
    affichage = tables["agences"].head(10)
else:
    print(f"{len(tables['extrait'])} entités du réseau")
    affichage = tables["extrait"].head(10)
affichage'''),

        md("""## 2. Nettoyage

Les enregistrements sans agence de rattachement (`SK_AGENCE` manquant) sont
écartés, les colonnes sont typées et les mesures converties en numérique.

*(Étape sans objet lorsque la source est l'extrait déjà agrégé : il ne contient
qu'une ligne par agence, sans clé manquante.)*"""),
        code('''if mode == "brut":
    tables = etl.nettoyer(tables)
    print("employés retenus :", len(tables["employes"]),
          "| clients :", len(tables["clients"]),
          "| lignes d'objectifs :", len(tables["objectifs"]))
else:
    print("Source déjà agrégée par agence : aucune ligne à écarter.")'''),

        md("""## 3 et 4. Transformation et intégration

Agrégation par agence puis fusion sur la clé `SK_AGENCE` :

| Mesure | Calcul |
|---|---|
| `effectif` | nombre d'employés de l'agence |
| `nb_gestionnaires` | employés avec `EST_GESTIONNAIRE = 1` |
| `nb_clients` | nombre de clients rattachés |
| `total_comptes` | somme des ouvertures de comptes |
| `production_credits` | somme de la production de crédits |
| `collecte_epargne` | somme de l'épargne additionnelle |
| `taux_presence` | part des pointages « présent » ou « retard » |"""),
        code('''datamart = etl.transformer(mode, tables)
mesures = etl.MESURES + ([etl.PRESENCE] if etl.PRESENCE in datamart.columns else [])
print(f"datamart : {len(datamart)} agences x {len(mesures)} mesures")
datamart.sort_values("nb_clients", ascending=False).head(10)[["agence"] + mesures]'''),

        md("""## 5. Contrôle de qualité

Avant chargement : aucune valeur manquante, aucune valeur négative, aucune
agence en double. Le chargement est interrompu si un contrôle échoue."""),
        code('''print("valeurs manquantes :", int(datamart[mesures].isna().sum().sum()))
print("valeurs négatives  :", int((datamart[mesures] < 0).sum().sum()))
print("agences en double  :", int(datamart["agence"].duplicated().sum()))
datamart[mesures].describe().round(1)'''),

        md("""## 6. Chargement (*Load*)

Écriture du datamart en étoile dans `etl/entrepot/`, puis du fichier consommé
par la segmentation (`clustering/data/agences.csv`)."""),
        code('''etl.load(datamart, mesures, *etl.transformer_gestionnaire(tables))
sorties = sorted(os.listdir(os.path.join(RACINE, "etl", "entrepot")))
print("\\nFichiers de l'entrepôt :", ", ".join(sorties))
pd.read_csv(os.path.join(RACINE, "etl", "entrepot", "fait_agence.csv")).head()'''),

        md("""## 7. Vérification

Le notebook doit retrouver **exactement** le résultat du script
`etl/etl_agences.py`. La cellule ci-dessous relance le script et compare."""),
        code('''import subprocess
subprocess.run([sys.executable, os.path.join(RACINE, "etl", "etl_agences.py")],
               cwd=RACINE, capture_output=True, text=True, check=True)
script = pd.read_csv(os.path.join(RACINE, "clustering", "data", "agences.csv"))
identique = script.equals(datamart[["agence"] + mesures].reset_index(drop=True))
print("Notebook et script produisent le même datamart :", identique)
assert identique, "Écart entre le notebook et le script."'''),
    ]
    return nb


# ==================== NOTEBOOK 2 : SEGMENTATION ============================
def notebook_clustering():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        md("""# Segmentation des agences BTK (apprentissage non supervisé)

Segmentation du réseau à partir du datamart produit par la chaîne ETL.

**Prérequis :** exécuter d'abord le notebook `etl/etl_btk.ipynb` (ou
`python3 etl/etl_agences.py`), qui écrit `clustering/data/agences.csv`.

**Exécution :** *Kernel → Restart & Run All*."""),

        md("## 0. Préparation"),
        code(AMORCE + '''

import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             calinski_harabasz_score)

NAVY, CYAN, ORANGE, GREEN = "#14507A", "#1B9CD8", "#E8A33D", "#2E9E6B"
FEATURES = ["effectif", "nb_gestionnaires", "nb_clients",
            "total_comptes", "production_credits", "collecte_epargne"]'''),

        md("""## 1. Chargement du datamart

Le datamart produit par l'ETL est utilisé en priorité ; à défaut, on repart de
l'extrait réel livré avec le projet."""),
        code('''DATA = os.path.join(RACINE, "clustering", "data")
src = os.path.join(DATA, "agences.csv")
if not os.path.exists(src):
    src = os.path.join(DATA, "agences_reelles.csv")
brut = pd.read_csv(src)
print("datamart :", os.path.relpath(src, RACINE), "|", len(brut), "entités")
brut.head()'''),

        md("""## 2. Préparation des variables

Le **siège** (540 employés) est une structure centrale, pas une agence : il est
conservé dans le datamart mais écarté de la segmentation, où il constitue un
point atypique qui écraserait toute autre structure.

Le portefeuille et les montants sont très asymétriques : ils passent au
**logarithme** avant standardisation, afin qu'une agence extrême ne domine pas
les distances."""),
        code('''df = brut[brut["agence"] != "SIEGE"].reset_index(drop=True)
T = df[FEATURES].copy()
for c in ["nb_clients", "total_comptes", "production_credits", "collecte_epargne"]:
    T[c] = np.log1p(T[c])
X = StandardScaler().fit_transform(T)
print(f"{len(brut)} entités, {len(df)} retenues (siège écarté) x {len(FEATURES)} indicateurs")
print("matrice standardisée :", X.shape)'''),

        md("""## 3. Choix du nombre de clusters

Méthode du coude (inertie intra-cluster) et score de silhouette.
`k = 2` isolerait trivialement les entités sans activité : on retient la
meilleure solution à partir de `k = 3`, exploitable pour le pilotage."""),
        code('''ks = range(2, 9)
inerties, sils = [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inerties.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))
k_opt = list(ks)[int(np.argmax([s if k >= 3 else -1 for k, s in zip(ks, sils)]))]

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(list(ks), inerties, "o-", color=NAVY, lw=2)
ax[0].set_title("Méthode du coude (inertie)"); ax[0].set_xlabel("k")
ax[0].set_ylabel("Inertie intra-cluster"); ax[0].grid(alpha=.3)
ax[1].plot(list(ks), sils, "o-", color=CYAN, lw=2)
ax[1].axvline(k_opt, ls="--", color=ORANGE)
ax[1].set_title("Score de silhouette"); ax[1].set_xlabel("k")
ax[1].set_ylabel("Silhouette"); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.show()
print("silhouettes :", [round(s, 3) for s in sils], "-> k optimal =", k_opt)'''),

        md("""## 4. Comparaison des modèles

Quatre modèles sont comparés. **Protocole d'évaluation équitable :** chaque
modèle est noté sur *la totalité* des agences ; les points qu'un modèle refuse
de classer (bruit DBSCAN) sont comptés comme un groupe à part entière, pour
qu'aucun modèle ne soit avantagé par le fait d'avoir écarté les agences les plus
difficiles à classer."""),
        code('''modeles = {
    "K-Means": KMeans(n_clusters=k_opt, n_init=10, random_state=42).fit_predict(X),
    "Agglomératif": AgglomerativeClustering(n_clusters=k_opt).fit_predict(X),
    "GMM": GaussianMixture(n_components=k_opt, random_state=42).fit_predict(X),
    "DBSCAN": DBSCAN(eps=1.5, min_samples=3).fit_predict(X),
}
lignes = []
for nom, lab in modeles.items():
    lab = lab.copy()
    if (lab == -1).any():
        lab[lab == -1] = lab.max() + 1
    lignes.append([nom, len(set(lab)), silhouette_score(X, lab),
                   davies_bouldin_score(X, lab), calinski_harabasz_score(X, lab)])
comp = pd.DataFrame(lignes, columns=["Modèle", "Clusters", "Silhouette",
                                     "Davies-Bouldin", "Calinski-Harabasz"])

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(comp["Modèle"], comp["Silhouette"], color=[NAVY, CYAN, ORANGE, GREEN])
for i, v in enumerate(comp["Silhouette"]):
    ax.text(i, v + .01, f"{v:.3f}", ha="center", fontsize=10, weight="bold")
ax.set_ylabel("Score de silhouette (↑ meilleur)")
ax.set_title("Comparaison des modèles de clustering")
ax.set_ylim(0, comp["Silhouette"].max() * 1.25); ax.grid(axis="y", alpha=.3)
plt.tight_layout(); plt.show()
comp.round(3)'''),

        md("""## 5. Modèle retenu et projection

Le modèle retenu est celui qui obtient le meilleur score de silhouette sous le
protocole ci-dessus. La projection **ACP** ramène les six indicateurs à deux
composantes pour visualiser les groupes."""),
        code('''best = comp.loc[comp["Silhouette"].idxmax(), "Modèle"]
labels = modeles[best]
print("modèle retenu :", best)

p = PCA(n_components=2).fit(X); Z = p.transform(X)
fig, ax = plt.subplots(figsize=(7.5, 5.2))
cols = [NAVY, ORANGE, GREEN, CYAN, "#B0489B"]
for c in sorted(set(labels)):
    m = labels == c
    ax.scatter(Z[m, 0], Z[m, 1], s=55, alpha=.85, color=cols[c % len(cols)],
               label=f"Cluster {c}", edgecolor="white")
ax.set_xlabel(f"Composante 1 ({p.explained_variance_ratio_[0]*100:.0f} %)")
ax.set_ylabel(f"Composante 2 ({p.explained_variance_ratio_[1]*100:.0f} %)")
ax.set_title(f"Segmentation des agences — {best} (projection ACP)")
ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.show()'''),

        md("## 6. Profils des segments"),
        code('''d = df.copy(); d["cluster"] = labels
prof = d.groupby("cluster")[FEATURES].mean().round(0).astype(int)
prof["nb_agences"] = d.groupby("cluster").size()
prof = prof[["nb_agences"] + FEATURES]
for c in sorted(set(labels)):
    noms = d.loc[d.cluster == c, "agence"].tolist()
    print(f"Cluster {c} ({len(noms)}) : {', '.join(noms[:8])}{' …' if len(noms) > 8 else ''}")
prof'''),

        md("""## 7. Vérification

Le notebook doit retrouver **exactement** le résultat du script
`clustering/segmentation_reelle.py`."""),
        code('''import subprocess
subprocess.run([sys.executable,
                os.path.join(RACINE, "clustering", "segmentation_reelle.py")],
               cwd=RACINE, capture_output=True, text=True, check=True)
ref = pd.read_csv(os.path.join(RACINE, "clustering", "comparaison_modeles_reelles.csv"))
ecart = float((ref["Silhouette"].values - comp["Silhouette"].values).__abs__().max())
print("écart maximal sur la silhouette entre notebook et script :", round(ecart, 12))
assert ecart < 1e-9, "Écart entre le notebook et le script."
print("Résultats identiques.")'''),
    ]
    return nb


if __name__ == "__main__":
    cibles = [(notebook_etl(), os.path.join(RACINE, "etl", "etl_btk.ipynb")),
              (notebook_clustering(),
               os.path.join(RACINE, "clustering", "segmentation_btk.ipynb"))]
    for nb, chemin in cibles:
        nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python",
                                     "name": "python3"}
        nb.metadata["language_info"] = {"name": "python"}
        nbf.write(nb, chemin)
        print(f"[notebook] {os.path.relpath(chemin, RACINE)} "
              f"({len(nb.cells)} cellules)")
