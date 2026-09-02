# Captures de la démonstration

Cinq captures, reprises telles quelles par les diapositives 34 à 38 de la
présentation. **Les noms de fichier doivent être exactement ceux-ci :**

| Fichier attendu | Écran | Diapositive |
|---|---|---|
| `01-auth-admin.png` | page de connexion, compte `admin` | 34 |
| `02-ajout-employe.png` | écran Employés, formulaire d'ajout rempli | 35 |
| `03-pointage-utilisateur.png` | écran Pointage, connecté en `USER` | 36 |
| `04-demande-directeur.png` | Validation des modifications, connecté en `DIRECTEUR_COMMERCIAL` | 37 |
| `05-assistant.png` | tableau de bord avec l'assistant ouvert | 38 |

Puis régénérer la présentation :

```bash
node presentation/build_presentation.js
```

Tant qu'un fichier manque, la diapositive affiche un **cadre d'attente** portant
le nom du fichier attendu : la présentation reste constructible, et il est
immédiat de voir ce qui n'a pas encore été fourni.

Format conseillé : PNG, largeur ≥ 1600 px, fenêtre du navigateur sans les
onglets ni la barre d'adresse si possible.
