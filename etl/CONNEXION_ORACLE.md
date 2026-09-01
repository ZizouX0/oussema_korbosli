# Brancher la chaîne ETL sur la base Oracle — étape par étape

Marche à suivre pour faire tourner l'ETL sur **votre base Oracle**, et non sur
l'extrait agrégé livré avec le projet.

Les paramètres de connexion de l'application ne sont pas dans `persistence.xml` :
l'unité de persistance est en JTA, donc c'est la **datasource WildFly**
`java:/OracleDS` qui les porte (voir `tools/DEPANNAGE_ORACLE_WILDFLY.md`).

| | Valeur |
|---|---|
| Utilisateur | `BTK_BI` |
| DSN | `localhost:1521/FREEPDB1` |
| Mot de passe | celui que vous avez défini pour ce compte |

Ces valeurs sont les **défauts** des outils ; pour en utiliser d'autres, définir
`BTK_DB_USER`, `BTK_DB_DSN` et `BTK_DB_PWD`.

Le DSN est l'URL JDBC `jdbc:oracle:thin:@localhost:1521/FREEPDB1` **sans le
préfixe** `jdbc:oracle:thin:@`.

---

## Étape 1 — Vérifier que la base tourne

**Windows.** Ouvrir `services.msc` et vérifier que ces deux services sont
*En cours d'exécution* ; sinon, clic droit → *Démarrer* :

- `OracleServiceFREE` (ou `OracleServiceXE`, selon la version installée) ;
- `OracleOraDB…TNSListener`.

**Vérification en ligne de commande** (invite Anaconda ou cmd) :

```bash
lsnrctl status
```

La sortie doit lister un service `freepdb1`. Si le nom diffère (`xepdb1`,
`orclpdb1`…), c'est **ce nom-là** qu'il faudra mettre dans le DSN à l'étape 3.

C'est la même base que celle utilisée par l'application : si l'application
démarre et affiche vos agences, la base tourne.

## Étape 2 — Installer le pilote Python

Dans l'**invite Anaconda** :

```bash
pip install oracledb
```

`oracledb` fonctionne en mode *thin* : **aucun client Oracle à installer**, il
parle directement le protocole réseau d'Oracle.

## Étape 3 — Tester la connexion

C'est l'étape qui règle 90 % des problèmes. Depuis le dossier du projet :

```bash
python3 etl/test_connexion_oracle.py
```

Le mot de passe est demandé à la saisie ; il n'est écrit nulle part.

Le script ne modifie rien. Il affiche la version du serveur, le schéma courant,
puis compte les lignes des cinq tables sources :

```
Connexion à BTK_BI@localhost:1521/FREEPDB1 …
Connecté. Serveur Oracle 23.x.x.x
Schéma courant : BTK_BI | conteneur : FREEPDB1

Table source          Lignes   État
----------------------------------------------------
AGENCE                    49   OK
B_UTILISATEURS           997   OK
CLIENT_BTK             29942   OK
B_OBJECTIF               ...   OK
POINTAGE                 ...   OK

Les cinq tables sources sont lisibles : la chaîne ETL peut tourner.
```

Pour changer d'utilisateur ou de service, définir les variables avant de lancer :

```bash
# Windows (cmd)
set BTK_DB_USER=BTK_BI
set BTK_DB_DSN=localhost:1521/FREEPDB1

# macOS / Linux
export BTK_DB_USER=BTK_BI
export BTK_DB_DSN=localhost:1521/FREEPDB1
```

### Si le test échoue

| Message | Cause | Manœuvre |
|---|---|---|
| `DPY-6005` / `ORA-12541` | la base ou le listener n'est pas démarré | étape 1 |
| `ORA-01017` | identifiant ou mot de passe incorrect | vérifier le compte `BTK_BI` et son mot de passe |
| `ORA-12514` | nom de service inconnu | remplacer `FREEPDB1` par le nom vu dans `lsnrctl status` (`XEPDB1`, `ORCLPDB1`…) |
| `ORA-12154` | DSN incomplet | donner `hote:port/service`, pas seulement le service |
| `ORA-28000` | compte verrouillé | `ALTER USER BTK_BI ACCOUNT UNLOCK;` |
| `ORA-00942` sur une table | la table n'appartient pas à ce schéma | voir ci-dessous |

### `ORA-00942` : les tables ne sont pas visibles depuis `BTK_BI`

Le compte se connecte, mais les tables appartiennent à un autre schéma. Depuis
le compte propriétaire (par exemple `SYSTEM`) :

