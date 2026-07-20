# Tableau de bord Power BI BTK — Guide de construction (4 pages)

Ce tableau de bord est **volontairement plus détaillé et différent** du dashboard
embarqué dans l'application web : 4 pages analytiques qui exploitent des données que
l'appli n'affiche pas (géographie et secteur des clients, présence dans le temps,
détail complet des objectifs commerciaux).

Maquettes (design cible) :
`dashboard_apercu.png` (p.1) · `page2_clients.png` · `page3_commercial.png` · `page4_presence.png`

## Principe : thème, pas image de fond
On n'utilise **aucune image de fond** (c'est ce qui provoquait le zoom). À la place :
`Affichage → Thèmes → Rechercher des thèmes…` → charger **`btk_theme.json`**.
Le thème met le fond en sombre `#17181C` et transforme chaque visuel en **carte arrondie
`#212329`** — exactement le rendu des maquettes, mais 100 % interactif et net.

## Prérequis (étapes déjà faites)
1. Données chargées depuis le schéma **BTK_BI** (Oracle `localhost:1521/FREEPDB1`).
2. **Relations** créées (AGENCE→B_UTILISATEURS / B_CLIENTS / B_OBJECTIF sur `SK_AGENCE` ;
   B_UTILISATEURS→POINTAGE sur `SK_UTILISATEUR`).
3. **Mesures de base** créées : `Nb Employés`, `Nb Clients`, `Total Comptes`,
   `Total Crédits`, `Taux Présence`, `Nb Présences`, `Nb Retards`, `Nb Absences`,
   + colonne calculée `Rôle`.

---

## Mesures supplémentaires (pour les pages détaillées)
Crée-les une fois (clic-droit sur une table → *Nouvelle mesure*) :

```DAX
Nb Gouvernorats = DISTINCTCOUNT(B_CLIENTS[GOUVERNORAT_ADRESSE_CLIENT])
Nb Secteurs     = DISTINCTCOUNT(B_CLIENTS[SECTEUR_ACTIVITE])
Nb Types Client = DISTINCTCOUNT(B_CLIENTS[TYPE_CLIENT])

Total Épargne = SUM(B_OBJECTIF[EPARGNE_ADD_OA])
Total Packs & Cartes =
      SUM(B_OBJECTIF[SOUSCRIPTION_PACKS_PARTICULIER_OA])
    + SUM(B_OBJECTIF[SOUSCRIPTION_PACKS_PRO_OA])
    + SUM(B_OBJECTIF[SOUSCRIPTION_CARTES_UNITE_OA])

Comptes Chèques  = SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_CHEQUES_OA])
Comptes Épargne  = SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_EPARGNES_OA])
Comptes Courants = SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_COURANTS_OA])

Crédits Conso  = SUM(B_OBJECTIF[PRODUCTION_CREDITS_CONSO_OA])
Crédits Immo   = SUM(B_OBJECTIF[PRODUCTION_CREDITS_IMMO_OA])
Crédits Invest = SUM(B_OBJECTIF[PRODUCTION_CREDITS_INVESTISSEMENT_OA])

EER Particulier      = SUM(B_OBJECTIF[EER_PARTICULIER_OA])
EER Hors Particulier = SUM(B_OBJECTIF[EER_HORS_PARTICULIER_OA])
```

---

## PAGE 1 — Résumé (`dashboard_apercu.png`)
| Zone | Visuel Power BI | Champs |
|---|---|---|
| KPI Clients | Carte | `Nb Clients` |
| KPI Crédits | Carte | `Total Crédits` |
| KPI Présence | Carte | `Taux Présence` |
| KPI Comptes | Carte | `Total Comptes` |
| Rôles | Anneau | Légende `B_UTILISATEURS[Rôle]` · Valeurs `Nb Employés` |
| Présence | Anneau | Légende `POINTAGE[STATUT]` · Valeurs = Nombre de `ID_POINTAGE` |
| Évolution production | Histogramme groupé | Axe `B_OBJECTIF[ANNEE_MOIS]` · Valeurs `Total Crédits` |
| Top 5 agences | Tableau | `AGENCE[LIBELLE_AGENCE]`, `Nb Clients`, `Total Crédits`, `Taux Présence` — filtre **N premiers = 5** par `Total Crédits` |

