-- =====================================================================
--  Créer un schéma dédié pour Power BI (BTK_BI) et y COPIER les données
--  À exécuter dans SQL Developer, connecté en SYSTEM, sur FREEPDB1
--  (ta connexion « BD » actuelle, celle qui voit déjà les tables)
-- =====================================================================

-- 1) Nouvel utilisateur / schéma pour la BI
CREATE USER BTK_BI IDENTIFIED BY "Btk_BI_2026";
GRANT CONNECT, RESOURCE TO BTK_BI;
ALTER USER BTK_BI QUOTA UNLIMITED ON USERS;

-- 2) Copier les tables (avec les données) depuis le schéma SYSTEM
CREATE TABLE BTK_BI.AGENCE         AS SELECT * FROM SYSTEM.AGENCE;
CREATE TABLE BTK_BI.B_UTILISATEURS AS SELECT * FROM SYSTEM.B_UTILISATEURS;
CREATE TABLE BTK_BI.B_CLIENTS      AS SELECT * FROM SYSTEM.B_CLIENTS;
CREATE TABLE BTK_BI.B_OBJECTIF     AS SELECT * FROM SYSTEM.B_OBJECTIF;
CREATE TABLE BTK_BI.POINTAGE       AS SELECT * FROM SYSTEM.POINTAGE;
CREATE TABLE BTK_BI.GESTIONNAIRE   AS SELECT * FROM SYSTEM.GESTIONNAIRE;
COMMIT;

-- (optionnel) autres tables si tu en as besoin :
-- CREATE TABLE BTK_BI.CLIENT   AS SELECT * FROM SYSTEM.CLIENT;
-- CREATE TABLE BTK_BI.OBJECTIF AS SELECT * FROM SYSTEM.OBJECTIF;

-- 3) Vérifier que tout est copié
SELECT table_name FROM all_tables WHERE owner = 'BTK_BI' ORDER BY table_name;

-- =====================================================================
--  Ensuite dans Power BI :
--    Obtenir les données -> Oracle
--    Serveur   : localhost:1521/FREEPDB1
--    Utilisateur : BTK_BI      Mot de passe : Btk_BI_2026
--    -> dans le Navigateur, déplie le schéma BTK_BI (tout en haut, "B...")
--    -> coche tes tables -> Charger
-- =====================================================================
