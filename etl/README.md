# Chaîne ETL du volet décisionnel (BTK)

Brique **ETL** (Extract – Transform – Load) du projet. Elle consolide les données
opérationnelles (agences, employés, clients, objectifs, pointage) en un
**datamart en étoile agrégé par agence**, qui alimente le tableau de bord,
Power BI et la segmentation par clustering.

## Lancer

```bash
pip install pandas
python3 etl_agences.py
```

La chaîne s'exécute **telle quelle sur les données réelles du réseau BTK**
(49 entités) : aucun jeu synthétique n'est utilisé.

```
python3 etl_agences.py --source auto      # détection automatique (défaut)
python3 etl_agences.py --source oracle    # base Oracle
python3 etl_agences.py --source csv       # export SQLcl dans etl/source/
python3 etl_agences.py --source extrait   # extrait agrégé livré avec le projet
```

## Les trois sources, par ordre de priorité

| Source | Contenu | Quand elle est utilisée |
|---|---|---|
| **Oracle** | tables `AGENCE`, `B_UTILISATEURS`, `CLIENT_BTK`, `B_OBJECTIF`, `POINTAGE` | si `BTK_DB_USER` est défini, ou `--source oracle` |
| **CSV** | export SQLcl des mêmes cinq tables, dans `etl/source/` | si les cinq fichiers sont présents, ou `--source csv` |
| **Extrait agrégé** | `clustering/data/agences_reelles.csv` — le relevé réel des 49 entités, versionné avec le projet | à défaut des deux précédentes |

L'extrait agrégé garantit que la chaîne reste **exécutable et vérifiable sans
accès à la base**. Les deux premières sources fournissent en plus le détail au
niveau employé, donc le **taux de présence** (table `POINTAGE`), le **district**
(table `AGENCE`) et l'**axe gestionnaire** (`dim_gestionnaire`, `fait_objectif`),
que l'extrait agrégé ne porte pas.

### Connexion Oracle

```bash
pip install oracledb
export BTK_DB_USER=votre_user
export BTK_DB_PWD=votre_mdp
export BTK_DB_DSN=localhost:1521/FREEPDB1
python3 etl_agences.py --source oracle
```

### Export CSV (sans connecteur Oracle)

```bash
sql VOTRE_USER/VOTRE_MDP@localhost:1521/FREEPDB1 @export_sources.sql
```
Le script produit `agences.csv`, `employes.csv`, `clients.csv`, `objectifs.csv`
et `pointages.csv` ; placez-les dans `etl/source/` puis relancez la chaîne.

## Les étapes

1. **Extract** — lecture des sources ci-dessus.
2. **Nettoyage** — les lignes sans `SK_AGENCE` sont écartées, les colonnes typées.
3. **Transformation / intégration** — agrégation par agence et fusion sur
   `SK_AGENCE` : `effectif`, `nb_gestionnaires`, `nb_clients`, `total_comptes`,
   `production_credits`, `collecte_epargne` (+ `taux_presence` si `POINTAGE`).
4. **Contrôle de qualité** — valeurs manquantes, valeurs négatives, agences en
   double ; le chargement est **interrompu** si un contrôle échoue.
5. **Load** — écriture du datamart en étoile.

## Sorties

```
etl/entrepot/dim_agence.csv          # dimension agence (SK_AGENCE, libellé [, district])
etl/entrepot/fait_agence.csv         # table de faits : mesures par agence
etl/entrepot/dim_gestionnaire.csv    # sources Oracle / CSV uniquement
etl/entrepot/fait_objectif.csv       # sources Oracle / CSV uniquement
clustering/data/agences.csv          # datamart consommé par la segmentation
```

`clustering/segmentation_reelle.py` consomme `clustering/data/agences.csv` dès
qu'il existe : la chaîne ETL et la segmentation sont donc directement enchaînées.

## Image d'exécution

`tools/render_console.py` exécute réellement la chaîne et met sa sortie en image :

```bash
python3 tools/render_console.py rapport-latex/images/etl/etl_execution.png \
    python3 etl/etl_agences.py
```

Le détail de la conception figure dans le chapitre « Volet décisionnel » du
rapport.
