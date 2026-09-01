# -*- coding: utf-8 -*-
"""
Chaîne ETL (Extract - Transform - Load) du volet décisionnel BTK.

Objectif : consolider les données opérationnelles (agences, employés, clients,
objectifs, pointage) en un datamart en étoile agrégé PAR AGENCE, qui alimente à
la fois le tableau de bord, Power BI et la segmentation par clustering.

  EXTRACT    trois sources possibles, dans cet ordre de priorité :
             1. Oracle          -- tables AGENCE, B_UTILISATEURS, CLIENT_BTK,
                                   B_OBJECTIF, POINTAGE (connecteur oracledb) ;
             2. etl/source/*.csv-- export SQLcl de ces mêmes tables ;
             3. extrait agrégé  -- clustering/data/agences_reelles.csv, le
                                   relevé réel des 49 entités du réseau, livré
                                   avec le projet pour que la chaîne soit
                                   exécutable sans accès à la base.
  TRANSFORM  nettoyage, typage, agrégation par agence et calcul des indicateurs.
  QUALITÉ    contrôles avant chargement (manquants, négatifs, doublons).
  LOAD       datamart en étoile dans etl/entrepot/ + clustering/data/agences.csv.

Lancement :
    python3 etl_agences.py                 # source détectée automatiquement
    python3 etl_agences.py --source oracle # force la base Oracle
    python3 etl_agences.py --source csv    # force etl/source/*.csv
    python3 etl_agences.py --source extrait

Connexion Oracle : variables d'environnement BTK_DB_USER, BTK_DB_PWD, BTK_DB_DSN.
"""
import argparse
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "source")
ENTREPOT = os.path.join(HERE, "entrepot")
RACINE = os.path.normpath(os.path.join(HERE, ".."))
EXTRAIT_REEL = os.path.join(RACINE, "clustering", "data", "agences_reelles.csv")
DATAMART = os.path.join(RACINE, "clustering", "data", "agences.csv")

# Mesures du datamart. Le taux de présence n'est calculable que si la table
# POINTAGE est disponible : il est donc optionnel.
MESURES = ["effectif", "nb_gestionnaires", "nb_clients",
           "total_comptes", "production_credits", "collecte_epargne"]
PRESENCE = "taux_presence"

# Requêtes d'extraction, identiques à celles du notebook connecté à la base.
SQL = {
    "agences": "SELECT SK_AGENCE, LIBELLE_AGENCE, DISTRICT FROM AGENCE",
    "employes": "SELECT SK_UTILISATEUR, LIBELLE_UTILISATEUR, SK_AGENCE, "
                "EST_GESTIONNAIRE FROM B_UTILISATEURS",
    "clients": "SELECT SK_CLIENT, SK_AGENCE FROM CLIENT_BTK",
    "objectifs": "SELECT SK_AGENCE, SK_UTILISATEUR, "
                 "  NVL(SOUSCRIPTION_COMPTE_CHEQUES_OA,0)"
                 "  + NVL(SOUSCRIPTION_COMPTE_EPARGNES_OA,0)"
                 "  + NVL(SOUSCRIPTION_COMPTE_COURANTS_OA,0)      AS COMPTES, "
                 "  NVL(PRODUCTION_CREDITS_CONSO_OA,0)"
                 "  + NVL(PRODUCTION_CREDITS_IMMO_OA,0)"
                 "  + NVL(PRODUCTION_CREDITS_INVESTISSEMENT_OA,0) AS CREDITS, "
                 "  NVL(EPARGNE_ADD_OA,0)                         AS EPARGNE "
                 "FROM B_OBJECTIF",
    "pointages": "SELECT P.SK_UTILISATEUR, U.SK_AGENCE, P.STATUT "
                 "FROM POINTAGE P JOIN B_UTILISATEURS U "
                 "  ON P.SK_UTILISATEUR = U.SK_UTILISATEUR",
}
TABLES = ["agences", "employes", "clients", "objectifs", "pointages"]

# Causes les plus fréquentes d'un échec de connexion, et la manœuvre à faire.
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


