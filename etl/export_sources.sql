-- =====================================================================
--  Export des données sources BTK vers CSV pour la chaîne ETL
--  À exécuter avec SQLcl :   sql BTK_USER/mot_de_passe@dsn @export_sources.sql
--  (SQLcl est fourni gratuitement avec Oracle ; SET SQLFORMAT CSV produit
--   des fichiers CSV avec en-têtes.)
--
--  Les 5 fichiers générés doivent être placés dans  etl/source/
--  puis :  python3 etl_agences.py
-- =====================================================================

SET SQLFORMAT CSV
SET FEEDBACK OFF
SET PAGESIZE 0

-- 1) Agences  -> agences.csv  (SK_AGENCE, LIBELLE_AGENCE, DISTRICT)
SPOOL agences.csv
SELECT SK_AGENCE, LIBELLE_AGENCE, DISTRICT
FROM   AGENCE;
SPOOL OFF

-- 2) Employés -> employes.csv (SK_UTILISATEUR, SK_AGENCE, EST_GESTIONNAIRE)
SPOOL employes.csv
SELECT SK_UTILISATEUR, SK_AGENCE, EST_GESTIONNAIRE
FROM   B_UTILISATEURS;
SPOOL OFF

-- 3) Clients  -> clients.csv  (SK_CLIENT, SK_AGENCE)
SPOOL clients.csv
SELECT SK_CLIENT, SK_AGENCE
FROM   CLIENT_BTK;
SPOOL OFF

-- 4) Objectifs -> objectifs.csv (SK_AGENCE, COMPTES, CREDITS, EPARGNE)
--    Les 3 indicateurs sont agrégés à partir des colonnes de B_OBJECTIF,
--    exactement comme dans la vue V_BI_OBJECTIFS.
SPOOL objectifs.csv
SELECT SK_AGENCE,
       NVL(SOUSCRIPTION_COMPTE_CHEQUES_OA,0)
         + NVL(SOUSCRIPTION_COMPTE_EPARGNES_OA,0)
         + NVL(SOUSCRIPTION_COMPTE_COURANTS_OA,0)   AS COMPTES,
       NVL(PRODUCTION_CREDITS_CONSO_OA,0)
         + NVL(PRODUCTION_CREDITS_IMMO_OA,0)
         + NVL(PRODUCTION_CREDITS_INVESTISSEMENT_OA,0) AS CREDITS,
       NVL(EPARGNE_ADD_OA,0)                        AS EPARGNE
FROM   B_OBJECTIF;
SPOOL OFF

-- 5) Pointages -> pointages.csv (SK_UTILISATEUR, SK_AGENCE, STATUT)
--    L'agence est récupérée via B_UTILISATEURS (la table POINTAGE ne la porte pas).
SPOOL pointages.csv
SELECT P.SK_UTILISATEUR, U.SK_AGENCE, P.STATUT
FROM   POINTAGE P
JOIN   B_UTILISATEURS U ON P.SK_UTILISATEUR = U.SK_UTILISATEUR;
SPOOL OFF

SET FEEDBACK ON
PROMPT Export terminé : agences.csv, employes.csv, clients.csv, objectifs.csv, pointages.csv
PROMPT Déplacez ces 5 fichiers dans etl/source/ puis lancez : python3 etl_agences.py