## PAGE 2 — Clients (`page2_clients.png`)
| Zone | Visuel | Champs |
|---|---|---|
| KPI | 4 Cartes | `Nb Clients` · `Nb Gouvernorats` · `Nb Secteurs` · `Nb Types Client` |
| Type de client | Anneau | Légende `B_CLIENTS[TYPE_CLIENT]` · Valeurs `Nb Clients` |
| Sexe | Anneau | Légende `B_CLIENTS[SEXE]` · Valeurs `Nb Clients` |
| Répartition par gouvernorat | Histogramme **barres** | Axe Y `B_CLIENTS[GOUVERNORAT_ADRESSE_CLIENT]` · Valeurs `Nb Clients` — tri décroissant, **N premiers = 8** |
| Clients par secteur | Histogramme barres | Axe Y `B_CLIENTS[SECTEUR_ACTIVITE]` · Valeurs `Nb Clients` |
| Statut du portefeuille | Anneau | Légende `B_CLIENTS[STATUT_CLIENT]` · Valeurs `Nb Clients` |

> 💡 *Option carte géo* : tu peux remplacer les barres « gouvernorat » par le visuel
> **Carte choroplèthe** (Azure Map) — Emplacement = `GOUVERNORAT_ADRESSE_CLIENT`,
> Taille = `Nb Clients`. Ça fait une vraie carte de la Tunisie.

## PAGE 3 — Performance commerciale (`page3_commercial.png`)
| Zone | Visuel | Champs |
|---|---|---|
| KPI | 4 Cartes | `Total Comptes` · `Total Crédits` · `Total Épargne` · `Total Packs & Cartes` |
| Souscriptions par type de compte | Histogramme groupé | Valeurs = `Comptes Chèques` + `Comptes Épargne` + `Comptes Courants` (3 mesures, **sans axe**) |
| Production de crédits | Histogramme groupé | Valeurs = `Crédits Conso` + `Crédits Immo` + `Crédits Invest` |
| EER — Effort équipement | Anneau | Valeurs = `EER Particulier` + `EER Hors Particulier` |
| Évolution mensuelle | Graphique en **courbes** | Axe `B_OBJECTIF[ANNEE_MOIS]` · Valeurs `Total Crédits` |
| Objectifs par agence | Tableau | `AGENCE[LIBELLE_AGENCE]`, `Total Comptes`, `Total Crédits`, `Total Packs & Cartes` — N premiers = 5 |

## PAGE 4 — Présence / RH (`page4_presence.png`)
| Zone | Visuel | Champs |
|---|---|---|
| KPI | 4 Cartes | `Taux Présence` · `Nb Présences` · `Nb Retards` · `Nb Absences` |
| Évolution du taux de présence | Graphique en courbes | Axe `POINTAGE[DATE_POINTAGE]` (niveau **Mois**) · Valeurs `Taux Présence` |
| Statuts | Anneau | Légende `POINTAGE[STATUT]` · Valeurs = Nombre de `ID_POINTAGE` |
| Source | Anneau | Légende `POINTAGE[SOURCE]` · Valeurs = Nombre de `ID_POINTAGE` |
| Taux de présence par agence | Histogramme barres | Axe Y `AGENCE[LIBELLE_AGENCE]` · Valeurs `Taux Présence` |
| Agences à surveiller | Tableau | `AGENCE[LIBELLE_AGENCE]`, `AGENCE[DISTRICT]`, `Taux Présence` — tri **croissant** (5 plus faibles) |

---

## Navigation entre les 4 pages (la barre latérale)
1. Renomme les onglets en bas : **Résumé · Clients · Commercial · Présence**.
2. `Insertion → Éléments → Navigateur → **Navigateur de pages**`.
3. Place-le en colonne à gauche → il crée automatiquement les boutons vers chaque page.
   *(Ou : `Insertion → Boutons` + action « Navigateur de pages ».)*

## Segments (slicers) communs
En haut à droite de chaque page, ajoute des **Segments** :
- p.1/3 : `AGENCE[DISTRICT]`, `B_OBJECTIF[ANNEE_MOIS]`
- p.2 : `B_CLIENTS[TYPE_CLIENT]`, `B_CLIENTS[GOUVERNORAT_ADRESSE_CLIENT]`
- p.4 : `POINTAGE[STATUT]`, `AGENCE[DISTRICT]`
Bouton **RESET** : `Insertion → Bouton` → action **« Effacer tous les segments »**.

## Finitions
- **Thème** appliqué → fonds sombres et cartes arrondies automatiques.
- Formats : `Taux Présence` en **%** ; montants avec **séparateur de milliers**.
- Masque les titres d'axe redondants ; garde des titres de visuel courts.
- Aligne chaque visuel sur la zone correspondante de la maquette.
