# Mesures DAX — référence unique (schéma BTK_BI)

Toutes les colonnes sont réelles (vérifiées dans les entités du projet).
Créer une **mesure** : clic-droit sur une table → *Nouvelle mesure* → coller → Entrée.
`Rôle` est une **colonne calculée** : ruban *Nouvelle colonne* (pas mesure).

## 1) MESURES DE BASE

```DAX
Nb Employés = DISTINCTCOUNT(B_UTILISATEURS[SK_UTILISATEUR])
```
```DAX
Nb Clients = DISTINCTCOUNT(B_CLIENTS[SK_CLIENT])
```
```DAX
Total Comptes =
      SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_CHEQUES_OA])
    + SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_EPARGNES_OA])
    + SUM(B_OBJECTIF[SOUSCRIPTION_COMPTE_COURANTS_OA])
```
```DAX
Total Crédits =
      SUM(B_OBJECTIF[PRODUCTION_CREDITS_CONSO_OA])
    + SUM(B_OBJECTIF[PRODUCTION_CREDITS_IMMO_OA])
    + SUM(B_OBJECTIF[PRODUCTION_CREDITS_INVESTISSEMENT_OA])
```
```DAX
Taux Présence =
DIVIDE(
    CALCULATE(COUNTROWS(POINTAGE), POINTAGE[STATUT] IN {"PRESENT","RETARD"}),
    COUNTROWS(POINTAGE)
)
```
```DAX
Nb Présences = CALCULATE(COUNTROWS(POINTAGE), POINTAGE[STATUT] = "PRESENT")
```
```DAX
Nb Retards = CALCULATE(COUNTROWS(POINTAGE), POINTAGE[STATUT] = "RETARD")
```
```DAX
Nb Absences = CALCULATE(COUNTROWS(POINTAGE), POINTAGE[STATUT] = "ABSENT")
```
```DAX
Nb Pointages = COUNT(POINTAGE[ID_POINTAGE])
```

## 2) COLONNE CALCULÉE (sur B_UTILISATEURS) — ruban « Nouvelle colonne »

```DAX
Rôle =
SWITCH(
    TRUE(),
    B_UTILISATEURS[EST_GESTIONNAIRE] = 1, "Gestionnaire",
    B_UTILISATEURS[EST_GESTIONNAIRE] = 0 && B_UTILISATEURS[SK_AGENCE] = 31, "Hors Commercial",
    "Conseiller"
)
```

## 3) MESURES SUPPLÉMENTAIRES (pages 2 et 3)

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

## 4) MESURES « CENTRE D'ANNEAU » (pour mieux visualiser les 2 donuts, page 1)
À afficher via une **Carte** superposée au centre de l'anneau (fond transparent).

```DAX
% Gestionnaires =
DIVIDE(
    CALCULATE(DISTINCTCOUNT(B_UTILISATEURS[SK_UTILISATEUR]), B_UTILISATEURS[Rôle] = "Gestionnaire"),
    DISTINCTCOUNT(B_UTILISATEURS[SK_UTILISATEUR])
)
```
```DAX
Taux Absentéisme = DIVIDE([Nb Absences], [Nb Pointages])
```
- Anneau **Rôles** → centre = `Nb Employés` (total) ou `% Gestionnaires`
- Anneau **Présence** → centre = `Taux Présence` (+ `Taux Absentéisme` en info-bulle)
- Formater `% Gestionnaires` et `Taux Absentéisme` en **pourcentage**.

## Formats (ruban « Outils de mesure »)
| Mesure | Format | Déc. |
|---|---|---|
| Nb Employés / Nb Clients / Total Comptes / Total Crédits | Nombre entier + séparateur milliers | 0 |
| **Taux Présence** | **Pourcentage %** | 1 |
| Nb Présences / Retards / Absences | Nombre entier | 0 |
| Total Épargne / EER* | Nombre entier + milliers | 0 |
