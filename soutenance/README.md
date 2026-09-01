# Documents de soutenance

```bash
cd soutenance
latexmk -pdf speech.tex
latexmk -pdf questions-reponses.tex
latexmk -pdf questions-jury.tex
```

| Document | Contenu |
|---|---|
| `speech.pdf` | Le speech de soutenance, **chiffres vérifiés** — 5 corrections, récapitulées en dernière page |
| `questions-reponses.pdf` | Les questions/réponses préparées, **vérifiées** — 6 corrections, doublon supprimé, tableau des tests remplacé par celui du rapport |
| `questions-jury.pdf` | Banque complète des questions que le jury peut poser, par thème, avec les questions pièges signalées |

`preambule.tex` est le préambule LaTeX commun aux trois.

Les chiffres ont été recoupés avec le code, le datamart (`clustering/data/`),
les résultats de la segmentation (`clustering/comparaison_modeles_reelles.csv`)
et le rapport.