def conseil(err):
    """Renvoie la manœuvre à faire pour l'erreur Oracle rencontrée."""
    for cle, texte in DIAGNOSTIC.items():
        if cle in str(err):
            return texte
    return "vérifiez que la base est démarrée et que le DSN est correct."


# ============================ 1. EXTRACT ===================================
def extract_oracle():
    """Lit les cinq tables sources directement dans la base Oracle BTK.

    POINTAGE est traitée à part : si elle n'a pas encore été créée
    (sql/setup_pointage.sql), la chaîne continue sans le taux de présence.
    """
    try:
        import oracledb
    except ImportError:
        sys.exit("[extract] le pilote « oracledb » n'est pas installé.\n"
                 "           pip install oracledb")
    user = os.environ.get("BTK_DB_USER", "SYSTEM")
    dsn = os.environ.get("BTK_DB_DSN", "localhost:1521/FREEPDB1")
    try:
        cn = oracledb.connect(user=user, password=os.environ.get("BTK_DB_PWD", ""),
                              dsn=dsn)
    except Exception as err:
        sys.exit(f"[extract] connexion à {user}@{dsn} impossible : "
                 f"{str(err).splitlines()[0]}\n           -> {conseil(err)}")
    print(f"[extract] connecté à {user}@{dsn} — Oracle {cn.version}")

    def q(sql):
        with cn.cursor() as cur:
            cur.execute(sql)
            return pd.DataFrame(cur.fetchall(),
                                columns=[d[0] for d in cur.description])

    tables = {}
    for nom in TABLES:
        try:
            tables[nom] = q(SQL[nom])
        except Exception as err:
            if nom != "pointages":
                cn.close()
                raise
            print(f"[extract] POINTAGE illisible ({str(err).splitlines()[0][:60]}) : "
                  "le taux de présence ne sera pas calculé.")
    cn.close()
    return tables


def extract_csv():
    """Lit l'export SQLcl des cinq tables sources (etl/source/*.csv)."""
    return {n: pd.read_csv(os.path.join(SOURCE, n + ".csv")) for n in TABLES}


def extract_extrait():
    """Lit le relevé réel déjà agrégé par agence (49 entités du réseau).

    Ce fichier est le résultat de l'extraction menée sur la base BTK ; il est
    versionné avec le projet afin que la chaîne reste exécutable et vérifiable
    sans accès à Oracle. Les clés SK_AGENCE suivent l'ordre de la table AGENCE.
    """
    ex = pd.read_csv(EXTRAIT_REEL)
    ex.insert(0, "SK_AGENCE", range(1, len(ex) + 1))
    return {"extrait": ex}


def sources_csv_disponibles():
    return all(os.path.exists(os.path.join(SOURCE, n + ".csv")) for n in TABLES)


def extract(source="auto"):
    """Choisit la source et renvoie (mode, tables)."""
    if source == "oracle" or (source == "auto" and os.environ.get("BTK_DB_USER")):
        print("[extract] source : base Oracle BTK")
        return "brut", extract_oracle()
    if source in ("csv", "auto") and sources_csv_disponibles():
        print(f"[extract] source : export CSV des tables ({SOURCE}/)")
        return "brut", extract_csv()
    if source == "csv":
        sys.exit(f"[extract] erreur : les cinq CSV sources sont absents de {SOURCE}/ "
                 f"({', '.join(n + '.csv' for n in TABLES)}). "
                 "Générez-les avec etl/export_sources.sql.")
    print(f"[extract] source : extrait agrégé réel ({os.path.relpath(EXTRAIT_REEL, RACINE)})")
    return "extrait", extract_extrait()


