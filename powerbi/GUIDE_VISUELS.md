# Remplir le template — visuels & données (pas à pas)

On pose un visuel Power BI dans chaque zone du fond, connecté aux vues `V_BI_*`.
Toutes les données sont **réelles** (celles de ta base Oracle).

## 1. Charger les données
`Obtenir les données` → **Oracle** → `localhost:1521/FREEPDB1` → mode **Import** →
cocher : `V_BI_EMPLOYES`, `V_BI_CLIENTS`, `V_BI_OBJECTIFS`, `V_BI_POINTAGE` → `Charger`.

## 2. Créer les relations (pour que les filtres agissent partout)
Vue **Modèle** → relier les 4 vues sur **`NOM_AGENCE`** (et `ANNEE_MOIS` entre
`V_BI_OBJECTIFS` et `V_BI_POINTAGE`). Sens du filtre : simple, depuis la dimension.
*(Simple : tu peux aussi garder les visuels indépendants et mettre un segment par vue.)*

## 3. Créer les mesures DAX
Clique-droit sur une table → `Nouvelle mesure`, et colle (une par une) :
```DAX
Nb Employés   = DISTINCTCOUNT(V_BI_EMPLOYES[ID_EMPLOYE])
Nb Clients    = DISTINCTCOUNT(V_BI_CLIENTS[ID_CLIENT])
Total Comptes = SUM(V_BI_OBJECTIFS[TOTAL_OUVERTURE_COMPTES])
Total Crédits = SUM(V_BI_OBJECTIFS[CREDITS_CONSO]) + SUM(V_BI_OBJECTIFS[CREDITS_IMMO]) + SUM(V_BI_OBJECTIFS[CREDITS_INVEST])
Total Épargne = SUM(V_BI_OBJECTIFS[COLLECTE_EPARGNE])
Taux Présence = AVERAGE(V_BI_POINTAGE[EST_PRESENT])
```
Formate `Taux Présence` en **pourcentage** (onglet Mesure → Format → %).

## 4. Poser un visuel dans chaque zone
| Zone du fond | Visuel | Champs |
|---|---|---|
| **KPI — Clients** | Carte | mesure `Nb Clients` |
| **KPI — Crédits** | Carte | mesure `Total Crédits` |
| **KPI — Présence** | Carte | mesure `Taux Présence` |
| **KPI — Comptes** | Carte | mesure `Total Comptes` |
| **Rôles** | Anneau | Légende = `V_BI_EMPLOYES[ROLE_LABEL]`, Valeurs = `Nb Employés` |
| **Présence** | Anneau | Légende = `V_BI_POINTAGE[STATUT]`, Valeurs = Nombre de `ID_POINTAGE` |
| **Évolution de la production** | Histogramme empilé | Axe X = `V_BI_OBJECTIFS[ANNEE_MOIS]`, Valeurs = `Total Crédits` |
| **Production par type de produit** | Histogramme + courbe | voir §5 (unpivot) |
| **Top 5 agences** | Tableau | `NOM_AGENCE`, `Nb Clients`, `Total Crédits`, `Taux Présence` |

**Top 5** : sur le tableau → volet `Filtres` → filtre sur `NOM_AGENCE` → type
**« N premiers »** = **5**, par `Total Crédits`.

## 5. Graphe « Production par type de produit »
Les types sont dans des colonnes séparées de `V_BI_OBJECTIFS`. Pour les mettre en
catégories : `Transformer les données` (Power Query) → sélectionner les colonnes
`TOTAL_OUVERTURE_COMPTES`, `CREDITS_CONSO`, `CREDITS_IMMO`, `CREDITS_INVEST`,
`CARTES_COMMANDES`, `COLLECTE_EPARGNE` → clic-droit → **« Dépivoter les colonnes »**.
Tu obtiens `Attribut` (type) + `Valeur`. Puis histogramme : Axe = `Attribut`,
Valeurs = somme de `Valeur`.

## 6. Segments (slicers) — en haut à droite
3 segments (visuel **Segment**) : `DISTRICT_AGENCE`, `ANNEE_MOIS`, `TYPE_CLIENT`.
Bouton **RESET** : `Insertion` → `Bouton` → action **« Effacer tous les segments »**.

## 7. Finitions
- Le **thème** (`btk_theme.json`) colore déjà les visuels ; garde les fonds de
  visuels à `#212329` pour qu'ils se fondent dans les cartes du fond.
- Aligne chaque visuel sur sa zone (le fond montre où chaque visuel va).
- Masque les titres redondants des visuels (le titre est déjà sur le fond).
```
```
Résultat = le rendu de `dashboard_apercu.png`, mais avec **tes vrais chiffres**.
