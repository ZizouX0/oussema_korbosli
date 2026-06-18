# Rapport de stage PFE — gestion-agences

`Rapport_de_stage_PFE_gestion-agences.docx` is the internship report, built on
the official **ESPRIT School of Business** template (Licence Business Computing —
parcours Business Intelligence). It keeps the template's original cover page,
logos and styles, and adds the full report body for the **gestion-agences**
project (balanced application + Business Intelligence framing).

## Structure

Cover page → Résumé/Abstract → Remerciements → Sommaire (auto TOC) → Lists →
Introduction → **Ch.1** Cadre général → **Ch.2** Analyse & spécification des
besoins → **Ch.3** Conception (incl. volet décisionnel / BI) → **Ch.4**
Réalisation (incl. Power BI) → Conclusion & perspectives → Bibliographie →
Annexes.

## How to finalize it in Word

1. **Update the table of contents:** open in Word, press `Ctrl+A` then `F9`
   (choose "Update entire table"). The Sommaire is an auto-generated TOC field.
2. **Fill the placeholders** — search (`Ctrl+F`) for `[` and replace:
   - `[organisme d'accueil]` / `[host organization]` — host company name (FR + EN).
   - `[organisme d'accueil — raison sociale, …]` and the "Décrire brièvement…"
     line — section 1.2 about the host organization.
   - `[Nom & Prénom]` — academic supervisor and company supervisor (remerciements
     + cover signature block).
   - `[caractéristiques : processeur, mémoire RAM, …]` — section 4.2.1.
   - Cover page: **Soutenu le** (defense date), **dates** of the internship, and
     the supervisor names.
3. **Insert the 13 figures** — search for `à insérer` to find each placeholder
   (architecture diagram, use-case / class / sequence diagrams, DB schema, BI
   model, app screenshots, Power BI report, Gantt chart). Replace each with your
   image and a proper Word caption (Références → Insérer une légende) so the
   "Liste des figures" can be generated.

> Note: the author name on the cover was pre-filled as **Oussema KORBOSLI** (from
> the repository name) — correct it if needed.

## Source

Generated with `python-docx` from the uploaded template; the project it documents
lives in this same repository.