# ============================ 2. NETTOYAGE =================================
def nettoyer(tables):
    """Écarte les enregistrements inexploitables et type les colonnes."""
    retire = {}
    for nom in [n for n in ["employes", "clients", "objectifs", "pointages"]
                if n in tables]:
        df = tables[nom]
        avant = len(df)
        df = df.dropna(subset=["SK_AGENCE"])
        df["SK_AGENCE"] = df["SK_AGENCE"].astype(int)
        tables[nom] = df
        if avant - len(df):
            retire[nom] = avant - len(df)
    tables["employes"]["EST_GESTIONNAIRE"] = (
        tables["employes"]["EST_GESTIONNAIRE"].fillna(0).astype(int))
    for c in ["COMPTES", "CREDITS", "EPARGNE"]:
        tables["objectifs"][c] = pd.to_numeric(
            tables["objectifs"][c], errors="coerce").fillna(0)
    print("[nettoyage] lignes écartées (SK_AGENCE manquant) : "
          + (", ".join(f"{k}={v}" for k, v in retire.items()) if retire else "aucune"))
    return tables


# ============================ 3-4. TRANSFORM + INTÉGRATION =================
def agreger(tables):
    """Agrège les tables sources par agence puis les fusionne sur SK_AGENCE."""
    eff = tables["employes"].groupby("SK_AGENCE").agg(
        effectif=("SK_UTILISATEUR", "count"),
        nb_gestionnaires=("EST_GESTIONNAIRE", "sum")).reset_index()
    cli = tables["clients"].groupby("SK_AGENCE").size().reset_index(name="nb_clients")
    obj = tables["objectifs"].groupby("SK_AGENCE").agg(
        total_comptes=("COMPTES", "sum"),
        production_credits=("CREDITS", "sum"),
        collecte_epargne=("EPARGNE", "sum")).reset_index()

    dm = (tables["agences"].merge(eff, on="SK_AGENCE", how="left")
                           .merge(cli, on="SK_AGENCE", how="left")
                           .merge(obj, on="SK_AGENCE", how="left"))

    poi = tables.get("pointages")
    if poi is not None and len(poi):
        pres = poi.assign(present=poi["STATUT"].isin(["PRESENT", "RETARD"]).astype(int)) \
                  .groupby("SK_AGENCE").agg(taux_presence=("present", "mean")).reset_index()
        dm = dm.merge(pres, on="SK_AGENCE", how="left")
    return dm.rename(columns={"LIBELLE_AGENCE": "agence"})


def transformer(mode, tables):
    """Produit le datamart au grain de l'agence, quelle que soit la source."""
    if mode == "brut":
        dm = agreger(nettoyer(tables))
    else:
        dm = tables["extrait"].copy()          # déjà au grain de l'agence
    for c in ["effectif", "nb_gestionnaires", "nb_clients"]:
        dm[c] = pd.to_numeric(dm[c], errors="coerce").fillna(0).astype(int)
    for c in ["total_comptes", "production_credits", "collecte_epargne"]:
        dm[c] = pd.to_numeric(dm[c], errors="coerce").fillna(0).round(1)
    if PRESENCE in dm.columns:
        dm[PRESENCE] = pd.to_numeric(dm[PRESENCE], errors="coerce").fillna(0).round(3)
    return dm.sort_values("SK_AGENCE").reset_index(drop=True)


def transformer_gestionnaire(tables):
    """Axe « gestionnaire » : la production de B_OBJECTIF est rattachée à un
    gestionnaire par SK_UTILISATEUR ; on en tire dim_gestionnaire et
    fait_objectif, au grain (agence x gestionnaire)."""
    objectifs, employes = tables.get("objectifs"), tables.get("employes")
    if objectifs is None or "SK_UTILISATEUR" not in objectifs.columns:
        return None, None
    obj = objectifs.dropna(subset=["SK_UTILISATEUR"]).copy()
    if obj.empty:
        return None, None
    obj["SK_UTILISATEUR"] = obj["SK_UTILISATEUR"].astype(int)

    dim = employes[employes["EST_GESTIONNAIRE"] == 1]
    cols = [c for c in ["SK_UTILISATEUR", "LIBELLE_UTILISATEUR", "SK_AGENCE"]
            if c in dim.columns]
    dim = dim[cols].drop_duplicates(subset=["SK_UTILISATEUR"]).reset_index(drop=True)

    fait = obj.groupby(["SK_AGENCE", "SK_UTILISATEUR"]).agg(
        total_comptes=("COMPTES", "sum"),
        production_credits=("CREDITS", "sum"),
        collecte_epargne=("EPARGNE", "sum")).reset_index()
    for c in ["total_comptes", "production_credits", "collecte_epargne"]:
        fait[c] = fait[c].round(1)
    return dim, fait


