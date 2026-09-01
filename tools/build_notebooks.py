# -*- coding: utf-8 -*-
"""Construit les deux notebooks du volet décisionnel (ETL et segmentation).

Les notebooks sont **autonomes** : ils n'importent aucun module du projet, tout
le traitement figure dans les cellules. Ils ont seulement besoin d'être placés
dans le dossier du projet, pour y trouver les données. Chacun se termine par une
cellule qui relance le script correspondant (`etl/etl_agences.py`,
`clustering/segmentation_reelle.py`) et vérifie que les résultats coïncident.

    python3 tools/build_notebooks.py        # génère les .ipynb
"""
import os

import nbformat as nbf

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Amorce : retrouve la racine du projet quel que soit le dossier depuis lequel
# Jupyter a été lancé. RACINE n'est définie qu'en cas de succès, de sorte que
# les cellules suivantes détectent proprement une préparation non exécutée.
AMORCE = '''\
import os, sys
import numpy as np
import pandas as pd

# On remonte depuis le dossier courant jusqu'à celui qui contient à la fois
# les répertoires "etl" et "clustering" : c'est la racine du projet.
_dossier = os.path.abspath(os.getcwd())
while not all(os.path.isdir(os.path.join(_dossier, d)) for d in ("etl", "clustering")):
    _parent = os.path.dirname(_dossier)
    if _parent == _dossier:
        raise FileNotFoundError(
            "Racine du projet introuvable depuis " + os.getcwd() + "\\n"
            "Placez ce notebook dans le dossier du projet, à côté des dossiers "
            "« etl » et « clustering », puis relancez cette cellule.")
    _dossier = _parent
RACINE = _dossier

pd.set_option("display.width", 170, "display.max_columns", 20)
print("Racine du projet :", RACINE)
print("pandas", pd.__version__, "| numpy", np.__version__)'''

# Garde placée en tête de la première cellule dépendante : transforme un
# « NameError » illisible en consigne claire.
GARDE = '''\
if "RACINE" not in globals():
    raise RuntimeError("Exécutez d'abord la cellule « 0. Préparation ». "
                       "Le plus simple : menu Kernel > Restart Kernel and Run All Cells.")

'''


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

> **Exécution : menu *Kernel → Restart Kernel and Run All Cells*.**
> Les cellules se lisent de haut en bas ; la première (« 0. Préparation »)
> définit les imports et le chemin du projet, elle doit donc passer en premier.

Ce notebook est autonome : il n'importe aucun module du projet. Il doit
seulement être placé **dans le dossier du projet**, à côté des dossiers `etl` et
`clustering`, pour y trouver les données.

La source est choisie automatiquement, dans cet ordre :
1. **Oracle** — si les variables `BTK_DB_USER`, `BTK_DB_PWD`, `BTK_DB_DSN` sont définies ;
2. **CSV** — si les cinq exports de `etl/export_sources.sql` sont dans `etl/source/` ;
3. **extrait agrégé réel** — le relevé des 49 entités du réseau livré avec le projet."""),

        md("## 0. Préparation"),
        code(AMORCE),

        md("""## 1. Connexion à la base Oracle

Prérequis, une seule fois, dans l'**invite Anaconda** : `pip install oracledb`.
Le pilote fonctionne en mode *thin* : aucun client Oracle à installer.

Les paramètres par défaut sont ceux de l'application
(`src/main/resources/META-INF/persistence.xml`). Le mot de passe n'est pas
écrit dans le notebook : il est demandé à la saisie.

