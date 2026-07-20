-- =====================================================================
--  Enrichir BTK_BI.B_OBJECTIF avec plusieurs mois d'objectifs (démo BI)
--  Objectif : remplir la page « Performance commerciale » — histogramme
--  d'évolution mensuelle, objectifs par agence, KPI comptes/crédits/épargne.
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
-- =====================================================================

-- ---------------------------------------------------------------------
-- ÉTAPE 0 — DIAGNOSTIC (lance ça d'abord, regarde le résultat)
-- ---------------------------------------------------------------------
SELECT COUNT(*)                    AS nb_lignes,
       COUNT(DISTINCT ANNEE_MOIS)  AS nb_periodes,
       COUNT(DISTINCT SK_AGENCE)   AS nb_agences
FROM   BTK_BI.B_OBJECTIF;

-- >>> IMPORTANT : note le FORMAT exact de ANNEE_MOIS ci-dessous <<<
SELECT ANNEE_MOIS, COUNT(*) AS nb
FROM   BTK_BI.B_OBJECTIF
GROUP  BY ANNEE_MOIS
ORDER  BY ANNEE_MOIS;

-- ---------------------------------------------------------------------
-- ÉTAPE 1 — SEED : 6 mois × toutes les agences
--   ⚠️ Adapte la liste v_months au FORMAT vu à l'étape 0 !
-- ---------------------------------------------------------------------
SET SERVEROUTPUT ON;

DECLARE
  v_base NUMBER;
  v_n    NUMBER := 0;
  v_g    NUMBER;          -- facteur de croissance mois après mois
  v_am   VARCHAR2(20);
  TYPE t_m IS TABLE OF VARCHAR2(20);
  -- Format réel du projet : texte « J/M/AAAA », 1er du mois (ex. 1/1/2026 = janvier)
  v_months t_m := t_m('1/1/2026','1/2/2026','1/3/2026','1/4/2026','1/5/2026','1/6/2026');
BEGIN
  SELECT NVL(MAX(ID_OBJECTIF), 0) INTO v_base FROM BTK_BI.B_OBJECTIF;

  FOR m IN 1 .. v_months.COUNT LOOP
    v_am := v_months(m);
    v_g  := 0.80 + 0.06 * m;             -- progression douce (mois 1 -> 0.86 … mois 6 -> 1.16)

    FOR ag IN (SELECT SK_AGENCE FROM BTK_BI.AGENCE) LOOP
      v_n := v_n + 1;
      INSERT INTO BTK_BI.B_OBJECTIF (
        ID_OBJECTIF, SITUATION_ADMINISTRATIVE,
        EER_PARTICULIER_OA, EER_HORS_PARTICULIER_OA,
        SOUSCRIPTION_COMPTE_CHEQUES_OA, SOUSCRIPTION_COMPTE_EPARGNES_OA, SOUSCRIPTION_COMPTE_COURANTS_OA,
        SOUSCRIPTION_PACKS_PARTICULIER_OA, SOUSCRIPTION_PACKS_PRO_OA, SOUSCRIPTION_CARTES_UNITE_OA,
        DAV_PP_ADD_OA, DAV_PM_ADD_OA, EPARGNE_ADD_OA,
        PRODUCTION_CREDITS_CONSO_OA, PRODUCTION_CREDITS_IMMO_OA, PRODUCTION_CREDITS_INVESTISSEMENT_OA,
        EVOL_ENCOURS_ESCOMPTE_OA, EVOL_ENCOURS_CREDITS_GESTION_OA, EVOL_ENCOURS_ENGAGEMENTS_PAR_SIGNATURE_OA,
        ANNEE_MOIS, SK_AGENCE, SK_GESTIONNAIRE, SK_UTILISATEUR
      ) VALUES (
        v_base + v_n, 'DEMO BI',
        ROUND(DBMS_RANDOM.VALUE(0.45, 0.90), 2), ROUND(DBMS_RANDOM.VALUE(0.20, 0.60), 2),
        TRUNC(DBMS_RANDOM.VALUE(50, 200) * v_g), TRUNC(DBMS_RANDOM.VALUE(30, 150) * v_g), TRUNC(DBMS_RANDOM.VALUE(20, 120) * v_g),
        TRUNC(DBMS_RANDOM.VALUE(10, 80) * v_g),  TRUNC(DBMS_RANDOM.VALUE(5, 40) * v_g),  TRUNC(DBMS_RANDOM.VALUE(40, 250) * v_g),
        ROUND(DBMS_RANDOM.VALUE(50000, 500000), 0), ROUND(DBMS_RANDOM.VALUE(50000, 500000), 0), ROUND(DBMS_RANDOM.VALUE(100000, 1500000) * v_g, 0),
        ROUND(DBMS_RANDOM.VALUE(200000, 2000000) * v_g, 0), ROUND(DBMS_RANDOM.VALUE(300000, 3000000) * v_g, 0), ROUND(DBMS_RANDOM.VALUE(100000, 1500000) * v_g, 0),
        ROUND(DBMS_RANDOM.VALUE(0, 500000), 0), ROUND(DBMS_RANDOM.VALUE(0, 800000), 0), ROUND(DBMS_RANDOM.VALUE(0, 600000), 0),
        v_am, ag.SK_AGENCE, NULL, NULL
      );
    END LOOP;
  END LOOP;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('OK : ' || v_n || ' objectifs insérés dans BTK_BI.B_OBJECTIF.');
END;
/

-- ---------------------------------------------------------------------
-- ÉTAPE 2 — VÉRIFICATION (doit montrer une production qui monte par mois)
-- ---------------------------------------------------------------------
SELECT ANNEE_MOIS,
       ROUND(SUM(PRODUCTION_CREDITS_CONSO_OA
               + PRODUCTION_CREDITS_IMMO_OA
               + PRODUCTION_CREDITS_INVESTISSEMENT_OA)) AS total_credits
FROM   BTK_BI.B_OBJECTIF
GROUP  BY ANNEE_MOIS
ORDER  BY ANNEE_MOIS;

-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser
--  -> l'histogramme « Évolution de la production » montre 6 barres qui montent.
--
--  Pour tout annuler :
--  DELETE FROM BTK_BI.B_OBJECTIF WHERE SITUATION_ADMINISTRATIVE = 'DEMO BI'; COMMIT;
-- =====================================================================
