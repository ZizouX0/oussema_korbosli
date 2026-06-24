# -*- coding: utf-8 -*-
"""
Chaîne ETL (Extract - Transform - Load) du volet décisionnel BTK.

Objectif : consolider les données opérationnelles (employés, clients, objectifs,
pointage) en un datamart agrégé PAR AGENCE, qui alimente à la fois le tableau de
bord / Power BI et la segmentation par clustering.

  EXTRACT   sources Oracle (B_UTILISATEURS, CLIENT, B_OBJECTIF, POINTAGE, AGENCE)
            -> lues depuis etl/source/*.csv si présents, sinon jeu synthétique.
  TRANSFORM nettoyage, typage, agrégation par agence, calcul des indicateurs
            (effectif, portefeuille, production, taux de présence).
  LOAD      datamart en étoile (etl/entrepot/) + clustering/data/agences.csv.

Pour brancher Oracle réel : installer `oracledb`, renseigner la connexion dans
extract_oracle() et appeler extract(source="oracle").
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "source")
ENTREPOT = os.path.join(HERE, "entrepot")
DATAMART = os.path.normpath(os.path.join(HERE, "..", "clustering", "data", "agences.csv"))
os.makedirs(ENTREPOT, exist_ok=True)
os.makedirs(os.path.dirname(DATAMART), exist_ok=True)

FEATURES = ["effectif", "nb_gestionnaires", "nb_clients", "total_comptes",
            "production_credits", "collecte_epargne", "taux_presence"]


# ============================ EXTRACT ======================================
def extract_oracle():
    """Extraction depuis Oracle (à activer avec vos identifiants).

    import oracledb
    cn = oracledb.connect(user="...", password="...", dsn="host:1521/FREEPDB1")
    emp = pd.read_sql("SELECT SK_UTILISATEUR, SK_AGENCE, EST_GESTIONNAIRE "
                      "FROM B_UTILISATEURS", cn)
    cli = pd.read_sql("SELECT SK_CLIENT, SK_AGENCE FROM CLIENT", cn)
    obj = pd.read_sql("SELECT SK_AGENCE, SOUSCRIPTION_COMPTE_CHEQUES_OA, ... "
                      "FROM B_OBJECTIF", cn)
    poi = pd.read_sql("SELECT P.SK_UTILISATEUR, U.SK_AGENCE, P.STATUT "
                      "FROM POINTAGE P JOIN B_UTILISATEURS U "
                      "ON P.SK_UTILISATEUR=U.SK_UTILISATEUR", cn)
    return emp, cli, obj, poi
    """
    raise NotImplementedError("Configurer la connexion Oracle dans extract_oracle().")


def _synthese_source():
    """Génère des données SOURCES brutes réalistes (3 profils d'agences)."""
    rng = np.random.default_rng(7)
    tiers = [("grande", 7, 116, 10), ("moyenne", 16, 55, 7), ("petite", 22, 22, 4)]
    agences, employes, clients, objectifs, pointages = [], [], [], [], []
    sk_ag = sk_emp = sk_cli = 1
    for nom, n, mu, sd in tiers:
        for _ in range(n):
            eff = int(max(5, rng.normal(mu, sd)))
            agences.append({"SK_AGENCE": sk_ag, "LIBELLE_AGENCE": f"Agence {sk_ag:02d}",
                            "DISTRICT": rng.choice(["Nord", "Centre", "Sud"])})
            p_pres = {"grande": 0.93, "moyenne": 0.89, "petite": 0.82}[nom]
            for _ in range(eff):                       # employés de l'agence
                gest = 1 if rng.random() < 0.30 else 0
                employes.append({"SK_UTILISATEUR": sk_emp, "SK_AGENCE": sk_ag,
                                 "EST_GESTIONNAIRE": gest})
                for _ in range(20):                    # ~20 jours de pointage / employé
                    r = rng.random()
                    statut = "PRESENT" if r < p_pres else ("RETARD" if r < p_pres + 0.05 else "ABSENT")
                    pointages.append({"SK_UTILISATEUR": sk_emp, "SK_AGENCE": sk_ag, "STATUT": statut})
                sk_emp += 1
            for _ in range(int(eff * rng.normal(8, 0.9))):   # clients de l'agence
                clients.append({"SK_CLIENT": sk_cli, "SK_AGENCE": sk_ag}); sk_cli += 1
            for _ in range(6):                          # 6 périodes d'objectifs / agence
                objectifs.append({
                    "SK_AGENCE": sk_ag,
                    "COMPTES": max(0, rng.normal(eff * 20 / 6, eff * 0.4)),
                    "CREDITS": max(0, rng.normal(eff * 15 / 6, eff * 0.3)),
                    "EPARGNE": max(0, rng.normal(eff * 10 / 6, eff * 0.25)),
                })
            sk_ag += 1
    return (pd.DataFrame(agences), pd.DataFrame(employes), pd.DataFrame(clients),
            pd.DataFrame(objectifs), pd.DataFrame(pointages))


def extract(source="auto"):
    """Lit les CSV sources s'ils existent, sinon génère un jeu synthétique."""
    fichiers = {n: os.path.join(SOURCE, n + ".csv")
                for n in ["agences", "employes", "clients", "objectifs", "pointages"]}
    if source == "oracle":
        ag = None; emp, cli, obj, poi = extract_oracle()
        return ag, emp, cli, obj, poi
    if all(os.path.exists(f) for f in fichiers.values()):
        print("[extract] Sources CSV réelles détectées dans etl/source/")
        return tuple(pd.read_csv(fichiers[n]) for n in
                     ["agences", "employes", "clients", "objectifs", "pointages"])
    print("[extract] Aucune source réelle — génération d'un jeu synthétique.")
    return _synthese_source()


# ============================ TRANSFORM ====================================
def transform(agences, employes, clients, objectifs, pointages):
    """Nettoie et agrège les sources par agence (calcul des indicateurs)."""
    # nettoyage minimal
    for df in (employes, clients, objectifs, pointages):
        df.dropna(subset=["SK_AGENCE"], inplace=True)

    eff = employes.groupby("SK_AGENCE").agg(
        effectif=("SK_UTILISATEUR", "count"),
        nb_gestionnaires=("EST_GESTIONNAIRE", "sum")).reset_index()
    cli = clients.groupby("SK_AGENCE").size().reset_index(name="nb_clients")
    obj = objectifs.groupby("SK_AGENCE").agg(
        total_comptes=("COMPTES", "sum"),
        production_credits=("CREDITS", "sum"),
        collecte_epargne=("EPARGNE", "sum")).reset_index()
    poi = pointages.assign(present=pointages["STATUT"].isin(["PRESENT", "RETARD"]).astype(int)) \
        .groupby("SK_AGENCE").agg(taux_presence=("present", "mean")).reset_index()

    dm = agences.merge(eff, on="SK_AGENCE", how="left") \
                .merge(cli, on="SK_AGENCE", how="left") \
                .merge(obj, on="SK_AGENCE", how="left") \
                .merge(poi, on="SK_AGENCE", how="left")
    dm = dm.rename(columns={"LIBELLE_AGENCE": "agence"})
    # arrondis et valeurs manquantes
    for c in ["nb_gestionnaires", "nb_clients"]:
        dm[c] = dm[c].fillna(0).astype(int)
    for c in ["total_comptes", "production_credits", "collecte_epargne"]:
        dm[c] = dm[c].fillna(0).round(1)
    dm["taux_presence"] = dm["taux_presence"].fillna(0).round(3)
    return dm


# ============================ LOAD =========================================
def load(dm):
    """Charge le datamart en étoile (entrepôt) et le fichier pour le clustering."""
    dim_agence = dm[["SK_AGENCE", "agence", "DISTRICT"]]
    fait_agence = dm[["SK_AGENCE"] + FEATURES]
    dim_agence.to_csv(os.path.join(ENTREPOT, "dim_agence.csv"), index=False)
    fait_agence.to_csv(os.path.join(ENTREPOT, "fait_agence.csv"), index=False)
    # fichier consommé par la segmentation (clustering)
    dm[["agence"] + FEATURES].to_csv(DATAMART, index=False)
    print(f"[load] Entrepôt -> {ENTREPOT}/ (dim_agence, fait_agence)")
    print(f"[load] Datamart clustering -> {DATAMART}")


# ============================ MAIN =========================================
def main():
    agences, employes, clients, objectifs, pointages = extract()
    print(f"[extract] {len(agences)} agences, {len(employes)} employés, "
          f"{len(clients)} clients, {len(objectifs)} lignes objectifs, "
          f"{len(pointages)} pointages.")
    dm = transform(agences, employes, clients, objectifs, pointages)
    print(f"[transform] datamart agrégé : {len(dm)} agences x {len(FEATURES)} indicateurs.")
    load(dm)
    print("\n[ok] Chaîne ETL terminée. Aperçu du datamart :")
    print(dm[["agence"] + FEATURES].head(6).to_string(index=False))


if __name__ == "__main__":
    main()
