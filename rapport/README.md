# Rapport de stage PFE — gestion-agences

`Rapport_de_stage_PFE_gestion-agences.docx` is the internship report, built on
the official **ESPRIT School of Business** template (Licence Business Computing —
parcours Business Intelligence). It keeps the template's original cover page,
logos and styles, and adds the full report body for the **gestion-agences**
project (balanced application + Business Intelligence framing).

Personalized with: **Oussema Korbosli** (étudiant), **Heni Abidi** (encadrant
académique), **Melek Elmoula** (maître de stage), at **BTK – Banque
Tuniso-Koweïtienne**.

## Structure

Cover page → Résumé/Abstract → Remerciements → Sommaire (auto TOC) → Lists →
Introduction → **Plan du rapport** → **Ch.1** Cadre général → **Ch.2** Analyse &
spécification des besoins → **Ch.3** Conception (incl. volet décisionnel / BI) →
**Ch.4** Réalisation (incl. Power BI) → Conclusion & perspectives → Bibliographie
→ Annexes.

The cover's generic "LOGOTEXT" placeholder is replaced with the BTK logo
(`btk_logo_cover.png`, fitted to the placeholder box); the Esprit School of
Business logo on the cover is kept unchanged.

## Diagrams (`diagrams/`)

8 figures are already **embedded** in the document: the BTK logo plus 7 diagrams
drawn from the project (PlantUML sources + PNGs kept in `diagrams/`, regenerate
the diagrams with `generate_diagrams.py` + `plantuml.jar`):

| Fig | Figure | File |
|-----|---------|------|
| 1  | Logo de la BTK             | `btk_logo.png` |
| 2  | Cas d'utilisation global   | `usecase.png` |
| 3  | Architecture en couches    | `architecture.png` |
| 4  | Diagramme de classes       | `classes.png` |
| 5  | Séquence « Validation d'une demande » | `sequence.png` |
| 6  | Schéma relationnel (BD)    | `er.png` |
| 7  | Modèle décisionnel (V_BI_*)| `bi.png` |
| 13 | Diagramme de Gantt         | `gantt.png` |

Section 1.2 (présentation de l'organisme) is filled with a presentation of the
BTK — fiche signalétique, historique, structure du capital, activités, réseau.

## How to finalize it in Word

1. **Update the table of contents:** open in Word, press `Ctrl+A` then `F9`
   (choose "Update entire table"). The Sommaire is an auto-generated TOC field.
2. **Remaining placeholders** — search (`Ctrl+F`) for `[` :
   - Section 1.2.5 — the host service/direction at BTK (`[Préciser le service…]`).
   - Section 4.2.1 — poste de travail (processeur, RAM, OS).
   - Cover page — **Soutenu le** (defense date) and the internship **dates**.
3. **Remaining figures to add** (search `à insérer`) — only the **app
   screenshots** remain (**Fig 8–12**: login, dashboard, management modules,
   requests, Power BI report). Add each with a Word caption (Références → Insérer
   une légende). The BTK logo (Fig 1) and all diagrams are already embedded.

## Source

Generated with `python-docx` from the uploaded template; diagrams rendered with
PlantUML. The project it documents lives in this same repository.
