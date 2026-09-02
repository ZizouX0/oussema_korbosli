// Soutenance PFE — BTK / Oussema Korbosli  (style aligné sur le modèle ESB fourni)
const pptxgen = require("pptxgenjs");
const path = require("path");
const { execSync } = require("child_process");
const fs = require("fs");
const R = "/home/user/oussema_korbosli/rapport-latex";
const img = (p) => path.join(R, p);

/* palette relevée sur le modèle */
const NAVY = "0A2558", ACC = "2B58A5", MID = "1D4EA0", LITE = "3C6FC3",
      NUMB = "4E74B4", BG = "F4F5FA", WHITE = "FFFFFF",
      INK = "1B2A44", MUTED = "6B7A90", CARD = "FFFFFF", EDGE = "DDE3ED";
const HF = "Georgia", BF = "Calibri";
const W = 13.333, H = 7.5, M = 0.62;
const FOOT = "Gestion des agences BTK — PFE Oussema Korbosli";

const pptx = new pptxgen();
pptx.defineLayout({ name: "BTK169", width: 13.333, height: 7.5 });
pptx.layout = "BTK169";
pptx.author = "Oussema Korbosli";
pptx.title = "Soutenance PFE — Gestion des agences BTK";

let pageNo = 0;
function footer(s) {
  pageNo++;
  s.addText(FOOT, { x: M, y: H - 0.44, w: 7, h: 0.26, fontFace: BF, fontSize: 9,
    color: MUTED, margin: 0, valign: "middle" });
  s.addText(String(pageNo), { x: W - 1.15, y: H - 0.44, w: 0.5, h: 0.26, fontFace: BF,
    fontSize: 9, color: MUTED, align: "right", margin: 0, valign: "middle" });
}
/* slide de contenu : bandeau navy + corps clair */
function slide(title) {
  const s = pptx.addSlide();
  s.background = { color: BG };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: 1.12, fill: { color: NAVY } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 1.12, w: W, h: 0.05, fill: { color: ACC } });
  s.addText(title, { x: M, y: 0.16, w: 11.9, h: 0.8, fontFace: HF, fontSize: 26,
    bold: true, color: WHITE, margin: 0, valign: "middle" });
  footer(s);
  return s;
}
/* slide pleine couleur navy */
function navySlide() {
  const s = pptx.addSlide();
  s.background = { color: NAVY };
  footer(s);
  return s;
}
/* séparateur de partie */
function divider(num, title) {
  const s = navySlide();
  s.addText(num, { x: M + 0.2, y: 0.55, w: 3, h: 1.0, fontFace: HF, fontSize: 54,
    bold: true, color: NUMB, margin: 0, valign: "middle" });
  s.addText("PARTIE " + num, { x: M + 0.25, y: 2.55, w: 8, h: 0.34,
    fontFace: BF, fontSize: 11.5, bold: true, color: LITE, charSpacing: 3, margin: 0, valign: "middle" });
  s.addText(title, { x: M + 0.2, y: 2.94, w: 11.5, h: 0.8, fontFace: HF, fontSize: 32,
    bold: true, color: WHITE, margin: 0, valign: "middle" });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 4.72, w: W, h: 0.05, fill: { color: ACC } });
  return s;
}
function card(s, x, y, w, h, fill) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06,
    fill: { color: fill || CARD }, line: { color: fill ? fill : EDGE, width: 1 } });
}
function bullets(s, x, y, w, items, fs) {
  const size = fs || 14;
  items.forEach((t, i) => {
    const yy = y + i * (size >= 14 ? 0.56 : 0.5);
    s.addShape(pptx.ShapeType.ellipse, { x, y: yy + 0.16, w: 0.12, h: 0.12,
      fill: { color: LITE }, line: { color: LITE } });
    s.addText(t, { x: x + 0.3, y: yy, w: w - 0.3, h: 0.46, fontFace: BF,
      fontSize: size, color: INK, margin: 0, valign: "middle" });
  });
}
function stat(s, x, y, w, h, value, label) {
  card(s, x, y, w, h);
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.07, fill: { color: LITE } });
  s.addText(value, { x: x + 0.1, y: y + h * 0.16, w: w - 0.2, h: h * 0.46, fontFace: HF,
    fontSize: 26, bold: true, color: NAVY, align: "center", margin: 0, valign: "middle" });
  s.addText(label, { x: x + 0.1, y: y + h * 0.62, w: w - 0.2, h: h * 0.3, fontFace: BF,
    fontSize: 11.5, color: MUTED, align: "center", margin: 0, valign: "middle" });
}
const dim = {};
function fit(s, file, bx, by, bw, bh) {
  // Capture pas encore fournie : on pose un cadre d'attente nommé, pour que la
  // construction aboutisse et que l'on voie tout de suite ce qui manque.
  if (!fs.existsSync(img(file))) {
    s.addShape(pptx.ShapeType.roundRect, { x: bx, y: by, w: bw, h: bh, rectRadius: 0.06,
      fill: { color: "F0F3F8" }, line: { color: LITE, width: 1.5, dashType: "dash" } });
    s.addText("Capture attendue\n" + file, { x: bx, y: by, w: bw, h: bh, fontFace: BF,
      fontSize: 12, color: MUTED, align: "center", valign: "middle", margin: 0,
      lineSpacing: 18 });
    return;
  }
  if (!dim[file]) dim[file] = execSync(
    `python3 -c "from PIL import Image;w,h=Image.open('${img(file)}').size;print(w,h)"`
  ).toString().trim().split(/\s+/).map(Number);
  const r = dim[file][0] / dim[file][1];
  let w = bw, h = bw / r;
  if (h > bh) { h = bh; w = bh * r; }
  s.addImage({ path: img(file), x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w, h });
}

/* ============================ 1 · TITRE ============================ */
{
  const s = navySlide();
  // motif : lignes verticales fines à droite
  for (let i = 0; i < 6; i++)
    s.addShape(pptx.ShapeType.rect, { x: 10.55 + i * 0.42, y: 0, w: 0.015, h: H,
      fill: { color: LITE } });
  s.addImage({ path: img("images/logo_esb.png"), x: M, y: 0.42, w: 1.72, h: 1.04 });
  s.addImage({ path: img("images/logo_btk.png"), x: 12.0, y: 0.42, w: 0.72, h: 0.75 });
  s.addText("PROJET DE FIN D'ÉTUDES", { x: M, y: 1.95, w: 9.4, h: 0.34,
    fontFace: BF, fontSize: 11.5, bold: true, color: LITE, charSpacing: 3, margin: 0 });
  s.addText("Système intelligent de gestion des rôles et\nde pointage avec tableau de bord décisionnel",
    { x: M, y: 2.4, w: 9.6, h: 1.5, fontFace: HF, fontSize: 28, bold: true, color: WHITE,
      lineSpacing: 38, margin: 0 });
  s.addText("Business Intelligence", { x: M, y: 4.0, w: 6, h: 0.44, fontFace: HF,
    fontSize: 19, italic: true, color: "9FB6DC", margin: 0 });
  s.addShape(pptx.ShapeType.rect, { x: M, y: 4.56, w: 1.35, h: 0.03, fill: { color: LITE } });
  s.addText("Présenté par : Oussema Korbosli", { x: M, y: 4.86, w: 7, h: 0.34,
    fontFace: BF, fontSize: 14, bold: true, color: WHITE, margin: 0 });
  s.addText([{ text: "Maître de stage : ", options: { bold: true } },
             { text: "M. ELMOULA Melek Aziz" }],
    { x: M, y: 5.42, w: 7, h: 0.3, fontFace: BF, fontSize: 12.5, color: "D5DEEE", margin: 0 });
  s.addText([{ text: "Encadrant académique : ", options: { bold: true } },
             { text: "M. ABIDI Heni" }],
    { x: M, y: 5.75, w: 7, h: 0.3, fontFace: BF, fontSize: 12.5, color: "D5DEEE", margin: 0 });
  s.addText("BTK – Banque Tuniso-Koweïtienne   ·   Année universitaire 2025/2026",
    { x: M, y: 6.36, w: 9, h: 0.32, fontFace: BF, fontSize: 11.5, color: LITE, margin: 0 });
}

