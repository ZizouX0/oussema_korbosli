# Rapport de stage PFE — projet LaTeX

Projet LaTeX du rapport de stage (Esprit School of Business, Licence Business
Computing — Business Intelligence) pour le projet **gestion-agences** réalisé à
la **BTK**. Le PDF compilé est inclus : **`main.pdf`**.

## Contenu

```
rapport-latex/
├── main.tex              ← fichier principal (à compiler)
├── main.pdf              ← rapport compilé (31 pages)
├── references.bib        ← bibliographie / nétographie
├── chapters/             ← page de garde + chapitres (un fichier par partie)
├── diagrams/             ← diagrammes (.png) + sources PlantUML (.puml) + générateur
├── images/               ← logos (ESB, BTK)
├── tables/  annexes/     ← annexes
```

## Compiler le rapport sur un autre PC

### Option 1 — Overleaf (le plus simple, rien à installer)
1. Aller sur https://www.overleaf.com → **New Project → Upload Project**.
2. Téléverser le dossier `rapport-latex` (ou le `.zip`).
3. Menu → **Main document = `main.tex`**, **Compiler = pdfLaTeX**.
4. Cliquer **Recompile**.

### Option 2 — Installation locale (TeX Live ou MiKTeX)
Depuis le dossier `rapport-latex/` :
```bash
# méthode simple (auto, recommandé)
latexmk -pdf main.tex

# ou méthode manuelle (pour la bibliographie)
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

### Option 3 — Tectonic (moteur autonome, télécharge les paquets)
```bash
tectonic main.tex
```

> Paquets requis (présents dans TeX Live complet / Overleaf) : `newtx`,
> `babel-french`, `geometry`, `setspace`, `caption`, `fancyhdr`, `titlesec`,
> `tabularx`, `longtable`, `enumitem`, `hyperref`, `cleveref`, `booktabs`.

## Regénérer les diagrammes (optionnel)
Les diagrammes sont déjà inclus en `.png`. Pour les régénérer après modification
des sources `.puml` : `java -jar plantuml.jar -tpng diagrams/*.puml`
(ou `python3 diagrams/generate_diagrams.py` avec `plantuml.jar`).
