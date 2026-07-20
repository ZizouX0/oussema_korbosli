-- =====================================================================
--  Traiter les LIGNES VIDES (valeurs NULL) de BTK_BI.B_OBJECTIF
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
-- =====================================================================

-- ---------------------------------------------------------------------
-- ÉTAPE 0 — VOIR les lignes vides (lance d'abord)
--   Montre l'ID, la période, l'agence et 3 métriques : tu verras si
--   la ligne est totalement vide (à supprimer) ou juste ses chiffres
--   qui manquent (à remplir).
-- ---------------------------------------------------------------------
SELECT ID_OBJECTIF, ANNEE_MOIS, SK_AGENCE,
       SOUSCRIPTION_COMPTE_CHEQUES_OA AS chq,
       PRODUCTION_CREDITS_CONSO_OA    AS credit_conso,
       EPARGNE_ADD_OA                 AS epargne
FROM   BTK_BI.B_OBJECTIF
WHERE  SOUSCRIPTION_COMPTE_CHEQUES_OA IS NULL
   OR  PRODUCTION_CREDITS_CONSO_OA    IS NULL
   OR  EPARGNE_ADD_OA                 IS NULL;


-- =====================================================================
--  OPTION A — SUPPRIMER les lignes totalement vides  (recommandé si la
--             ligne n'a ni chiffres, elle ne sert à rien et crée un
--             « (vide) » dans le dashboard)
-- =====================================================================
DELETE FROM BTK_BI.B_OBJECTIF
WHERE  SOUSCRIPTION_COMPTE_CHEQUES_OA        IS NULL
  AND  SOUSCRIPTION_COMPTE_EPARGNES_OA       IS NULL
  AND  SOUSCRIPTION_COMPTE_COURANTS_OA       IS NULL
  AND  PRODUCTION_CREDITS_CONSO_OA           IS NULL
  AND  PRODUCTION_CREDITS_IMMO_OA            IS NULL
  AND  PRODUCTION_CREDITS_INVESTISSEMENT_OA  IS NULL
  AND  EPARGNE_ADD_OA                        IS NULL;
COMMIT;


-- =====================================================================
--  OPTION B — REMPLIR les cases vides avec des valeurs représentatives
--             (garde la ligne ; NVL ne touche QUE les cases NULL,
--              jamais tes vraies valeurs existantes)
-- =====================================================================
UPDATE BTK_BI.B_OBJECTIF SET
  -- EER = objectifs chiffrés (entiers, cf. EER_PARTICULIER ~40-110 dans les données)
  EER_PARTICULIER_OA                        = NVL(EER_PARTICULIER_OA,                        TRUNC(DBMS_RANDOM.VALUE(30,110))),
  EER_HORS_PARTICULIER_OA                   = NVL(EER_HORS_PARTICULIER_OA,                   TRUNC(DBMS_RANDOM.VALUE(15,80))),
  SOUSCRIPTION_COMPTE_CHEQUES_OA            = NVL(SOUSCRIPTION_COMPTE_CHEQUES_OA,            TRUNC(DBMS_RANDOM.VALUE(50,200))),
  SOUSCRIPTION_COMPTE_EPARGNES_OA           = NVL(SOUSCRIPTION_COMPTE_EPARGNES_OA,           TRUNC(DBMS_RANDOM.VALUE(30,150))),
  SOUSCRIPTION_COMPTE_COURANTS_OA           = NVL(SOUSCRIPTION_COMPTE_COURANTS_OA,           TRUNC(DBMS_RANDOM.VALUE(20,120))),
  SOUSCRIPTION_PACKS_PARTICULIER_OA         = NVL(SOUSCRIPTION_PACKS_PARTICULIER_OA,         TRUNC(DBMS_RANDOM.VALUE(10,80))),
  SOUSCRIPTION_PACKS_PRO_OA                 = NVL(SOUSCRIPTION_PACKS_PRO_OA,                 TRUNC(DBMS_RANDOM.VALUE(5,40))),
  SOUSCRIPTION_CARTES_UNITE_OA              = NVL(SOUSCRIPTION_CARTES_UNITE_OA,              TRUNC(DBMS_RANDOM.VALUE(40,250))),
  DAV_PP_ADD_OA                             = NVL(DAV_PP_ADD_OA,                             ROUND(DBMS_RANDOM.VALUE(50000,500000),0)),
  DAV_PM_ADD_OA                             = NVL(DAV_PM_ADD_OA,                             ROUND(DBMS_RANDOM.VALUE(50000,500000),0)),
  EPARGNE_ADD_OA                            = NVL(EPARGNE_ADD_OA,                            ROUND(DBMS_RANDOM.VALUE(100000,1500000),0)),
  PRODUCTION_CREDITS_CONSO_OA               = NVL(PRODUCTION_CREDITS_CONSO_OA,               ROUND(DBMS_RANDOM.VALUE(200000,2000000),0)),
  PRODUCTION_CREDITS_IMMO_OA                = NVL(PRODUCTION_CREDITS_IMMO_OA,                ROUND(DBMS_RANDOM.VALUE(300000,3000000),0)),
  PRODUCTION_CREDITS_INVESTISSEMENT_OA      = NVL(PRODUCTION_CREDITS_INVESTISSEMENT_OA,      ROUND(DBMS_RANDOM.VALUE(100000,1500000),0)),
  EVOL_ENCOURS_ESCOMPTE_OA                  = NVL(EVOL_ENCOURS_ESCOMPTE_OA,                  ROUND(DBMS_RANDOM.VALUE(0,500000),0)),
  EVOL_ENCOURS_CREDITS_GESTION_OA           = NVL(EVOL_ENCOURS_CREDITS_GESTION_OA,           ROUND(DBMS_RANDOM.VALUE(0,800000),0)),
  EVOL_ENCOURS_ENGAGEMENTS_PAR_SIGNATURE_OA = NVL(EVOL_ENCOURS_ENGAGEMENTS_PAR_SIGNATURE_OA, ROUND(DBMS_RANDOM.VALUE(0,600000),0))
WHERE  SOUSCRIPTION_COMPTE_CHEQUES_OA IS NULL
   OR  PRODUCTION_CREDITS_CONSO_OA    IS NULL
   OR  EPARGNE_ADD_OA                 IS NULL
   OR  SOUSCRIPTION_CARTES_UNITE_OA   IS NULL
   OR  EER_PARTICULIER_OA             IS NULL;
COMMIT;

-- Si la ligne vide a AUSSI SK_AGENCE ou ANNEE_MOIS à NULL, ajoute (option B) :
-- UPDATE BTK_BI.B_OBJECTIF
--   SET SK_AGENCE  = NVL(SK_AGENCE,  (SELECT MIN(SK_AGENCE) FROM BTK_BI.AGENCE)),
--       ANNEE_MOIS = NVL(ANNEE_MOIS, '1/1/2026')
-- WHERE SK_AGENCE IS NULL OR ANNEE_MOIS IS NULL;
-- COMMIT;

-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser
-- =====================================================================
