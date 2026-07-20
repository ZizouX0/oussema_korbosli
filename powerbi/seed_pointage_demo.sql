-- =====================================================================
--  Injecter 100 pointages de démonstration dans BTK_BI.POINTAGE
--  Objectif : donner du volume au tableau de bord Power BI (anneau
--  Présence à 3 parts, taux de présence réaliste, évolution mensuelle).
--  À exécuter dans SQL Developer, connecté en SYSTEM (connexion « BD »).
--
--  Répartition : ~65 % PRÉSENT · ~25 % RETARD · ~10 % ABSENT
--  (le retard compte comme présent dans le taux ; les absences le font
--   descendre sous 100 % — c'est ce qui rend le KPI crédible).
--  Employés tirés au hasard parmi ceux qui existent réellement.
-- =====================================================================
SET SERVEROUTPUT ON;

DECLARE
  TYPE t_emp IS TABLE OF BTK_BI.B_UTILISATEURS.SK_UTILISATEUR%TYPE;
  v_emps t_emp;
  v_base NUMBER;
  v_emp  NUMBER;
  v_date DATE;
  v_stat VARCHAR2(20);
  v_src  VARCHAR2(10);
  v_arr  TIMESTAMP;
  v_dep  TIMESTAMP;
  v_r    NUMBER;
BEGIN
  -- liste des employés réels
  SELECT SK_UTILISATEUR BULK COLLECT INTO v_emps FROM BTK_BI.B_UTILISATEURS;
  IF v_emps.COUNT = 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Aucun employé dans BTK_BI.B_UTILISATEURS.');
  END IF;

  -- point de départ des identifiants (évite tout conflit de clé)
  SELECT NVL(MAX(ID_POINTAGE), 0) INTO v_base FROM BTK_BI.POINTAGE;

  FOR i IN 1 .. 100 LOOP
    -- employé aléatoire
    v_emp := v_emps( TRUNC(DBMS_RANDOM.VALUE(1, v_emps.COUNT + 1)) );

    -- date aléatoire sur les 120 derniers jours (≈ 4 mois -> courbe mensuelle)
    v_date := TRUNC(SYSDATE) - TRUNC(DBMS_RANDOM.VALUE(1, 120));

    -- statut : 65 % présent / 25 % retard / 10 % absent
    v_r := DBMS_RANDOM.VALUE(0, 1);
    IF    v_r < 0.65 THEN v_stat := 'PRESENT';
    ELSIF v_r < 0.90 THEN v_stat := 'RETARD';
    ELSE                  v_stat := 'ABSENT';
    END IF;

    -- source : 75 % auto / 25 % manuel
    v_src := CASE WHEN DBMS_RANDOM.VALUE(0, 1) < 0.75 THEN 'AUTO' ELSE 'MANUEL' END;

    -- heures d'arrivée / départ
    IF v_stat = 'ABSENT' THEN
      v_arr := NULL;
      v_dep := NULL;
    ELSIF v_stat = 'RETARD' THEN
      v_arr := CAST(v_date AS TIMESTAMP) + INTERVAL '9' HOUR
                 + NUMTODSINTERVAL(TRUNC(DBMS_RANDOM.VALUE(20, 90)), 'MINUTE');
      v_dep := CAST(v_date AS TIMESTAMP) + INTERVAL '17' HOUR;
    ELSE  -- PRESENT
      v_arr := CAST(v_date AS TIMESTAMP) + INTERVAL '8' HOUR
                 + NUMTODSINTERVAL(TRUNC(DBMS_RANDOM.VALUE(0, 15)), 'MINUTE');
      v_dep := CAST(v_date AS TIMESTAMP) + INTERVAL '17' HOUR;
    END IF;

    INSERT INTO BTK_BI.POINTAGE
      (ID_POINTAGE, SK_UTILISATEUR, DATE_POINTAGE, HEURE_ARRIVEE, HEURE_DEPART, STATUT, SOURCE, COMMENTAIRE)
    VALUES
      (v_base + i, v_emp, v_date, v_arr, v_dep, v_stat, v_src, 'Donnée de démonstration BI');
  END LOOP;

  COMMIT;
  DBMS_OUTPUT.PUT_LINE('OK : 100 pointages insérés dans BTK_BI.POINTAGE.');
END;
/

-- Vérification : la répartition par statut
SELECT STATUT, COUNT(*) AS NB FROM BTK_BI.POINTAGE GROUP BY STATUT ORDER BY NB DESC;

-- =====================================================================
--  Ensuite dans Power BI : Accueil -> Actualiser  (pour recharger POINTAGE)
--  -> l'anneau Présence a 3 parts, le taux devient réaliste (~90 %),
--     la courbe mensuelle se remplit.
--
--  Pour repartir de zéro : DELETE FROM BTK_BI.POINTAGE WHERE COMMENTAIRE =
--  'Donnée de démonstration BI'; COMMIT;
-- =====================================================================
