# Template Power BI — Tableau de bord décisionnel BTK

Template pour construire, dans **Power BI Desktop**, le tableau de bord décisionnel
au thème sombre (style « ZoomCharts »), distinct du tableau de bord embarqué de
l'application.

## Contenu du dossier
| Fichier | Rôle |
|---|---|
| `template_background.png` | **Image de fond** du canvas (sidebar + zones de cartes vides), format Power BI 1280×720 |
| `btk_theme.json` | **Thème** Power BI (couleurs, polices, styles des visuels) |
| `dashboard_apercu.png` | **Aperçu** du rendu final visé (référence) |
| `generate_dashboard.py` / `generate_template.py` | Scripts qui régénèrent l'aperçu et le fond |

## Étapes dans Power BI Desktop

**1. Appliquer le thème**
`Affichage` → `Thèmes` → `Rechercher des thèmes` → sélectionner **`btk_theme.json`**.

**2. Mettre l'image de fond**
Volet `Format de la page` → `Arrière-plan du canevas` → `Parcourir` →
**`template_background.png`** → Transparence **0 %**, Ajustement **« Ajuster »**.
Régler la taille de page sur **1280×720** (16:9).

**3. Connecter les données (vues décisionnelles)**
`Obtenir les données` → **Oracle** → serveur `localhost:1521/FREEPDB1` →
importer les vues : `V_BI_EMPLOYES`, `V_BI_CLIENTS`, `V_BI_OBJECTIFS`,
`V_BI_POINTAGE`.

**4. Poser un visuel dans chaque zone du fond**
| Zone du fond | Visuel Power BI | Vue / champs |
|---|---|---|
| KPI — Clients | Carte | `V_BI_CLIENTS` : nombre de clients |
| KPI — Crédits | Carte | `V_BI_OBJECTIFS` : somme `CREDITS_*` |
| KPI — Présence | Carte | `V_BI_POINTAGE` : moyenne `EST_PRESENT` |
| KPI — Comptes | Carte | `V_BI_OBJECTIFS` : `TOTAL_OUVERTURE_COMPTES` |
| Rôles | Anneau (donut) | `V_BI_EMPLOYES` : par `ROLE_LABEL` |
| Présence | Anneau (donut) | `V_BI_POINTAGE` : Présents/Retards/Absents |
| Évolution de la production | Histogramme | `V_BI_OBJECTIFS` : crédits par `ANNEE_MOIS` |
| Production par type de produit | Histogramme + courbe | `V_BI_OBJECTIFS` : comptes/crédits/épargne |
| Top 5 agences | Tableau | `V_BI_*` agrégées par `NOM_AGENCE` |

**5. Ajouter les segments (slicers)** en haut à droite : `District`, `ANNEE_MOIS`,
`TYPE_CLIENT`, plus un bouton **Réinitialiser les filtres**.

> Astuce : le thème colore automatiquement les visuels. Garde les fonds de visuels
> en `#212329` (déjà dans le thème) pour qu'ils se fondent dans les cartes du fond.

## Données de démonstration
En attendant l'export réel, l'aperçu (`dashboard_apercu.png`) est alimenté par le
datamart de la chaîne ETL (jeu représentatif). Une fois tes vraies vues connectées,
le rendu est identique avec tes chiffres réels. Voir `../etl/README.md`.
