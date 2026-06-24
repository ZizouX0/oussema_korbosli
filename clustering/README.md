# Segmentation des agences par apprentissage non supervisé

Brique d'IA du projet : regrouper les agences BTK en **segments homogènes** par
**clustering**, pour l'aide à la décision (parcours Business Intelligence).

## Ce que fait le pipeline (`segmentation_agences.py`)
1. Charge les données (CSV réel si présent, sinon un **jeu de démonstration** réaliste).
2. **Standardise** les variables (`StandardScaler`).
3. Détermine le **nombre de clusters** : méthode du **coude** + **silhouette**.
4. **Compare** 4 modèles : K-Means, Agglomératif, GMM, DBSCAN
   (silhouette, Davies-Bouldin, Calinski-Harabasz).
5. Retient le **meilleur** modèle, projette en **PCA** et **profile** les segments.

## Lancer
```bash
pip install pandas scikit-learn matplotlib
python3 segmentation_agences.py
```
Sorties : `figures/` (choix de k, comparaison, projection PCA) et
`resultats_segmentation.csv`, `comparaison_modeles.csv`, `profils_clusters.csv`.

## Source des données : la chaîne ETL
Le fichier **`data/agences.csv`** est produit automatiquement par la chaîne
**ETL** (`../etl/etl_agences.py`), qui agrège les données par agence. Il suffit
donc d'exécuter l'ETL avant la segmentation pour travailler sur des données
cohérentes avec le tableau de bord et Power BI. Colonnes attendues :
```
agence, effectif, nb_gestionnaires, nb_clients, total_comptes,
production_credits, collecte_epargne, taux_presence
```
> Pour des données réelles : alimentez l'ETL depuis Oracle (ou un export CSV des
> vues `V_BI_*`), voir `../etl/README.md`. Le script de segmentation utilise
> automatiquement `data/agences.csv` s'il est présent.

## Résultat
3 segments (k=3, silhouette ≈ 0,74) : **grandes**, **moyennes** et **petites**
agences ; les quatre modèles testés convergent vers la même partition. Le détail
et l'interprétation figurent au chapitre « Sprint 6 : Segmentation des agences »
du rapport.
