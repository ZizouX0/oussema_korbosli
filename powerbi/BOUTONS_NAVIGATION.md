# Boutons du tableau de bord (navigation + RESET)

## 1) Barre latérale — Navigateur de pages (le plus simple, auto)
Crée les 4 boutons Résumé / Clients / Commercial / Présence d'un coup, et
**surligne tout seul** la page en cours.

1. Renomme d'abord tes 4 onglets (en bas) : `Résumé`, `Clients`, `Commercial`, `Présence`.
2. Ruban **Insertion → Boutons (Éléments) → Navigateur → Navigateur de pages**.
3. Un bloc de boutons apparaît (un par page). Place-le en **colonne à gauche** :
   `Format du visuel → Disposition en grille → Orientation = Verticale`.
4. Il fonctionne sur **toutes les pages** — pas besoin de le refaire page par page.

### Style sombre (pour coller à la maquette)
`Format du visuel` →
- **Formes → Remplissage** : `#212329` (état par défaut) ; **État = Sélectionné** → `#2E3038`
- **Texte** : couleur `#E8E9ED`, taille 13, police Segoe UI
- **Bordure** : arrondi 8

> Astuce : pour masquer une page du navigateur (ex. une page technique), clic droit
> sur l'onglet → **Masquer la page** (elle disparaît des boutons).

## 2) Bouton RESET (efface tous les filtres)
1. `Insertion → Boutons → Vide`.
2. `Format du bouton → Texte → Activé` → écris **RESET** (centré, blanc).
3. `Format du bouton → Style → Remplissage` = `#33353D`, arrondi 6.
4. `Format du bouton → **Action** → Activé` → **Type = Effacer tous les segments**.
5. Place-le en haut à droite, à côté des segments.

## 3) (Option) Boutons manuels avec icônes
Si tu veux l'icône + le libellé (📊 Résumé…) comme sur la maquette :
1. `Insertion → Boutons → Vide` → un bouton par page.
2. `Format → Icône` (choisis) + `Texte` = le nom de la page.
3. `Format → Action → Type = Navigation de page → Destination` = la page voulue.
4. Sélectionne les 4 boutons → **Copier** → **Coller** sur chaque page.
   *(Inconvénient : l'état « actif » de la page courante est à gérer à la main —
   le Navigateur de pages du §1 le fait automatiquement, d'où la recommandation.)*

## 4) Tester les boutons
En mode **Édition**, un bouton se déclenche avec **Ctrl + clic**.
En mode **Lecture** (Affichage → Vue Lecture), un simple **clic** suffit.

## Récap
| Bouton | Insertion | Action |
|---|---|---|
| Navigation (×4) | Navigateur de pages | auto (va à chaque page) |
| RESET | Bouton vide + texte | Effacer tous les segments |