Si la connexion échoue, la cellule affiche la cause probable et **le notebook
continue** sur l'extrait agrégé réel livré avec le projet."""),
        code(GARDE + r"""UTILISER_ORACLE = True   # False -> travailler sur l'extrait livré, sans invite

BTK_USER = os.environ.get("BTK_DB_USER", "SYSTEM")
BTK_DSN  = os.environ.get("BTK_DB_DSN",  "localhost:1521/FREEPDB1")
BTK_PWD  = os.environ.get("BTK_DB_PWD")

DIAGNOSTIC = {
    "ORA-01017": "identifiant ou mot de passe incorrect.",
    "ORA-12541": "aucun listener : le service Oracle n'est pas démarré "
                 "(Windows : services.msc, démarrer OracleServiceFREE et le TNSListener).",
    "DPY-6005":  "connexion refusée : vérifiez l'hôte et le port du DSN, et que "
                 "la base est bien démarrée.",
    "ORA-12514": "nom de service inconnu : essayez XEPDB1 ou ORCLPDB1 à la place "
                 "de FREEPDB1 (le nom dépend de la version d'Oracle installée).",
    "ORA-12154": "nom de service introuvable : donnez le DSN complet hote:port/service.",
    "ORA-28000": "compte verrouillé : ALTER USER ... ACCOUNT UNLOCK.",
}

CONNEXION = None
if not UTILISER_ORACLE:
    print("Oracle désactivé (UTILISER_ORACLE = False).")
else:
  try:
    import oracledb
  except ImportError:
    print("Le pilote « oracledb » n'est pas installé.")
    print("Dans l'invite Anaconda :  pip install oracledb")
  else:
    if not BTK_PWD:
        from getpass import getpass
        BTK_PWD = getpass(f"Mot de passe Oracle de {BTK_USER}@{BTK_DSN} : ")
    try:
        CONNEXION = oracledb.connect(user=BTK_USER, password=BTK_PWD, dsn=BTK_DSN)
        print(f"Connecté à {BTK_USER}@{BTK_DSN}")
        print("Serveur Oracle", CONNEXION.version)
    except Exception as err:
        print("Connexion impossible :", str(err).splitlines()[0])
        for cle, conseil in DIAGNOSTIC.items():
            if cle in str(err):
                print("  ->", conseil)
                break

if CONNEXION is None:
    print("\nLa suite du notebook utilisera l'extrait agrégé réel du réseau.")"""),

        md("""### Inventaire des tables sources

Contrôle de lecture table par table : une table illisible n'interrompt pas
l'inventaire, ce qui permet de voir d'un coup d'œil ce qui manque."""),
        code(r"""# Exécute une requête et renvoie un DataFrame (colonnes en majuscules).
def q(sql):
    with CONNEXION.cursor() as cur:
        cur.execute(sql)
        return pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])

if CONNEXION is None:
    print("Pas de connexion : inventaire ignoré.")
    inventaire = None
else:
    lignes = []
    for t in ["AGENCE", "B_UTILISATEURS", "CLIENT_BTK", "B_OBJECTIF", "POINTAGE"]:
        try:
            lignes.append([t, int(q(f"SELECT COUNT(*) AS N FROM {t}")["N"][0]), "OK"])
        except Exception as err:
            lignes.append([t, None, str(err).splitlines()[0][:45]])
    inventaire = pd.DataFrame(lignes, columns=["Table source", "Lignes", "État"])
inventaire"""),

        md("""## 2. Collecte (*Extract*)

Lecture des cinq tables sources. `POINTAGE` est traitée à part : si elle n'a pas
encore été créée (`sql/setup_pointage.sql`), la chaîne continue sans le taux de
présence.

Sans connexion Oracle, la collecte se rabat sur l'export CSV
(`etl/source/`) puis, à défaut, sur l'extrait agrégé réel."""),
        code('if "CONNEXION" not in globals():\n'
             '    raise RuntimeError("Exécutez d\'abord les cellules 0 et 1 "\n'
             '                       "(Préparation et Connexion).")\n\n'
             '''SOURCE  = os.path.join(RACINE, "etl", "source")
EXTRAIT = os.path.join(RACINE, "clustering", "data", "agences_reelles.csv")
TABLES  = ["agences", "employes", "clients", "objectifs", "pointages"]

SQL = {
    "agences":   "SELECT SK_AGENCE, LIBELLE_AGENCE, DISTRICT FROM AGENCE",
    "employes":  "SELECT SK_UTILISATEUR, LIBELLE_UTILISATEUR, SK_AGENCE, "
                 "EST_GESTIONNAIRE FROM B_UTILISATEURS",
    "clients":   "SELECT SK_CLIENT, SK_AGENCE FROM CLIENT_BTK",
    "objectifs": "SELECT SK_AGENCE, SK_UTILISATEUR, "
                 "  NVL(SOUSCRIPTION_COMPTE_CHEQUES_OA,0)"
                 "  + NVL(SOUSCRIPTION_COMPTE_EPARGNES_OA,0)"
                 "  + NVL(SOUSCRIPTION_COMPTE_COURANTS_OA,0)      AS COMPTES, "
                 "  NVL(PRODUCTION_CREDITS_CONSO_OA,0)"
                 "  + NVL(PRODUCTION_CREDITS_IMMO_OA,0)"
                 "  + NVL(PRODUCTION_CREDITS_INVESTISSEMENT_OA,0) AS CREDITS, "
                 "  NVL(EPARGNE_ADD_OA,0)                         AS EPARGNE "
                 "FROM B_OBJECTIF",
    "pointages": "SELECT P.SK_UTILISATEUR, U.SK_AGENCE, P.STATUT FROM POINTAGE P "
                 "JOIN B_UTILISATEURS U ON P.SK_UTILISATEUR = U.SK_UTILISATEUR",
}

if CONNEXION is not None:                               # 1) base Oracle
    tables, mode = {}, "brut"
    for n in TABLES:
        try:
            tables[n] = q(SQL[n])
        except Exception as err:
            if n != "pointages":
                raise
            print("POINTAGE illisible :", str(err).splitlines()[0][:60])
            print("  -> le taux de présence ne sera pas calculé.")
    print("source : base Oracle BTK")
elif all(os.path.exists(os.path.join(SOURCE, n + ".csv")) for n in TABLES):   # 2) CSV
    tables = {n: pd.read_csv(os.path.join(SOURCE, n + ".csv")) for n in TABLES}
    mode = "brut"
    print("source : export CSV des tables —", os.path.relpath(SOURCE, RACINE))
else:                                                   # 3) extrait agrégé réel
    extrait = pd.read_csv(EXTRAIT)
    extrait.insert(0, "SK_AGENCE", range(1, len(extrait) + 1))
    tables, mode = {"extrait": extrait}, "extrait"
    print("source : extrait agrégé réel —", os.path.relpath(EXTRAIT, RACINE))

if mode == "brut":
    print(" | ".join(f"{n} : {len(tables[n])}" for n in TABLES if n in tables))
    apercu = tables["agences"].head(10)
else:
    print(len(tables["extrait"]), "entités du réseau")
    apercu = tables["extrait"].head(10)
apercu'''),

        md("""## 2. Nettoyage

Les enregistrements sans agence de rattachement (`SK_AGENCE` manquant) sont
écartés, les colonnes typées et les mesures converties en numérique.

*Étape sans objet lorsque la source est l'extrait déjà agrégé : il ne contient
qu'une ligne par agence, sans clé manquante.*"""),
        code('''if mode == "brut":
    for n in [x for x in ["employes", "clients", "objectifs", "pointages"]
              if x in tables]:
        avant = len(tables[n])
        tables[n] = tables[n].dropna(subset=["SK_AGENCE"]).copy()
        tables[n]["SK_AGENCE"] = tables[n]["SK_AGENCE"].astype(int)
        print(f"{n:<10} {avant:>7} -> {len(tables[n]):>7} lignes")
    tables["employes"]["EST_GESTIONNAIRE"] = (
        tables["employes"]["EST_GESTIONNAIRE"].fillna(0).astype(int))
    for c in ["COMPTES", "CREDITS", "EPARGNE"]:
        tables["objectifs"][c] = pd.to_numeric(
            tables["objectifs"][c], errors="coerce").fillna(0)
else:
    print("Source déjà agrégée par agence : aucune ligne à écarter.")'''),

        md("""## 3 et 4. Transformation et intégration

Agrégation par agence, puis fusion des quatre jeux sur la clé `SK_AGENCE` :

| Mesure | Calcul |
|---|---|
| `effectif` | nombre d'employés de l'agence |
| `nb_gestionnaires` | employés avec `EST_GESTIONNAIRE = 1` |
| `nb_clients` | nombre de clients rattachés |
| `total_comptes` | somme des ouvertures de comptes |
| `production_credits` | somme de la production de crédits |
| `collecte_epargne` | somme de l'épargne additionnelle |
| `taux_presence` | part des pointages « présent » ou « retard » |"""),
        code('''MESURES = ["effectif", "nb_gestionnaires", "nb_clients",
           "total_comptes", "production_credits", "collecte_epargne"]

if mode == "brut":
    eff = tables["employes"].groupby("SK_AGENCE").agg(
        effectif=("SK_UTILISATEUR", "count"),
        nb_gestionnaires=("EST_GESTIONNAIRE", "sum")).reset_index()
    cli = tables["clients"].groupby("SK_AGENCE").size().reset_index(name="nb_clients")
    obj = tables["objectifs"].groupby("SK_AGENCE").agg(
        total_comptes=("COMPTES", "sum"),
        production_credits=("CREDITS", "sum"),
        collecte_epargne=("EPARGNE", "sum")).reset_index()
    datamart = (tables["agences"].merge(eff, on="SK_AGENCE", how="left")
                                 .merge(cli, on="SK_AGENCE", how="left")
                                 .merge(obj, on="SK_AGENCE", how="left")
                                 .rename(columns={"LIBELLE_AGENCE": "agence"}))
    if "pointages" in tables:                    # taux de présence si POINTAGE existe
        poi = tables["pointages"]
        pres = poi.assign(present=poi["STATUT"].isin(["PRESENT", "RETARD"]).astype(int)) \\
                  .groupby("SK_AGENCE").agg(taux_presence=("present", "mean")).reset_index()
        datamart = datamart.merge(pres, on="SK_AGENCE", how="left")
else:
    datamart = tables["extrait"].copy()          # déjà au grain de l'agence

for c in ["effectif", "nb_gestionnaires", "nb_clients"]:
    datamart[c] = pd.to_numeric(datamart[c], errors="coerce").fillna(0).astype(int)
for c in ["total_comptes", "production_credits", "collecte_epargne"]:
    datamart[c] = pd.to_numeric(datamart[c], errors="coerce").fillna(0).round(1)

mesures = list(MESURES)
if "taux_presence" in datamart.columns:
    datamart["taux_presence"] = pd.to_numeric(
        datamart["taux_presence"], errors="coerce").fillna(0).round(3)
    mesures.append("taux_presence")

datamart = datamart.sort_values("SK_AGENCE").reset_index(drop=True)
print(f"datamart : {len(datamart)} agences x {len(mesures)} mesures")
datamart.sort_values("nb_clients", ascending=False).head(10)[["agence"] + mesures]'''),

        md("""## 5. Contrôle de qualité

Avant chargement : aucune valeur manquante, aucune valeur négative, aucune
agence en double."""),
        code('''manquants = int(datamart[mesures].isna().sum().sum())
negatifs  = int((datamart[mesures] < 0).sum().sum())
doublons  = int(datamart["agence"].duplicated().sum())
print("valeurs manquantes :", manquants)
print("valeurs négatives  :", negatifs)
print("agences en double  :", doublons)
assert not (manquants or negatifs or doublons), "Anomalie : chargement interrompu."
datamart[mesures].describe().round(1)'''),

        md("""## 6. Chargement (*Load*)

Écriture du datamart en étoile dans `etl/entrepot/`, puis du fichier consommé
par la segmentation (`clustering/data/agences.csv`).

L'axe gestionnaire (`dim_gestionnaire`, `fait_objectif`) n'est produit que si la
source porte le détail par employé, c'est-à-dire Oracle ou l'export CSV."""),
        code('''ENTREPOT = os.path.join(RACINE, "etl", "entrepot")
DATAMART = os.path.join(RACINE, "clustering", "data", "agences.csv")
os.makedirs(ENTREPOT, exist_ok=True)

cols_dim = ["SK_AGENCE", "agence"] + (["DISTRICT"] if "DISTRICT" in datamart.columns else [])
datamart[cols_dim].to_csv(os.path.join(ENTREPOT, "dim_agence.csv"), index=False)
datamart[["SK_AGENCE"] + mesures].to_csv(os.path.join(ENTREPOT, "fait_agence.csv"), index=False)

if mode == "brut" and "SK_UTILISATEUR" in tables.get("objectifs", pd.DataFrame()).columns:
    obj = tables["objectifs"].dropna(subset=["SK_UTILISATEUR"]).copy()
    obj["SK_UTILISATEUR"] = obj["SK_UTILISATEUR"].astype(int)
    colonnes = [c for c in ["SK_UTILISATEUR", "LIBELLE_UTILISATEUR", "SK_AGENCE"]
                if c in tables["employes"].columns]
    dim_g = (tables["employes"][tables["employes"]["EST_GESTIONNAIRE"] == 1][colonnes]
             .drop_duplicates(subset=["SK_UTILISATEUR"]))
    fait_o = obj.groupby(["SK_AGENCE", "SK_UTILISATEUR"]).agg(
        total_comptes=("COMPTES", "sum"),
        production_credits=("CREDITS", "sum"),
        collecte_epargne=("EPARGNE", "sum")).round(1).reset_index()
    dim_g.to_csv(os.path.join(ENTREPOT, "dim_gestionnaire.csv"), index=False)
    fait_o.to_csv(os.path.join(ENTREPOT, "fait_objectif.csv"), index=False)
    print(f"axe gestionnaire : {len(dim_g)} gestionnaires, {len(fait_o)} lignes de faits")
else:
    print("axe gestionnaire non produit : la source n'a pas le détail par employé.")

datamart[["agence"] + mesures].to_csv(DATAMART, index=False)
print("entrepôt ->", ", ".join(sorted(os.listdir(ENTREPOT))))
print("datamart de segmentation ->", os.path.relpath(DATAMART, RACINE))
pd.read_csv(os.path.join(ENTREPOT, "fait_agence.csv")).head()'''),

        md("""## 7. Vérification

Le notebook doit retrouver **exactement** le résultat du script
`etl/etl_agences.py`. La cellule relance le script et compare les deux
datamarts ; elle échoue si un écart apparaît."""),
        code('''import subprocess

script = os.path.join(RACINE, "etl", "etl_agences.py")
if not os.path.exists(script):
    print("Script etl/etl_agences.py absent : vérification ignorée.")
else:
    r = subprocess.run([sys.executable, script], cwd=RACINE,
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-800:])
        raise RuntimeError("Le script s'est terminé en erreur.")
    identique = pd.read_csv(DATAMART).equals(
        datamart[["agence"] + mesures].reset_index(drop=True))
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

> **Exécution : menu *Kernel → Restart Kernel and Run All Cells*.**
> La première cellule (« 0. Préparation ») définit les imports et le chemin du
> projet : elle doit passer en premier.

**Prérequis :** exécuter d'abord `etl/etl_btk.ipynb` (ou
`python3 etl/etl_agences.py`), qui écrit `clustering/data/agences.csv`.
À défaut, ce notebook repart de l'extrait réel livré avec le projet."""),

        md("## 0. Préparation"),
        code(AMORCE + '''

import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (silhouette_score, davies_bouldin_score,
                             calinski_harabasz_score)
import sklearn

print("scikit-learn", sklearn.__version__, "| matplotlib", plt.matplotlib.__version__)

NAVY, CYAN, ORANGE, GREEN = "#14507A", "#1B9CD8", "#E8A33D", "#2E9E6B"
FEATURES = ["effectif", "nb_gestionnaires", "nb_clients",
            "total_comptes", "production_credits", "collecte_epargne"]'''),

        md("## 1. Chargement du datamart"),
        code(GARDE + '''DATA = os.path.join(RACINE, "clustering", "data")
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
ax.set_ylabel("Score de silhouette (plus haut = meilleur)")
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

script = os.path.join(RACINE, "clustering", "segmentation_reelle.py")
if not os.path.exists(script):
    print("Script clustering/segmentation_reelle.py absent : vérification ignorée.")
else:
    r = subprocess.run([sys.executable, script], cwd=RACINE,
                       capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-800:])
        raise RuntimeError("Le script s'est terminé en erreur.")
    ref = pd.read_csv(os.path.join(RACINE, "clustering",
                                   "comparaison_modeles_reelles.csv"))
    ecart = float(np.abs(ref["Silhouette"].values - comp["Silhouette"].values).max())
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
