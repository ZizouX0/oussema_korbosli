# Chaîne ETL du volet décisionnel (BTK)

Brique **ETL** (Extract – Transform – Load) du projet. Elle consolide les données
opérationnelles (employés, clients, objectifs, pointage) en un **datamart agrégé
par agence**, qui alimente à la fois le tableau de bord / Power BI et la
segmentation par clustering.

## Ce que fait le pipeline (`etl_agences.py`)
1. **Extract** — lit les sources `AGENCE`, `B_UTILISATEURS`, `CLIENT_BTK`,
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

## Brancher VOS vraies données Oracle BTK

Par défaut le script tourne sur un jeu représentatif. Pour traiter les **vraies
données** de la base BTK, deux méthodes (au choix) — les deux produisent le même
datamart.

### Méthode A — Export CSV (la plus simple)
1. Ouvrez la base BTK avec **SQLcl** (fourni avec Oracle) et exécutez le script
   d'export fourni :
   ```bash
   sql VOTRE_USER/VOTRE_MDP@localhost:1521/FREEPDB1 @export_sources.sql
   ```
   Il génère 5 fichiers : `agences.csv`, `employes.csv`, `clients.csv`,
   `objectifs.csv`, `pointages.csv`.
   *(Avec SQL Developer : exécutez chaque requête de `export_sources.sql` puis
   clic-droit → Export → CSV.)*
2. Placez ces 5 fichiers dans **`etl/source/`**.
3. Lancez : `python3 etl_agences.py` — il détecte automatiquement les CSV réels.

### Méthode B — Connexion directe Oracle
1. `pip install oracledb`
2. Renseignez la connexion (variables d'environnement) :
   ```bash
   export BTK_DB_USER=votre_user
   export BTK_DB_PWD=votre_mdp
   export BTK_DB_DSN=localhost:1521/FREEPDB1
   ```
3. Dans `etl_agences.py`, appelez `extract(source="oracle")` (les requêtes SQL
   réelles sont déjà écrites dans `extract_oracle()`).

> Tables sources utilisées : `AGENCE`, `B_UTILISATEURS`, `CLIENT_BTK`,
> `B_OBJECTIF`, `POINTAGE` — les mêmes que celles de vos vues `V_BI_*`.

## Sorties
```
etl/entrepot/dim_agence.csv      # dimension agence (clé, libellé, district)
etl/entrepot/fait_agence.csv     # table de faits (7 indicateurs / agence)
clustering/data/agences.csv      # datamart consommé par la segmentation
```

Le détail de la conception et de la réalisation de cette chaîne figure dans le
chapitre « Sprint 5 : Chaîne ETL et volet décisionnel » du rapport.
