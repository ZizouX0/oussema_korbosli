# Dossier technique de soutenance

Support de préparation à la soutenance technique : chaque fonctionnalité de
l'application, sa mise en œuvre côté présentation / contrôle / métier /
persistance, puis la chaîne décisionnelle et Power BI.

```bash
cd soutenance-technique
latexmk -pdf main.tex          # produit main.pdf (21 pages)
```

| Fichier | Contenu |
|---|---|
| `01_vue_ensemble.tex` | pile technique, architecture en 4 couches, cycle de vie d'une requête |
| `02_socle.tex` | authentification et rôles, filtre, journal, notifications, entités |
| `03_fonctionnalites.tex` | une fiche par fonctionnalité (front / back / données) |
| `04_front_back.tex` | JSTL, CSS, ApexCharts ; servlets, EJB, JPA, transactions |
| `05_decisionnel.tex` | vues `V_BI_*`, schéma `BTK_BI`, ETL, Power BI, segmentation |
| `06_deploiement.tex` | Maven, WAR, WildFly, datasource, diagnostic `IJ000453` |
| `07_questions.tex` | questions probables du jury, limites, carte des URL |

Tout le contenu est relevé dans le code du dépôt (servlets, services, entités,
JSP, SQL, scripts ETL et Power BI). L'inventaire — 18 servlets, 16 services,
16 entités, 17 pages JSP — est issu d'une extraction automatique des sources.
