# Chaîne ETL du volet décisionnel (BTK)

Brique **ETL** (Extract – Transform – Load) du projet. Elle consolide les données
opérationnelles (employés, clients, objectifs, pointage) en un **datamart agrégé
par agence**, qui alimente à la fois le tableau de bord / Power BI et la
segmentation par clustering.

## Ce que fait le pipeline (`etl_agences.py`)
1. **Extract** — lit les sources `AGENCE`, `B_UTILISATEURS`, `CLIENT`,
   `B_OBJECTIF`, `POINTAGE` (depuis Oracle, ou des CSV dans `etl/source/`).
2. **Transform** — nettoie, type et **agrège par agence** pour calculer 7
   indicateurs : `effectif`, `nb_gestionnaires`, `nb_clients`, `total_comptes`,
   `production_credits`, `collecte_epargne`, `taux_presence`.
3. **Load** — écrit le datamart en **étoile** dans `etl/entrepot/`
   (`dim_agence.csv`, `fait_agence.csv`) et le fichier consommé par la
   segmentation (`../clustering/data/agences.csv`).

## Lancer
```bash
pip install pandas numpy
python3 etl_agences.py
```
En l'absence de source réelle, le script génère un **jeu représentatif** du réseau
BTK (45 agences) afin de démontrer la chaîne complète.

## Brancher vos données réelles
Deux options :

**a) Export CSV** — déposez dans `etl/source/` les fichiers `agences.csv`,
`employes.csv`, `clients.csv`, `objectifs.csv`, `pointages.csv` (colonnes
attendues : voir `extract()`). Le script les détecte automatiquement.

**b) Connexion Oracle** — installez `oracledb`, renseignez la connexion dans
`extract_oracle()` puis appelez `extract(source="oracle")`.

## Sorties
```
etl/entrepot/dim_agence.csv      # dimension agence (clé, libellé, district)
etl/entrepot/fait_agence.csv     # table de faits (7 indicateurs / agence)
clustering/data/agences.csv      # datamart consommé par la segmentation
```

Le détail de la conception et de la réalisation de cette chaîne figure dans le
chapitre « Sprint 5 : Chaîne ETL et volet décisionnel » du rapport.