# ============================ 5. CONTRÔLE DE QUALITÉ =======================
def controle_qualite(dm, mesures):
    """Vérifie le datamart avant chargement ; interrompt en cas d'anomalie."""
    manquants = int(dm[mesures].isna().sum().sum())
    negatifs = int((dm[mesures] < 0).sum().sum())
    doublons = int(dm["agence"].duplicated().sum())
    print(f"[qualité] {len(dm)} lignes x {len(mesures)} mesures | "
          f"valeurs manquantes : {manquants} | valeurs négatives : {negatifs} | "
          f"agences en double : {doublons}")
    if manquants or negatifs or doublons:
        sys.exit("[qualité] anomalie détectée : chargement interrompu.")
    print(dm[mesures].describe().loc[["mean", "min", "max"]].round(1).to_string())


# ============================ 6. LOAD ======================================
def load(dm, mesures, dim_gestionnaire=None, fait_objectif=None):
    """Écrit le datamart en étoile puis le fichier consommé par la segmentation."""
    os.makedirs(ENTREPOT, exist_ok=True)
    os.makedirs(os.path.dirname(DATAMART), exist_ok=True)

    cols_dim = ["SK_AGENCE", "agence"] + (["DISTRICT"] if "DISTRICT" in dm.columns else [])
    tables = ["dim_agence", "fait_agence"]
    dm[cols_dim].to_csv(os.path.join(ENTREPOT, "dim_agence.csv"), index=False)
    dm[["SK_AGENCE"] + mesures].to_csv(os.path.join(ENTREPOT, "fait_agence.csv"), index=False)
    if dim_gestionnaire is not None and fait_objectif is not None:
        dim_gestionnaire.to_csv(os.path.join(ENTREPOT, "dim_gestionnaire.csv"), index=False)
        fait_objectif.to_csv(os.path.join(ENTREPOT, "fait_objectif.csv"), index=False)
        tables += ["dim_gestionnaire", "fait_objectif"]
        print(f"[load] axe gestionnaire : {len(dim_gestionnaire)} gestionnaires, "
              f"{len(fait_objectif)} lignes de faits (agence x gestionnaire)")
    dm[["agence"] + mesures].to_csv(DATAMART, index=False)

    if "DISTRICT" not in dm.columns:
        print("[load] dim_agence sans DISTRICT : cet attribut n'est porté que par "
              "la table AGENCE (sources Oracle ou CSV).")
    print(f"[load] entrepôt -> etl/entrepot/ ({', '.join(tables)})")
    print(f"[load] datamart de segmentation -> {os.path.relpath(DATAMART, RACINE)}")


# ============================ MAIN =========================================
def main():
    ap = argparse.ArgumentParser(description="Chaîne ETL du datamart BTK.")
    ap.add_argument("--source", choices=["auto", "oracle", "csv", "extrait"],
                    default="auto", help="source des données (défaut : auto)")
    args = ap.parse_args()

    mode, tables = extract(args.source)
    if mode == "brut":
        print("[extract] " + " | ".join(f"{n} : {len(tables[n])}"
                                for n in TABLES if n in tables))
    else:
        print(f"[extract] {len(tables['extrait'])} entités du réseau")

    dm = transformer(mode, tables)
    mesures = MESURES + ([PRESENCE] if PRESENCE in dm.columns else [])
    print(f"[transform] datamart agrégé : {len(dm)} agences x {len(mesures)} mesures")

    controle_qualite(dm, mesures)
    load(dm, mesures, *transformer_gestionnaire(tables))

    print("\n[ok] chaîne ETL terminée — aperçu du datamart "
          "(10 premières agences par portefeuille) :")
    apercu = dm.sort_values("nb_clients", ascending=False).head(10)
    print(apercu[["agence"] + mesures].to_string(index=False))


if __name__ == "__main__":
    main()