/* ============================ 2 · PLAN ============================ */
{
  const s = pptx.addSlide();
  s.background = { color: BG };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 3.62, h: H, fill: { color: NAVY } });
  s.addText("PLAN", { x: 0.55, y: 3.1, w: 3, h: 1.0, fontFace: HF, fontSize: 40,
    bold: true, color: WHITE, margin: 0, valign: "middle" });
  const parts = [
    ["01", "Contexte général"], ["02", "Spécifications des besoins"],
    ["03", "Conception & architecture"], ["04", "Volet décisionnel & réalisation"],
    ["05", "Intelligence artificielle & démonstration"], ["06", "Conclusion & perspectives"],
  ];
  parts.forEach((p, i) => {
    const col = Math.floor(i / 3), row = i % 3;
    const x = 4.35 + col * 4.5, y = 1.15 + row * 1.9;
    s.addText(p[0], { x, y, w: 1.2, h: 0.66, fontFace: HF, fontSize: 30, bold: true,
      color: NUMB, margin: 0, valign: "middle" });
    s.addText(p[1], { x, y: y + 0.74, w: 4.2, h: 0.44, fontFace: BF, fontSize: 14.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
  });
  footer(s);
}

/* ======================= PARTIE 01 ======================= */
divider("01", "Contexte général");

/* -- contexte / citation -- */
{
  const s = slide("Contexte général");
  card(s, M, 1.6, 12.1, 1.62, NAVY);
  s.addText("« Une donnée dispersée ne décide rien : c'est en la consolidant\nqu'elle devient un instrument de pilotage. »",
    { x: M + 0.5, y: 1.6, w: 11.1, h: 1.62, fontFace: HF, fontSize: 18, italic: true,
      color: WHITE, margin: 0, valign: "middle", lineSpacing: 28 });
  bullets(s, M, 3.5, 12.1, [
    "Un réseau de 45 agences réparties sur tout le territoire tunisien",
    "Des données d'activité éclatées entre plusieurs fichiers et applications",
    "Un besoin de piloter la performance commerciale et l'assiduité des équipes",
    "Une direction qui doit décider vite, sur des indicateurs fiables et à jour",
  ], 14);
  card(s, M, 5.85, 12.1, 0.85);
  s.addText("Objectif du projet : centraliser la gestion du réseau et transformer les données opérationnelles en indicateurs d'aide à la décision.",
    { x: M + 0.35, y: 5.85, w: 11.4, h: 0.85, fontFace: BF, fontSize: 13, color: NAVY,
      margin: 0, valign: "middle" });
}

/* -- présentation BTK -- */
{
  const s = slide("Présentation de l'organisme d'accueil");
  card(s, M, 1.62, 6.05, 4.95);
  fit(s, "images/logo_btk.png", M + 0.4, 1.9, 1.1, 1.1);
  s.addText("BTK – Banque Tuniso-Koweïtienne", { x: M + 0.4, y: 3.12, w: 5.2, h: 0.42,
    fontFace: HF, fontSize: 17, bold: true, color: NAVY, margin: 0, valign: "middle" });
  bullets(s, M + 0.4, 3.62, 5.25, [
    "Banque universelle de droit tunisien",
    "Créée le 25 février 1981 (coopération Tunisie – Koweït)",
    "Capital social de 200 millions de dinars",
    "Siège social à Tunis, réseau national",
  ], 12.5);
  s.addText("STAGE EFFECTUÉ", { x: 7.05, y: 1.68, w: 5.7, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  const info = [["Département", "DATA"], ["Période", "16 février → 16 juin 2026"],
                ["Durée", "4 mois"], ["Encadrement", "M. ELMOULA Melek Aziz"]];
  info.forEach((it, i) => {
    const y = 2.02 + i * 1.16;
    card(s, 7.05, y, 5.7, 1.0);
    s.addShape(pptx.ShapeType.rect, { x: 7.05, y, w: 0.08, h: 1.0, fill: { color: LITE } });
    s.addText(it[0], { x: 7.35, y: y + 0.1, w: 5.2, h: 0.34, fontFace: BF, fontSize: 11,
      color: MUTED, margin: 0, valign: "middle" });
    s.addText(it[1], { x: 7.35, y: y + 0.46, w: 5.2, h: 0.4, fontFace: HF, fontSize: 14.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
  });
}

/* -- le réseau en chiffres -- */
{
  const s = slide("Le réseau BTK en chiffres");
  const st = [["45", "agences"], ["997", "employés"], ["29 942", "clients"], ["24", "gouvernorats"]];
  st.forEach((v, i) => stat(s, M + i * 3.08, 1.75, 2.86, 1.75, v[0], v[1]));
  const st2 = [["105 K", "comptes ouverts"], ["1,40 Md", "production de crédits"],
               ["253 M", "collecte d'épargne"], ["87,9 %", "taux de présence"]];
  st2.forEach((v, i) => stat(s, M + i * 3.08, 3.85, 2.86, 1.75, v[0], v[1]));
  card(s, M, 5.92, 12.1, 0.8, NAVY);
  s.addText("Chiffres issus du datamart réel produit par la chaîne ETL du projet",
    { x: M, y: 5.92, w: 12.1, h: 0.8, fontFace: BF, fontSize: 12.5, color: "CBD8EE",
      align: "center", margin: 0, valign: "middle" });
}

/* -- problématiques -- */
{
  const s = slide("Problématiques");
  const pb = [
    "Des données d'activité dispersées, saisies et consolidées manuellement",
    "Un suivi de la présence des employés sans traçabilité fiable",
    "Aucune vision consolidée de la performance du réseau d'agences",
    "Des indicateurs de pilotage indisponibles au moment de décider",
  ];
  pb.forEach((t, i) => {
    const y = 1.72 + i * 1.28;
    card(s, M, y, 12.1, 1.1);
    s.addShape(pptx.ShapeType.roundRect, { x: M + 0.28, y: y + 0.26, w: 0.58, h: 0.58,
      rectRadius: 0.1, fill: { color: NAVY } });
    s.addText(String(i + 1), { x: M + 0.28, y: y + 0.26, w: 0.58, h: 0.58, fontFace: HF,
      fontSize: 19, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(t, { x: M + 1.1, y, w: 10.7, h: 1.1, fontFace: BF, fontSize: 14.5,
      color: INK, margin: 0, valign: "middle" });
  });
}

/* -- étude de l'existant -- */
{
  const s = slide("Étude de l'existant");
  s.addText("SOLUTIONS ENVISAGÉES", { x: M, y: 1.68, w: 5.5, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  const outils = [["Tableurs Excel", "Gestion manuelle des données"],
                  ["Progiciel du marché", "Solution intégrée sur étagère"],
                  ["Développement sur mesure", "Application adaptée au métier"]];
  outils.forEach((o, i) => {
    const y = 2.05 + i * 1.24;
    card(s, M, y, 5.5, 1.06, i === 2 ? NAVY : CARD);
    s.addText(o[0], { x: M + 0.3, y: y + 0.12, w: 4.9, h: 0.38, fontFace: HF, fontSize: 14.5,
      bold: true, color: i === 2 ? WHITE : NAVY, margin: 0, valign: "middle" });
    s.addText(o[1], { x: M + 0.3, y: y + 0.52, w: 4.9, h: 0.36, fontFace: BF, fontSize: 11.5,
      color: i === 2 ? "CBD8EE" : MUTED, margin: 0, valign: "middle" });
  });
  s.addText("→", { x: 6.35, y: 3.3, w: 0.6, h: 0.6, fontFace: BF, fontSize: 26, bold: true,
    color: LITE, align: "center", margin: 0, valign: "middle" });
  s.addText("LIMITES CONSTATÉES", { x: 7.15, y: 1.68, w: 5.6, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  card(s, 7.15, 2.05, 5.6, 3.44);
  bullets(s, 7.4, 2.3, 5.15, [
    "Risque d'erreurs et de doublons de saisie",
    "Pas de gestion des rôles ni des droits",
    "Aucune traçabilité des opérations sensibles",
    "Coût élevé des progiciels du marché",
    "Restitution des indicateurs impossible",
  ], 12.5);
  card(s, M, 5.78, 12.1, 0.82, NAVY);
  s.addText("Choix retenu : une solution développée sur mesure, alignée sur les processus réels de la BTK",
    { x: M, y: 5.78, w: 12.1, h: 0.82, fontFace: BF, fontSize: 13, color: WHITE,
      align: "center", margin: 0, valign: "middle" });
}

/* -- solution proposée -- */
{
  const s = slide("Solution proposée");
  const cols = [
    ["Application web", "Gestion centralisée des agences, employés, clients et objectifs · rôles et droits · pointage · circuits de validation", "Jakarta EE · Oracle"],
    ["Chaîne décisionnelle", "Processus ETL consolidant les données dans un datamart en étoile, restitué par des tableaux de bord Power BI", "Python · Power BI"],
    ["Intelligence artificielle", "Segmentation automatique des agences en profils homogènes pour un pilotage différencié du réseau", "scikit-learn"],
  ];
  cols.forEach((c, i) => {
    const x = M + i * 4.13;
    card(s, x, 1.7, 3.83, 4.5);
    s.addShape(pptx.ShapeType.rect, { x, y: 1.7, w: 3.83, h: 0.08, fill: { color: LITE } });
    s.addShape(pptx.ShapeType.roundRect, { x: x + 0.3, y: 2.02, w: 0.6, h: 0.6,
      rectRadius: 0.1, fill: { color: NAVY } });
    s.addText(String(i + 1), { x: x + 0.3, y: 2.02, w: 0.6, h: 0.6, fontFace: HF,
      fontSize: 19, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(c[0], { x: x + 0.3, y: 2.78, w: 3.25, h: 0.72, fontFace: HF, fontSize: 16.5,
      bold: true, color: NAVY, margin: 0, valign: "top" });
    s.addText(c[1], { x: x + 0.3, y: 3.56, w: 3.25, h: 1.85, fontFace: BF, fontSize: 12.5,
      color: INK, margin: 0, lineSpacing: 19, valign: "top" });
    s.addText(c[2], { x: x + 0.3, y: 5.6, w: 3.25, h: 0.36, fontFace: BF, fontSize: 11,
      bold: true, color: LITE, margin: 0 });
  });
  s.addText("Une seule solution, de la saisie opérationnelle jusqu'à l'aide à la décision.",
    { x: M, y: 6.42, w: 12.1, h: 0.4, fontFace: BF, fontSize: 13, italic: true,
      color: MUTED, align: "center", margin: 0 });
}

/* -- méthodologie CRISP-DM -- */
{
  const s = slide("Méthodologie adoptée : CRISP-DM");
  s.addText("Projet centré sur les données : Scrum structure la production logicielle, mais ne couvre pas les étapes d'analyse et de valorisation des données.",
    { x: M, y: 1.42, w: 12.1, h: 0.5, fontFace: BF, fontSize: 13, color: INK, margin: 0 });
  // le cycle CRISP-DM à gauche
  fit(s, "images/crispdm.png", M, 1.95, 6.5, 4.75);
  // justification à droite
  s.addText("POURQUOI CRISP-DM ?", { x: 7.35, y: 2.0, w: 5.4, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.35, 2.34, 5.4, [
    "Méthodologie de référence des projets décisionnels",
    "Ses six phases épousent le déroulement réel du projet",
    "Pratiques agiles conservées : itérations et validations",
    "Scrum ne couvre pas l'analyse et la valorisation des données",
  ], 12);
  card(s, 7.35, 4.62, 5.4, 2.05);
  s.addShape(pptx.ShapeType.rect, { x: 7.35, y: 4.62, w: 5.4, h: 0.08, fill: { color: LITE } });
  s.addText("Correspondance avec le rapport", { x: 7.62, y: 4.82, w: 4.9, h: 0.36,
    fontFace: HF, fontSize: 14, bold: true, color: NAVY, margin: 0, valign: "middle" });
  s.addText("Phases 1–2  →  Chapitres 1 et 2\nPhase 3  →  Chapitre 3 et chaîne ETL\nPhases 4–5  →  Chapitre 4\nPhase 6  →  Chapitre 5",
    { x: 7.62, y: 5.24, w: 4.9, h: 1.3, fontFace: BF, fontSize: 12, color: INK,
      margin: 0, lineSpacing: 18 });
}

/* ======================= PARTIE 02 ======================= */
divider("02", "Spécifications des besoins");

/* -- acteurs -- */
{
  const s = slide("Identification des acteurs");
  const act = [
    ["Administrateur", "ADMIN", "Couvre les 13 cas d'utilisation : rôles et droits · agences, employés, clients · demandes · pointage · journal d'audit · volet décisionnel"],
    ["Directeur commercial", "DIRECTEUR_COMMERCIAL", "Consulte les employés, les objectifs et le tableau de bord · soumet les demandes de création · valide les modifications des employés"],
    ["Utilisateur", "USER", "Pointe son arrivée et son départ · soumet les demandes de modification de ses propres informations · reçoit ses notifications"],
  ];
  act.forEach((a, i) => {
    const x = M + i * 4.13;
    card(s, x, 1.7, 3.83, 4.35);
    s.addShape(pptx.ShapeType.rect, { x, y: 1.7, w: 3.83, h: 0.08, fill: { color: LITE } });
    s.addShape(pptx.ShapeType.ellipse, { x: x + 1.46, y: 2.05, w: 0.9, h: 0.9,
      fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(String(i + 1), { x: x + 1.46, y: 2.05, w: 0.9, h: 0.9, fontFace: HF,
      fontSize: 24, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(a[0], { x: x + 0.22, y: 3.1, w: 3.4, h: 0.4, fontFace: HF, fontSize: 15.5,
      bold: true, color: NAVY, align: "center", margin: 0, valign: "middle" });
    s.addText(a[1], { x: x + 0.22, y: 3.52, w: 3.4, h: 0.32, fontFace: "Consolas",
      fontSize: 10, color: LITE, align: "center", margin: 0, valign: "middle" });
    s.addText(a[2], { x: x + 0.3, y: 3.95, w: 3.25, h: 1.9, fontFace: BF, fontSize: 12,
      color: INK, margin: 0, lineSpacing: 18, valign: "top" });
  });
  s.addText("Les rôles sont gérés par le module de sécurité (table SECURITY_USERS) et conditionnent l'accès à chaque fonctionnalité.",
    { x: M, y: 6.25, w: 12.1, h: 0.4, fontFace: BF, fontSize: 12.5, italic: true,
      color: MUTED, align: "center", margin: 0 });
}

/* -- besoins fonctionnels -- */
{
  const s = slide("Besoins fonctionnels");
  const bf = [
    ["Authentification & rôles", "Connexion sécurisée, gestion des droits d'accès"],
    ["Gestion du référentiel", "CRUD des agences, des employés et des clients"],
    ["Objectifs commerciaux", "Suivi de la production par agence et par période"],
    ["Pointage des employés", "Arrivée / départ, statut présent · retard · absent"],
    ["Circuits de validation", "Double validation : approbation du directeur puis exécution par l'admin"],
    ["Volet décisionnel", "Chaîne ETL, tableaux de bord et segmentation des agences"],
  ];
  bf.forEach((b, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 6.15, y = 1.72 + row * 1.62;
    card(s, x, y, 5.75, 1.35);
    s.addShape(pptx.ShapeType.roundRect, { x: x + 0.26, y: y + 0.36, w: 0.6, h: 0.6,
      rectRadius: 0.1, fill: { color: NAVY } });
    s.addText(String(i + 1), { x: x + 0.26, y: y + 0.36, w: 0.6, h: 0.6, fontFace: HF,
      fontSize: 17, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(b[0], { x: x + 1.05, y: y + 0.24, w: 4.5, h: 0.4, fontFace: HF, fontSize: 14.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(b[1], { x: x + 1.05, y: y + 0.66, w: 4.5, h: 0.44, fontFace: BF, fontSize: 12,
      color: MUTED, margin: 0, valign: "middle" });
  });
}

/* -- besoins non fonctionnels -- */
{
  const s = slide("Besoins non fonctionnels");
  const bnf = [["Sécurité", "Authentification, rôles et workflows de validation"],
               ["Fiabilité", "Intégrité garantie par le SGBD et les transactions"],
               ["Performance", "Temps de réponse adapté aux volumes manipulés"],
               ["Ergonomie", "Interface claire, navigation par menu latéral"],
               ["Maintenabilité", "Architecture en couches, code faiblement couplé"],
               ["Portabilité", "Application Jakarta EE standard, serveur compatible"]];
  bnf.forEach((b, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * 4.13, y = 1.85 + row * 2.35;
    card(s, x, y, 3.83, 2.05);
    s.addShape(pptx.ShapeType.rect, { x, y, w: 3.83, h: 0.08, fill: { color: LITE } });
    s.addText(b[0], { x: x + 0.3, y: y + 0.32, w: 3.25, h: 0.44, fontFace: HF,
      fontSize: 16, bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(b[1], { x: x + 0.3, y: y + 0.86, w: 3.25, h: 1.0, fontFace: BF, fontSize: 12.5,
      color: INK, margin: 0, lineSpacing: 18, valign: "top" });
  });
}

/* ======================= PARTIE 03 ======================= */
divider("03", "Conception & architecture");

/* -- architecture logique -- */
{
  const s = slide("Architecture logique en couches");
  const layers = [["Présentation", "Pages JSP / JSTL et graphiques ApexCharts"],
                  ["Contrôle", "Servlets et filtre de sécurité (NotificationFilter)"],
                  ["Métier", "Services EJB encapsulant les règles de gestion"],
                  ["Persistance", "Entités JPA / Hibernate vers la base Oracle"]];
  layers.forEach((l, i) => {
    const y = 1.72 + i * 1.13;
    card(s, M, y, 7.4, 0.98, i === 0 ? NAVY : CARD);
    s.addShape(pptx.ShapeType.rect, { x: M, y, w: 0.09, h: 0.98, fill: { color: LITE } });
    s.addText(l[0], { x: M + 0.35, y: y + 0.1, w: 2.6, h: 0.4, fontFace: HF, fontSize: 15,
      bold: true, color: i === 0 ? WHITE : NAVY, margin: 0, valign: "middle" });
    s.addText(l[1], { x: M + 0.35, y: y + 0.52, w: 6.7, h: 0.36, fontFace: BF, fontSize: 12,
      color: i === 0 ? "CBD8EE" : MUTED, margin: 0, valign: "middle" });
  });
  fit(s, "diagrams/archi_logique.png", 8.35, 1.72, 4.4, 4.4);
  s.addText("Patron MVC : chaque couche est indépendante et faiblement couplée aux autres.",
    { x: M, y: 6.42, w: 12.1, h: 0.4, fontFace: BF, fontSize: 12.5, italic: true,
      color: MUTED, align: "center", margin: 0 });
}

/* -- architecture physique -- */
{
  const s = slide("Architecture physique (3-tiers)");
  const tiers = [["Poste client", "Navigateur web", NAVY],
                 ["Serveur d'applications", "WildFly · WAR Jakarta EE", MID],
                 ["Serveur de données", "Oracle FREEPDB1", LITE],
                 ["Restitution", "Power BI · Python ETL", NAVY]];
  tiers.forEach((t, i) => {
    const x = M + i * 3.08;
    s.addShape(pptx.ShapeType.roundRect, { x, y: 2.1, w: 2.7, h: 2.2, rectRadius: 0.08,
      fill: { color: t[2] }, line: { color: t[2] } });
    s.addText(t[0], { x: x + 0.15, y: 2.55, w: 2.4, h: 0.75, fontFace: HF, fontSize: 15,
      bold: true, color: WHITE, align: "center", margin: 0, valign: "middle" });
    s.addText(t[1], { x: x + 0.15, y: 3.3, w: 2.4, h: 0.65, fontFace: BF, fontSize: 12,
      color: "D5DEEE", align: "center", margin: 0, valign: "top" });
    if (i < 3) s.addText("→", { x: x + 2.72, y: 3.0, w: 0.36, h: 0.4, fontFace: BF,
      fontSize: 18, bold: true, color: NAVY, align: "center", margin: 0, valign: "middle" });
  });
  card(s, M, 4.75, 12.1, 1.5);
  s.addText("Communication", { x: M + 0.35, y: 4.92, w: 4, h: 0.34, fontFace: HF,
    fontSize: 14, bold: true, color: NAVY, margin: 0, valign: "middle" });
  s.addText("Le client dialogue en HTTP avec WildFly, qui accède à Oracle via la source de données JTA java:/OracleDS. Power BI et la chaîne ETL Python se connectent directement aux vues décisionnelles de la base.",
    { x: M + 0.35, y: 5.3, w: 11.4, h: 0.8, fontFace: BF, fontSize: 12.5, color: INK,
      margin: 0, lineSpacing: 18, valign: "top" });
}

/* -- cas d'utilisation -- */
{
  const s = slide("Diagramme de cas d'utilisation global");
  // le diagramme est au format portrait : encadré à gauche, lecture élargie à droite
  fit(s, "diagrams/uc_global.png", 1.05, 1.28, 5.1, 5.70);
  s.addText("LECTURE DU DIAGRAMME", { x: 7.05, y: 1.86, w: 5.6, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.05, 2.28, 5.6, [
    "Trois acteurs, treize cas d'utilisation",
    "Chaque cas inclut \u00ab S'authentifier \u00bb (include)",
    "Administrateur : les 13 cas, sans exception",
    "Directeur commercial : 5 cas, dont les employ\u00e9s en consultation",
    "Utilisateur : 3 cas \u2014 pointage, demandes, notifications",
  ], 13);
}

/* -- diagramme de classes -- */
{
  const s = slide("Diagramme de classes du modèle métier");
  fit(s, "diagrams/class.png", M, 1.30, 8.5, 5.60);
  s.addText("LECTURE DU DIAGRAMME", { x: 9.35, y: 1.72, w: 3.4, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 9.35, 2.10, 3.4, [
    "13 classes group\u00e9es en 5 paquetages fonctionnels",
    "\u00ab Utilisateur \u00bb au centre du mod\u00e8le",
    "Rattachements par cl\u00e9s \u00e9trang\u00e8res : SK_AGENCE, SK_GESTIONNAIRE",
    "Demandes, pointage, journal, notifications : @ManyToOne vers Utilisateur",
    "DemandeAgence \u2194 Utilisateur : @ManyToMany",
    "Ni h\u00e9ritage ni composition",
  ], 11);
}

/* -- modèle en étoile -- */
{
  const s = slide("Modèle décisionnel en étoile");
  s.addText("TROIS SCHÉMAS COMPARÉS", { x: M, y: 1.62, w: 5.9, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  const comp = [["Étoile", "Simple, lisible, requêtes rapides", true],
                ["Flocon", "Dimensions normalisées, plus de jointures", false],
                ["Constellation", "Plusieurs tables de faits, surdimensionné ici", false]];
  comp.forEach((c, i) => {
    const y = 1.98 + i * 1.06;
    card(s, M, y, 5.9, 0.92, c[2] ? NAVY : CARD);
    s.addText(c[0], { x: M + 0.3, y: y + 0.08, w: 2.4, h: 0.36, fontFace: HF, fontSize: 14.5,
      bold: true, color: c[2] ? WHITE : NAVY, margin: 0, valign: "middle" });
    s.addText(c[1], { x: M + 0.3, y: y + 0.46, w: 5.3, h: 0.36, fontFace: BF, fontSize: 11.5,
      color: c[2] ? "CBD8EE" : MUTED, margin: 0, valign: "middle" });
  });
  s.addText("Des grains homogènes — l'agence, puis le couple agence × gestionnaire — et peu de dimensions : l'étoile offre la lisibilité attendue par un outil libre-service comme Power BI.",
    { x: M, y: 5.2, w: 5.9, h: 0.9, fontFace: BF, fontSize: 12.5, color: INK, margin: 0,
      lineSpacing: 18, valign: "top" });
  card(s, 7.15, 1.98, 5.6, 4.2);
  s.addText("DATAMART CHARGÉ PAR L'ETL", { x: 7.45, y: 2.16, w: 5.1, h: 0.28, fontFace: BF,
    fontSize: 10, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.45, 2.46, 5.1, [
    "fait_agence / dim_agence — 7 indicateurs au grain de l'agence",
    "fait_objectif / dim_gestionnaire — production au grain agence × gestionnaire",
  ], 11.5);
  s.addText("COUCHE SÉMANTIQUE POWER BI", { x: 7.45, y: 4.06, w: 5.1, h: 0.28, fontFace: BF,
    fontSize: 10, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.45, 4.36, 5.1, [
    "4 vues V_BI_* : production, effectifs, clients, présence",
    "Dimensions conformes AGENCE (SK_AGENCE) et B_UTILISATEURS (SK_UTILISATEUR)",
    "Période et type de client : dimensions dégénérées portées par les vues",
  ], 11.5);
}

/* ======================= PARTIE 04 ======================= */
divider("04", "Volet décisionnel & réalisation");

/* -- chaîne ETL -- */
{
  const s = slide("Chaîne ETL en Python : cinq étapes");
  const steps = [["Collecte", "Lecture des 5 tables sources Oracle"],
                 ["Nettoyage", "Lignes incomplètes écartées, typage des colonnes"],
                 ["Transformation", "Agrégation par agence des 7 indicateurs"],
                 ["Intégration", "Fusion sur SK_AGENCE, puis regroupement sur SK_UTILISATEUR"],
                 ["Contrôle qualité", "Valeurs manquantes, arrondis et journal"]];
  steps.forEach((st, i) => {
    const x = M + i * 2.44;
    card(s, x, 1.72, 2.26, 2.15);
    s.addShape(pptx.ShapeType.rect, { x, y: 1.72, w: 2.26, h: 0.08, fill: { color: LITE } });
    s.addText("0" + (i + 1), { x: x + 0.2, y: 1.94, w: 1.9, h: 0.4, fontFace: HF,
      fontSize: 17, bold: true, color: NUMB, margin: 0, valign: "middle" });
    s.addText(st[0], { x: x + 0.2, y: 2.36, w: 1.9, h: 0.36, fontFace: HF, fontSize: 13.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(st[1], { x: x + 0.2, y: 2.76, w: 1.9, h: 0.98, fontFace: BF, fontSize: 11,
      color: MUTED, margin: 0, lineSpacing: 14, valign: "top" });
    if (i < 4) s.addText("→", { x: x + 2.28, y: 2.6, w: 0.16, h: 0.4, fontFace: BF,
      fontSize: 15, bold: true, color: LITE, align: "center", margin: 0, valign: "middle" });
  });
  card(s, M, 4.15, 5.9, 2.15, NAVY);
  s.addText("Sources Oracle", { x: M + 0.35, y: 4.35, w: 5.2, h: 0.36, fontFace: HF,
    fontSize: 14.5, bold: true, color: WHITE, margin: 0, valign: "middle" });
  s.addText("AGENCE · B_UTILISATEURS · CLIENT_BTK\nB_OBJECTIF · POINTAGE",
    { x: M + 0.35, y: 4.76, w: 5.2, h: 0.8, fontFace: "Consolas", fontSize: 11.5,
      color: "CBD8EE", margin: 0, lineSpacing: 18, valign: "top" });
  s.addText("Chaîne rejouable, exécutée sur les données réelles du réseau.",
    { x: M + 0.35, y: 5.62, w: 5.2, h: 0.4, fontFace: BF, fontSize: 11.5, color: LITE,
      italic: true, margin: 0, valign: "middle" });
  stat(s, 7.15, 4.15, 2.7, 2.15, "49", "entités consolidées");
  stat(s, 10.05, 4.15, 2.7, 2.15, "7", "indicateurs par agence");
}

/* -- datamart réel -- */
{
  const s = slide("Datamart obtenu sur les données réelles");
  fit(s, "images/etl/etl_cell2.png", M, 1.55, 12.1, 3.5);
  card(s, M, 5.28, 12.1, 1.42);
  s.addText("Lecture", { x: M + 0.35, y: 5.44, w: 3, h: 0.34, fontFace: HF, fontSize: 14,
    bold: true, color: NAVY, margin: 0, valign: "middle" });
  s.addText("Le datamart décrit chaque agence par ses sept indicateurs. BIZERTE et MGHIRA dominent le portefeuille clients, tandis que CENTRALE concentre la production de crédits — une hétérogénéité que la segmentation exploitera.",
    { x: M + 0.35, y: 5.8, w: 11.4, h: 0.78, fontFace: BF, fontSize: 12.5, color: INK,
      margin: 0, lineSpacing: 18, valign: "top" });
}

/* -- intégration Power BI -- */
{
  const s = slide("Intégration du modèle dans Power BI");
  fit(s, "images/etl/pbi_modele.png", M, 1.5, 6.4, 5.2);
  s.addText("RELATIONS DU MODÈLE", { x: 7.35, y: 1.68, w: 5.4, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  const rels = [["AGENCE → B_UTILISATEURS", "SK_AGENCE"],
                ["AGENCE → B_CLIENTS", "SK_AGENCE"],
                ["AGENCE → B_OBJECTIF", "SK_AGENCE"],
                ["B_UTILISATEURS → POINTAGE", "SK_UTILISATEUR"]];
  rels.forEach((r, i) => {
    const y = 2.05 + i * 0.82;
    card(s, 7.35, y, 5.4, 0.7);
    s.addText(r[0], { x: 7.6, y: y + 0.04, w: 4.2, h: 0.34, fontFace: "Consolas",
      fontSize: 10.5, color: NAVY, margin: 0, valign: "middle" });
    s.addText(r[1], { x: 7.6, y: y + 0.36, w: 4.2, h: 0.3, fontFace: BF, fontSize: 10,
      color: MUTED, margin: 0, valign: "middle" });
    s.addText("1 — ∗", { x: 11.85, y, w: 0.75, h: 0.7, fontFace: BF, fontSize: 12,
      bold: true, color: LITE, align: "center", margin: 0, valign: "middle" });
  });
  card(s, 7.35, 5.42, 5.4, 1.28, NAVY);
  s.addText("Filtrage croisé", { x: 7.6, y: 5.56, w: 4.9, h: 0.32, fontFace: HF,
    fontSize: 14, bold: true, color: WHITE, margin: 0, valign: "middle" });
  s.addText("Les relations un-à-plusieurs propagent le filtre de la dimension vers les faits : un clic recalcule tous les visuels.",
    { x: 7.6, y: 5.9, w: 4.9, h: 0.7, fontFace: BF, fontSize: 11.5, color: "CBD8EE",
      margin: 0, lineSpacing: 16, valign: "top" });
}

/* -- 4 tableaux de bord -- */
const dash = [
  { t: "Tableau de bord — Résumé du réseau", im: "images/screens/pbi_resume.png",
    stats: [["30 K", "clients"], ["1,40 Md", "crédits"], ["87,9 %", "présence"]],
    ins: ["Vue consolidée des indicateurs clés du réseau",
          "Un pointage sur trois est un retard ou une absence",
          "Pic de production en février, puis tassement"] },
  { t: "Tableau de bord — Clients", im: "images/screens/pbi_clients.png",
    stats: [["88 %", "particuliers"], ["24", "gouvernorats"], ["63 %", "hommes"]],
    ins: ["Portefeuille très majoritairement « particuliers »",
          "Forte concentration sur le Grand Tunis",
          "Marge de développement sur la clientèle professionnelle"] },
  { t: "Tableau de bord — Performance commerciale", im: "images/screens/pbi_commercial.png",
    stats: [["1,40 Md", "crédits"], ["105 K", "comptes"], ["83,6 %", "EER particuliers"]],
    ins: ["Production équilibrée : immobilier, conso, investissement",
          "Les comptes chèques dominent les ouvertures",
          "CENTRALE : agence phare, bonnes pratiques à diffuser"] },
  { t: "Tableau de bord — Présence & assiduité", im: "images/screens/pbi_presence.png",
    stats: [["87,9 %", "taux de présence"], ["25 %", "retards"], ["72 %", "pointage auto"]],
    ins: ["Bonne adoption du pointage automatique",
          "Pic d'assiduité en avril–mai, repli estival",
          "Agences à surveiller identifiées pour action RH"] },
];
dash.forEach((d) => {
  const s = slide(d.t);
  fit(s, d.im, M, 1.5, 7.75, 4.35);
  d.stats.forEach((st, i) => stat(s, 8.62, 1.5 + i * 1.52, 4.13, 1.36, st[0], st[1]));
  card(s, M, 6.08, 12.1, 0.86);
  d.ins.forEach((t, i) => {
    const x = M + 0.3 + i * 3.95;
    s.addShape(pptx.ShapeType.ellipse, { x, y: 6.42, w: 0.11, h: 0.11,
      fill: { color: LITE }, line: { color: LITE } });
    s.addText(t, { x: x + 0.22, y: 6.14, w: 3.55, h: 0.74, fontFace: BF, fontSize: 11,
      color: INK, margin: 0, valign: "middle", lineSpacing: 15 });
  });
});

/* -- environnement technique -- */
{
  const s = slide("Environnement technique");
  const logos = [["logos/java.png", "Java 21"], ["logos/jakartaee.png", "Jakarta EE 10"],
                 ["logos/hibernate.png", "Hibernate"], ["logos/oracle.png", "Oracle"],
                 ["logos/wildfly.png", "WildFly"], ["logos/maven.png", "Maven"],
                 ["logos/powerbi.png", "Power BI"], ["logos/python.png", "Python"]];
  logos.forEach((l, i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = M + col * 1.62, y = 1.75 + row * 1.62;
    card(s, x, y, 1.48, 1.44);
    fit(s, "images/" + l[0], x + 0.34, y + 0.18, 0.8, 0.64);
    s.addText(l[1], { x: x + 0.05, y: y + 0.92, w: 1.38, h: 0.38, fontFace: BF,
      fontSize: 10.5, color: NAVY, align: "center", margin: 0, valign: "middle" });
  });
  s.addText("PILE APPLICATIVE", { x: 7.05, y: 1.78, w: 5.7, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.05, 2.14, 5.7, [
    "Java 21 et Jakarta EE 10, empaquet\u00e9s par Maven",
    "Hibernate pour la persistance, base Oracle",
    "D\u00e9ploiement sur WildFly, racine /gestion-agences",
  ], 12.5);
  s.addText("VOLET D\u00c9CISIONNEL", { x: 7.05, y: 3.94, w: 5.7, h: 0.3, fontFace: BF,
    fontSize: 10.5, bold: true, color: LITE, charSpacing: 2, margin: 0 });
  bullets(s, 7.05, 4.30, 5.7, [
    "Cha\u00eene ETL en Python (pandas)",
    "Segmentation avec scikit-learn",
    "Restitution Power BI sur les vues V_BI_*",
  ], 12.5);
  card(s, M, 5.36, 6.2, 0.98, NAVY);
  s.addText("10 sc\u00e9narios de tests fonctionnels \u2014 tous conformes", { x: M, y: 5.36,
    w: 6.2, h: 0.98, fontFace: BF, fontSize: 12.5, color: WHITE, align: "center",
    margin: 0, valign: "middle" });
}

/* ======================= PARTIE 05 ======================= */
divider("05", "Intelligence artificielle & démonstration");

/* -- zoom technique clustering -- */
{
  const s = slide("Zoom technique — segmentation par K-Means");
  s.addText("Principe : regrouper les agences en profils homogènes à partir de six indicateurs réels, sans étiquette préalable (apprentissage non supervisé).",
    { x: M, y: 1.55, w: 12.1, h: 0.5, fontFace: BF, fontSize: 13, color: INK, margin: 0 });
  const st = [["1", "Prétraitement", "Log sur les montants puis centrage-réduction (6 variables)"],
              ["2", "Choix de k", "Coude et silhouette → k = 3, exploitable pour le pilotage"],
              ["3", "Comparaison", "K-Means, hiérarchique, GMM et DBSCAN"],
              ["4", "Modèle retenu", "K-Means : meilleure silhouette (0,604) et cohésion (95,2)"]];
  st.forEach((c, i) => {
    const y = 2.2 + i * 1.12;
    card(s, M, y, 6.1, 0.98);
    s.addShape(pptx.ShapeType.roundRect, { x: M + 0.24, y: y + 0.2, w: 0.58, h: 0.58,
      rectRadius: 0.1, fill: { color: NAVY } });
    s.addText(c[0], { x: M + 0.24, y: y + 0.2, w: 0.58, h: 0.58, fontFace: HF, fontSize: 17,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(c[1], { x: M + 1.02, y: y + 0.08, w: 4.9, h: 0.38, fontFace: HF, fontSize: 14,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(c[2], { x: M + 1.02, y: y + 0.48, w: 4.9, h: 0.38, fontFace: BF, fontSize: 11.5,
      color: MUTED, margin: 0, valign: "middle" });
  });
  fit(s, "images/clustering_pca.png", 7.05, 2.2, 5.7, 4.4);
}

/* -- résultats segmentation -- */
{
  const s = slide("Résultats de la segmentation");
  const seg = [["34", "Agences d'exploitation", "880 clients · 12 employés · 7,80 MDT de crédits",
                "Objectifs différenciés, diffusion des bonnes pratiques"],
               ["6", "Entités de production", "Quasi aucun client · 14,61 MDT de crédits",
                "Analyser ces financements réalisés hors guichet"],
               ["8", "Entités sans activité", "Ni clientèle, ni comptes, ni production",
                "Statuer : ouverture, rattachement ou intégration"]];
  seg.forEach((g, i) => {
    const x = M + i * 4.13;
    card(s, x, 1.7, 3.83, 4.0);
    s.addShape(pptx.ShapeType.rect, { x, y: 1.7, w: 3.83, h: 0.08, fill: { color: LITE } });
    s.addText(g[0], { x: x + 0.3, y: 1.95, w: 3.25, h: 0.75, fontFace: HF, fontSize: 34,
      bold: true, color: NUMB, margin: 0, valign: "middle" });
    s.addText(g[1], { x: x + 0.3, y: 2.72, w: 3.25, h: 0.4, fontFace: HF, fontSize: 15.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(g[2], { x: x + 0.3, y: 3.16, w: 3.25, h: 0.66, fontFace: BF, fontSize: 11.5,
      color: MUTED, margin: 0, lineSpacing: 16, valign: "top" });
    s.addShape(pptx.ShapeType.rect, { x: x + 0.3, y: 3.92, w: 1.0, h: 0.025, fill: { color: EDGE } });
    s.addText(g[3], { x: x + 0.3, y: 4.1, w: 3.25, h: 1.3, fontFace: BF, fontSize: 12,
      color: INK, margin: 0, lineSpacing: 18, valign: "top" });
  });
  card(s, M, 5.92, 12.1, 0.82, NAVY);
  s.addText("Apport décisionnel : différencier les objectifs selon le régime d'activité réel et fiabiliser le référentiel",
    { x: M, y: 5.92, w: 12.1, h: 0.82, fontFace: BF, fontSize: 12.5, color: WHITE,
      align: "center", margin: 0, valign: "middle" });
}

/* -- démonstration -- */
{
  const s = navySlide();
  s.addText("DÉMONSTRATION", { x: M, y: 1.28, w: 9, h: 0.34,
    fontFace: BF, fontSize: 12, bold: true, color: LITE, charSpacing: 3, margin: 0 });
  s.addText("Parcours de démonstration \u2014 les trois rôles", { x: M, y: 1.66, w: 11.5, h: 0.7,
    fontFace: HF, fontSize: 30, bold: true, color: WHITE, margin: 0, valign: "middle" });
  s.addShape(pptx.ShapeType.rect, { x: M, y: 2.44, w: 1.35, h: 0.03, fill: { color: LITE } });
  s.addText("Le même circuit est suivi de bout en bout : on se connecte, on agit, et l'on voit la trace de l'action.",
    { x: M, y: 2.66, w: 11.5, h: 0.36, fontFace: BF, fontSize: 13, color: "CBD8EE", margin: 0 });
  const etapes = [
    ["1", "Connexion", "ADMIN", "Identifiants v\u00e9rifi\u00e9s, r\u00f4le charg\u00e9 en session"],
    ["2", "Tableau de bord", "ADMIN", "Indicateurs, graphiques et actions requises"],
    ["3", "Employ\u00e9s", "ADMIN", "Ajout d'un employ\u00e9, filtre et liste"],
    ["4", "Agences", "ADMIN", "Cr\u00e9ation et suppression d'une agence"],
    ["5", "Pointage", "USER", "Arriv\u00e9e, d\u00e9part et statut calcul\u00e9"],
    ["6", "Validation", "DIRECTEUR", "Approbation d'une demande de modification"],
  ];
  etapes.forEach((e, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * 4.03, y = 3.24 + row * 1.72;
    s.addShape(pptx.ShapeType.roundRect, { x, y, w: 3.83, h: 1.52,
      rectRadius: 0.08, fill: { color: MID }, line: { color: MID } });
    s.addShape(pptx.ShapeType.ellipse, { x: x + 0.2, y: y + 0.2, w: 0.42, h: 0.42,
      fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(e[0], { x: x + 0.2, y: y + 0.2, w: 0.42, h: 0.42, fontFace: HF,
      fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(e[1], { x: x + 0.72, y: y + 0.18, w: 2.0, h: 0.34, fontFace: HF,
      fontSize: 14, bold: true, color: WHITE, margin: 0, valign: "middle" });
    s.addText(e[2], { x: x + 2.72, y: y + 0.2, w: 0.95, h: 0.3, fontFace: BF,
      fontSize: 8.5, bold: true, color: NAVY, align: "center", margin: 0, valign: "middle",
      fill: { color: LITE }, rectRadius: 0.04 });
    s.addText(e[3], { x: x + 0.2, y: y + 0.68, w: 3.45, h: 0.7, fontFace: BF,
      fontSize: 10.5, color: "CBD8EE", margin: 0, valign: "top", lineSpacing: 13 });
  });
  s.addText("Les quatre pages Power BI ont \u00e9t\u00e9 pr\u00e9sent\u00e9es dans la partie pr\u00e9c\u00e9dente.",
    { x: M, y: 6.72, w: 11.5, h: 0.32, fontFace: BF, fontSize: 11.5, italic: true,
      color: "9FB6DC", margin: 0 });
}

/* -- captures de la démonstration : une par écran -- */
{
  const ecrans = [
    ["Authentification de l'administrateur", "../presentation/captures/01-auth-admin.png",
     "L'identifiant et le mot de passe sont v\u00e9rifi\u00e9s dans SECURITY_USERS ; le r\u00f4le est charg\u00e9 en session et conditionne tout l'acc\u00e8s."],
    ["Ajout d'un employ\u00e9", "../presentation/captures/02-ajout-employe.png",
     "L'administrateur cr\u00e9e l'employ\u00e9 et son compte de connexion, le rattache \u00e0 son agence, et l'action est inscrite au journal d'audit."],
    ["Pointage de l'utilisateur", "../presentation/captures/03-pointage-utilisateur.png",
     "L'employ\u00e9 pointe son arriv\u00e9e et son d\u00e9part ; le statut est calcul\u00e9 par le serveur \u2014 au-del\u00e0 de 9 h, c'est un retard."],
    ["La demande arrive chez le directeur", "../presentation/captures/04-demande-directeur.png",
     "La demande de modification passe en attente ; le directeur approuve ou refuse, mais la donn\u00e9e n'est modifi\u00e9e qu'apr\u00e8s ex\u00e9cution par l'administrateur."],
    ["Assistant int\u00e9gr\u00e9", "../presentation/captures/05-assistant.png",
     "Un assistant conversationnel r\u00e9pond aux questions sur les donn\u00e9es de l'application, \u00e0 partir des m\u00eames indicateurs que le tableau de bord."],
  ];
  ecrans.forEach((e) => {
    const s = slide(e[0]);
    fit(s, e[1], M, 1.30, 12.1, 4.85);
    s.addShape(pptx.ShapeType.rect, { x: M, y: 6.32, w: 0.055, h: 0.44, fill: { color: LITE } });
    s.addText(e[2], { x: M + 0.22, y: 6.30, w: 11.9, h: 0.48, fontFace: BF,
      fontSize: 12.5, color: INK, margin: 0, valign: "middle", lineSpacing: 16 });
  });
}

/* ======================= PARTIE 06 ======================= */
divider("06", "Conclusion & perspectives");

/* -- conclusion -- */
{
  const s = slide("Conclusion");
  const done = [["Application web", "Gestion centralisée du réseau : agences, employés, clients, objectifs, rôles, pointage et circuits de validation"],
                ["Chaîne décisionnelle", "ETL Python, datamart en étoile et quatre tableaux de bord Power BI sur les données réelles"],
                ["Intelligence artificielle", "Segmentation du réseau en trois profils d'agences directement exploitables"]];
  done.forEach((d, i) => {
    const y = 1.75 + i * 1.42;
    card(s, M, y, 12.1, 1.22);
    s.addShape(pptx.ShapeType.roundRect, { x: M + 0.3, y: y + 0.32, w: 0.58, h: 0.58,
      rectRadius: 0.1, fill: { color: NAVY } });
    s.addText("✓", { x: M + 0.3, y: y + 0.32, w: 0.58, h: 0.58, fontFace: BF, fontSize: 17,
      bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    s.addText(d[0], { x: M + 1.12, y: y + 0.16, w: 10.6, h: 0.42, fontFace: HF,
      fontSize: 15.5, bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(d[1], { x: M + 1.12, y: y + 0.6, w: 10.6, h: 0.46, fontFace: BF,
      fontSize: 12.5, color: INK, margin: 0, valign: "middle" });
  });
  card(s, M, 6.02, 12.1, 0.8, NAVY);
  s.addText("Un système complet, de la donnée opérationnelle jusqu'à la décision",
    { x: M, y: 6.02, w: 12.1, h: 0.8, fontFace: HF, fontSize: 15, bold: true,
      color: WHITE, align: "center", margin: 0, valign: "middle" });
}

/* -- perspectives -- */
{
  const s = slide("Perspectives");
  const per = [["Sécurité renforcée", "Hachage des mots de passe et durcissement des accès"],
               ["Industrialisation de l'ETL", "Ordonnancement automatique et historisation incrémentale"],
               ["Analyses prédictives", "Prévision des objectifs commerciaux par agence"],
               ["API REST", "Interopérabilité avec les autres systèmes de la banque"],
               ["Application mobile", "Consultation des indicateurs en mobilité"],
               ["Alertes automatiques", "Notification des agences sous les seuils critiques"]];
  per.forEach((p, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 6.15, y = 1.75 + row * 1.6;
    card(s, x, y, 5.75, 1.34);
    s.addShape(pptx.ShapeType.rect, { x, y, w: 0.08, h: 1.34, fill: { color: LITE } });
    s.addText(p[0], { x: x + 0.35, y: y + 0.2, w: 5.2, h: 0.4, fontFace: HF, fontSize: 14.5,
      bold: true, color: NAVY, margin: 0, valign: "middle" });
    s.addText(p[1], { x: x + 0.35, y: y + 0.62, w: 5.2, h: 0.5, fontFace: BF, fontSize: 12,
      color: MUTED, margin: 0, lineSpacing: 16, valign: "top" });
  });
}

/* -- merci -- */
{
  const s = navySlide();
  for (let i = 0; i < 6; i++)
    s.addShape(pptx.ShapeType.rect, { x: 10.55 + i * 0.42, y: 0, w: 0.015, h: H,
      fill: { color: LITE } });
  s.addText("MERCI POUR VOTRE ATTENTION", { x: M, y: 2.9, w: 9.6, h: 0.9,
    fontFace: HF, fontSize: 27, bold: true, color: WHITE, charSpacing: 2, margin: 0, valign: "middle" });
  s.addShape(pptx.ShapeType.rect, { x: M, y: 4.0, w: 1.35, h: 0.03, fill: { color: LITE } });
  s.addText("Questions & discussion", { x: M, y: 4.3, w: 8, h: 0.44, fontFace: BF,
    fontSize: 17, color: "CBD8EE", margin: 0 });
  s.addImage({ path: img("images/logo_esb.png"), x: M, y: 5.5, w: 1.55, h: 0.94 });
  s.addImage({ path: img("images/logo_btk.png"), x: 2.55, y: 5.5, w: 0.85, h: 0.89 });
}

const out = "/home/user/oussema_korbosli/presentation/Soutenance_PFE_Oussema_Korbosli.pptx";
pptx.writeFile({ fileName: out }).then(() => console.log("OK ->", out, "|", pageNo, "slides"));
