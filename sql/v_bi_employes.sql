-- Vue pour l'analyse des effectifs (Power BI)
-- Cette vue regroupe les informations des utilisateurs avec leurs agences respectives

CREATE OR REPLACE VIEW V_BI_EMPLOYES AS
SELECT 
    U.SK_UTILISATEUR AS ID_EMPLOYE,
    U.LIBELLE_UTILISATEUR AS NOM_COMPLET,
    U.EMAIL_UTILISATEUR AS EMAIL,
    CASE 
        WHEN U.EST_GESTIONNAIRE = 1 THEN 'Gestionnaire'
        WHEN U.EST_GESTIONNAIRE = 0 AND U.SK_AGENCE = 31 THEN 'Hors Commercial'
        ELSE 'Conseiller'
    END AS ROLE_LABEL,
    CASE 
        WHEN U.EST_SUSPENDU = 1 THEN 'Suspendu'
        ELSE 'Actif'
    END AS STATUT,
    A.LIBELLE_AGENCE AS NOM_AGENCE,
    A.DISTRICT AS DISTRICT_AGENCE,
    A.ADRESSE_AGENCE AS ADRESSE_AGENCE
FROM 
    B_UTILISATEURS U
LEFT JOIN 
    AGENCE A ON U.SK_AGENCE = A.SK_AGENCE;

COMMENT ON COLUMN V_BI_EMPLOYES.ROLE_LABEL IS 'Rôle calculé selon les règles métier de la BTK';
COMMENT ON COLUMN V_BI_EMPLOYES.NOM_AGENCE IS 'Nom de l''agence de rattachement';
