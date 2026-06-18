-- Vue pour l'analyse du portefeuille clients (Power BI)
-- Segmentée par type de client, statut et géographie

CREATE OR REPLACE VIEW V_BI_CLIENTS AS
SELECT 
    C.SK_CLIENT AS ID_CLIENT,
    C.NOM_CLIENT || ' ' || C.PRENOM_CLIENT AS NOM_COMPLET,
    C.SEXE,
    NVL(C.TYPE_CLIENT, 'Non spécifié') AS TYPE_CLIENT,
    NVL(C.STATUT_CLIENT, 'Inconnu') AS STATUT,
    A.LIBELLE_AGENCE AS NOM_AGENCE,
    A.DISTRICT AS DISTRICT_AGENCE
FROM 
    CLIENT_BTK C
LEFT JOIN 
    AGENCE A ON C.SK_AGENCE = A.SK_AGENCE;

COMMENT ON COLUMN V_BI_CLIENTS.TYPE_CLIENT IS 'Particulier, Société, etc.';
COMMENT ON COLUMN V_BI_CLIENTS.NOM_AGENCE IS 'Agence gérant le client';
