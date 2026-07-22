-- =====================================================================
--  Remplir TOUTES les cases vides (NULL) de BTK_BI.B_CLIENTS
--  Principe : chaque case vide reçoit une valeur qui EXISTE DÉJÀ dans sa
--  colonne, répartie de façon déterministe (MOD sur SK_CLIENT).
--  -> aucune nouvelle catégorie, aucun souci d'encodage, plus de « (Vide) ».
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
-- =====================================================================
SET SERVEROUTPUT ON;

DECLARE
  TYPE t_cols IS TABLE OF VARCHAR2(40);
  -- colonnes à remplir (toutes celles qui peuvent avoir des vides)
  v_cols t_cols := t_cols(
    'NOM_CLIENT', 'PRENOM_CLIENT', 'SEXE', 'TYPE_CLIENT', 'STATUT_CLIENT',
    'SECTEUR_ACTIVITE', 'REGION_ADRESSE_CLIENT', 'GOUVERNORAT_ADRESSE_CLIENT',
    'DELEGATION_ADRESSE_CLIENT', 'LIBELLE_PROFIL',
    'SK_AGENCE', 'SK_GESTIONNAIRE', 'SK_UTILISATEUR');
  v_sql VARCHAR2(2000);
  v_n   NUMBER;
BEGIN
  FOR i IN 1 .. v_cols.COUNT LOOP
    v_sql :=
      'UPDATE BTK_BI.B_CLIENTS b SET ' || v_cols(i) || ' = (' ||
      '  SELECT v FROM (' ||
      '    SELECT v, ROW_NUMBER() OVER (ORDER BY v) rn, COUNT(*) OVER () cnt' ||
      '    FROM (SELECT DISTINCT ' || v_cols(i) || ' v FROM BTK_BI.B_CLIENTS' ||
      '          WHERE ' || v_cols(i) || ' IS NOT NULL)' ||
      '  ) x WHERE x.rn = MOD(b.SK_CLIENT, x.cnt) + 1' ||
      ') WHERE b.' || v_cols(i) || ' IS NULL';
    EXECUTE IMMEDIATE v_sql;
    v_n := SQL%ROWCOUNT;
    IF v_n > 0 THEN
      DBMS_OUTPUT.PUT_LINE(RPAD(v_cols(i), 30) || ' : ' || v_n || ' cases remplies');
    END IF;
  END LOOP;
  COMMIT;
  DBMS_OUTPUT.PUT_LINE('--- Terminé : toutes les cases vides sont remplies. ---');
END;
/

-- Vérification : plus aucune ligne avec une case vide sur les colonnes clés
SELECT COUNT(*) AS reste_vides
FROM   BTK_BI.B_CLIENTS
WHERE  SEXE IS NULL OR TYPE_CLIENT IS NULL OR STATUT_CLIENT IS NULL
    OR SECTEUR_ACTIVITE IS NULL OR REGION_ADRESSE_CLIENT IS NULL
    OR GOUVERNORAT_ADRESSE_CLIENT IS NULL OR LIBELLE_PROFIL IS NULL;

-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser
--  -> plus aucun « (Vide) » dans les anneaux et les segments.
-- =====================================================================
