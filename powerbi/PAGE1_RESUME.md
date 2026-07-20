# Page 1 — RÉSUMÉ (cockpit de pilotage) — construction pas à pas

Maquette cible : `dashboard_apercu.png`. Canevas **1280 × 720** (16:9, défaut).

## A. Préparer la page
1. Onglet en bas → clic droit → **Renommer** → `Résumé`.
2. `Affichage → Thèmes → Rechercher des thèmes…` → **`btk_theme.json`** (fond sombre + cartes arrondies automatiques).
3. Volet **Format de la page** → Canevas : `16:9`.

## B. Les 4 cartes KPI (bande du haut)
Visuel **Carte** × 4, alignées côte à côte :

| Carte | Champ (mesure) | Format |
|---|---|---|
| Clients | `Nb Clients` | nombre entier, séparateur milliers |
| Production crédits | `Total Crédits` | milliers, ou « M » |
| Taux de présence | `Taux Présence` | **pourcentage**, 1 décimale |
| Comptes ouverts | `Total Comptes` | milliers |

*Format carte : `Format → Étiquette d'appel` (valeur) 27 px ; `Étiquette de catégorie` = le titre.*

## C. Anneau « Rôles »
Visuel **Anneau** · Légende = `B_UTILISATEURS[Rôle]` · Valeurs = `Nb Employés`.
→ montre Gestionnaire / Conseiller (/ Hors Commercial).

## D. Anneau « Présence »
Visuel **Anneau** · Légende = `POINTAGE[STATUT]` · Valeurs = **Nombre de** `ID_POINTAGE`
*(glisse `ID_POINTAGE` dans Valeurs → clic sur le champ → « Nombre »)*.

## E. Histogramme « Évolution de la production de crédits »
Visuel **Histogramme groupé** · Axe X = `B_OBJECTIF[ANNEE_MOIS]` · Valeurs = `Total Crédits`.
*(Trie l'axe par `ANNEE_MOIS` croissant pour l'ordre chronologique.)*

## F. Histogramme « Production par type de produit »
Visuel **Histogramme groupé** · Valeurs (glisse ces 6 mesures, **sans axe**) :
`Comptes Chèques`, `Comptes Épargne`, `Comptes Courants`,
`Crédits Conso`, `Crédits Immo`, `Crédits Invest`.
→ une barre par produit. *(Ces mesures sont dans le bloc « mesures supplémentaires ».)*

## G. Tableau « Top 5 agences »
Visuel **Tableau** · Colonnes : `AGENCE[LIBELLE_AGENCE]`, `Nb Clients`, `Total Crédits`, `Taux Présence`.
Filtre du visuel → sur `LIBELLE_AGENCE` → **N premiers = 5**, par `Total Crédits`.

## H. Les segments de pilotage (haut à droite) + RESET
3 visuels **Segment** (orientation horizontale, style « liste déroulante ») :
- `AGENCE[DISTRICT]`
- `B_OBJECTIF[ANNEE_MOIS]`
- `B_CLIENTS[TYPE_CLIENT]`

Bouton **RESET** : `Insertion → Bouton → Vide` → volet `Action` = **« Effacer tous les segments »**.

## I. Barre latérale de navigation (vers les 4 pages)
`Insertion → Éléments → Navigateur → **Navigateur de pages**` → place-le en colonne à gauche.
Il crée tout seul les boutons Résumé / Clients / Commercial / Présence.

## Pilotage (le principe)
- Clique un **district**, une **année-mois** ou un **type de client** → **toute la page se recalcule** (KPI, anneaux, histogrammes, top 5).
- Clique une part d'un anneau (ex. « Conseillers ») → ça **filtre en croisé** les autres visuels.
- `RESET` remet tout à zéro.

> Tout est net et interactif : **pas d'image de fond** (c'est le thème qui fait le look sombre) → plus de problème de zoom.
