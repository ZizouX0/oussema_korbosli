-- =====================================================================
--  Corriger les « (Vide) » et les accents de BTK_BI.B_CLIENTS
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
-- =====================================================================

-- ÉTAPE 0 — combien de vides par colonne ?
SELECT
  SUM(CASE WHEN SEXE IS NULL THEN 1 ELSE 0 END)                       AS sexe_vides,
  SUM(CASE WHEN REGION_ADRESSE_CLIENT IS NULL THEN 1 ELSE 0 END)      AS region_vides,
  SUM(CASE WHEN GOUVERNORAT_ADRESSE_CLIENT IS NULL THEN 1 ELSE 0 END) AS gouv_vides,
  COUNT(*)                                                            AS total
FROM BTK_BI.B_CLIENTS;

-- ---------------------------------------------------------------------
-- ÉTAPE 1 — remplir les cases vides (NVL ne touche que le vide)
-- ---------------------------------------------------------------------
-- SEXE : répartir M / F
UPDATE BTK_BI.B_CLIENTS
SET SEXE = CASE WHEN MOD(SK_CLIENT, 2) = 0 THEN 'M' ELSE 'F' END
WHERE SEXE IS NULL OR TRIM(SEXE) IS NULL;

-- REGION : répartir sur les régions réelles
UPDATE BTK_BI.B_CLIENTS
SET REGION_ADRESSE_CLIENT = CASE MOD(SK_CLIENT, 6)
      WHEN 0 THEN 'REGION TUNIS NORD' WHEN 1 THEN 'REGION TUNIS SUD'
      WHEN 2 THEN 'REGION DU SAHEL'   WHEN 3 THEN 'REGION DU NORD'
      WHEN 4 THEN 'REGION DU CENTRE'  ELSE 'REGION DU SUD' END
WHERE REGION_ADRESSE_CLIENT IS NULL OR TRIM(REGION_ADRESSE_CLIENT) IS NULL;

-- GOUVERNORAT : répartir sur des gouvernorats réels
UPDATE BTK_BI.B_CLIENTS
SET GOUVERNORAT_ADRESSE_CLIENT = CASE MOD(SK_CLIENT, 8)
      WHEN 0 THEN 'Tunis'  WHEN 1 THEN 'Ariana'  WHEN 2 THEN 'Ben Arous' WHEN 3 THEN 'Sfax'
      WHEN 4 THEN 'Sousse' WHEN 5 THEN 'Nabeul'  WHEN 6 THEN 'Bizerte'   ELSE 'Monastir' END
WHERE GOUVERNORAT_ADRESSE_CLIENT IS NULL OR TRIM(GOUVERNORAT_ADRESSE_CLIENT) IS NULL;

COMMIT;

-- ---------------------------------------------------------------------
-- ÉTAPE 2 — les accents (« SociÃ©té »)
-- ---------------------------------------------------------------------
-- D'ABORD vérifier OÙ est le problème :
SELECT DISTINCT TYPE_CLIENT FROM BTK_BI.B_CLIENTS ORDER BY 1;
--   * Si SQL Developer affiche « Société » correctement -> le souci est dans
--     Power BI (encodage de la connexion), PAS dans la base : ne pas UPDATE.
--   * Si SQL Developer affiche aussi « SociÃ©té » -> la donnée est corrompue,
--     lance la correction ci-dessous.

UPDATE BTK_BI.B_CLIENTS
SET TYPE_CLIENT = 'Société'
WHERE UPPER(TYPE_CLIENT) LIKE 'SOCI%T%' AND TYPE_CLIENT <> 'Société';
COMMIT;

-- ---------------------------------------------------------------------
-- ÉTAPE 3 — vérifier : plus aucun vide
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS reste_vides FROM BTK_BI.B_CLIENTS
WHERE SEXE IS NULL OR REGION_ADRESSE_CLIENT IS NULL OR GOUVERNORAT_ADRESSE_CLIENT IS NULL;

-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser
-- =====================================================================
