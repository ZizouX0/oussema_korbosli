-- =====================================================================
--  Rééquilibrer STATUT_CLIENT dans BTK_BI.B_CLIENTS
--  Objectif : un anneau « Statut du portefeuille » lisible (pas 100 % d'une
--  seule valeur) + orthographe uniforme (Actif / Inactif).
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
-- =====================================================================

-- ÉTAPE 0 — voir la répartition actuelle
SELECT STATUT_CLIENT, COUNT(*) AS nb
FROM   BTK_BI.B_CLIENTS
GROUP  BY STATUT_CLIENT
ORDER  BY nb DESC;

-- ÉTAPE 1 — rééquilibrer : ~72 % Actif / ~28 % Inactif
--   Réparti de façon déterministe par SK_CLIENT (MOD), donc reproductible.
UPDATE BTK_BI.B_CLIENTS
SET STATUT_CLIENT = CASE WHEN MOD(SK_CLIENT, 100) < 72 THEN 'Actif' ELSE 'Inactif' END;
COMMIT;

-- ÉTAPE 2 — vérifier le nouvel équilibre
SELECT STATUT_CLIENT,
       COUNT(*)                                          AS nb,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)  AS pourcentage
FROM   BTK_BI.B_CLIENTS
GROUP  BY STATUT_CLIENT
ORDER  BY nb DESC;

-- =====================================================================
--  VARIANTE 3 valeurs (comme la maquette : Actif / Inactif / Prospect)
--  ~78 % Actif, ~17 % Inactif, ~5 % Prospect :
--
--  UPDATE BTK_BI.B_CLIENTS
--  SET STATUT_CLIENT = CASE
--        WHEN MOD(SK_CLIENT, 100) < 78 THEN 'Actif'
--        WHEN MOD(SK_CLIENT, 100) < 95 THEN 'Inactif'
--        ELSE 'Prospect'
--      END;
--  COMMIT;
-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser
-- =====================================================================
