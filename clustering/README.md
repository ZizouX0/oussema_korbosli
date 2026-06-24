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

## Utiliser VOS données réelles
Exportez vos vues `V_BI_*` agrégées **par agence** dans **`data/agences.csv`**
avec les colonnes :
```
agence, effectif, nb_gestionnaires, nb_clients, total_comptes,
production_credits, collecte_epargne, taux_presence
```
Le script les utilisera automatiquement à la place du jeu de démonstration.

> Exemple de requête SQL (à adapter) : agréger `V_BI_EMPLOYES` (effectif,
> gestionnaires), `V_BI_CLIENTS` (clients), `V_BI_OBJECTIFS` (comptes, crédits,
> épargne) et `V_BI_POINTAGE` (taux de présence) par `NOM_AGENCE`.

## Résultat de démonstration
3 segments (k=3, silhouette ≈ 0,71) : **grandes**, **moyennes** et **petites**
agences. Le détail et l'interprétation figurent au chapitre « Segmentation des
agences » du rapport.