```sql
GRANT SELECT ON SYSTEM.AGENCE          TO BTK_BI;
GRANT SELECT ON SYSTEM.B_UTILISATEURS  TO BTK_BI;
GRANT SELECT ON SYSTEM.CLIENT_BTK      TO BTK_BI;
GRANT SELECT ON SYSTEM.B_OBJECTIF      TO BTK_BI;
GRANT SELECT ON SYSTEM.POINTAGE        TO BTK_BI;

-- pour que BTK_BI puisse écrire « FROM AGENCE » sans préfixer le schéma
CREATE OR REPLACE SYNONYM BTK_BI.AGENCE         FOR SYSTEM.AGENCE;
CREATE OR REPLACE SYNONYM BTK_BI.B_UTILISATEURS FOR SYSTEM.B_UTILISATEURS;
CREATE OR REPLACE SYNONYM BTK_BI.CLIENT_BTK     FOR SYSTEM.CLIENT_BTK;
CREATE OR REPLACE SYNONYM BTK_BI.B_OBJECTIF     FOR SYSTEM.B_OBJECTIF;
CREATE OR REPLACE SYNONYM BTK_BI.POINTAGE       FOR SYSTEM.POINTAGE;
```

L'application a besoin d'écrire (pointage, demandes) : ajouter
`INSERT, UPDATE, DELETE` aux `GRANT` sur les tables concernées.

Si seule `POINTAGE` manque, ce n'est pas bloquant : la chaîne tournera sans le
taux de présence. Pour la créer : `sql/setup_pointage.sql`.

## Étape 4 — Lancer la chaîne ETL sur Oracle

```bash
# Windows (cmd)
set BTK_DB_USER=BTK_BI
set BTK_DB_PWD=votre_mot_de_passe
set BTK_DB_DSN=localhost:1521/FREEPDB1
python etl\etl_agences.py --source oracle

# macOS / Linux
export BTK_DB_USER=BTK_BI BTK_DB_PWD=votre_mot_de_passe BTK_DB_DSN=localhost:1521/FREEPDB1
python3 etl/etl_agences.py --source oracle
```

La chaîne affiche alors `[extract] connecté à BTK_BI@…` puis le nombre de lignes
lues par table, l'agrégation, le contrôle de qualité et le chargement.

Trois éléments que l'extrait agrégé ne porte pas apparaissent seulement ici :
le **taux de présence** (table `POINTAGE`), le **district** (table `AGENCE`) et
l'**axe gestionnaire** (`dim_gestionnaire.csv`, `fait_objectif.csv`).

## Étape 5 — La même chose dans le notebook

Ouvrir `etl/etl_btk.ipynb` dans Jupyter, puis **Kernel → Restart Kernel and Run
All Cells**. Les sections s'enchaînent :

| Section | Ce qu'elle fait |
|---|---|
| 0. Préparation | imports, repérage du dossier du projet |
| **1. Connexion à la base Oracle** | ouvre la connexion, demande le mot de passe |
| Inventaire des tables sources | compte les lignes des 5 tables |
| 2. Collecte | exécute les 5 requêtes `SELECT` |
| 3. Nettoyage | écarte les lignes sans `SK_AGENCE` |
| 4-5. Transformation et intégration | agrège par agence, fusionne sur `SK_AGENCE` |
| 6. Contrôle de qualité | manquants, négatifs, doublons |
| 7. Chargement | écrit le datamart en étoile |
| 8. Vérification | relance le script et compare |

La cellule 1 demande le mot de passe dans une petite zone de saisie : tapez-le
puis `Entrée`, l'exécution reprend. Pour travailler **sans** Oracle, mettre
`UTILISER_ORACLE = False` en tête de cette cellule : il n'y a alors aucune
invite, et la chaîne repart de l'extrait agrégé.

Si la connexion échoue, la cellule affiche la cause et **le notebook continue**
sur l'extrait : on ne perd pas la séance.

## Étape 6 — Enchaîner la segmentation

La segmentation consomme le datamart que l'ETL vient d'écrire :

```bash
python3 clustering/segmentation_reelle.py
```

ou le notebook `clustering/segmentation_btk.ipynb`.

---

## Sans connecteur Oracle : passer par des CSV

Si `pip install oracledb` est impossible sur le poste, exporter les tables avec
**SQLcl** puis relancer la chaîne :

```bash
sql BTK_BI/votre_mot_de_passe@localhost:1521/FREEPDB1 @etl/export_sources.sql
```

Placer les cinq fichiers produits dans `etl/source/`, puis :

```bash
python3 etl/etl_agences.py --source csv
```

Le résultat est identique à celui de la source Oracle.
