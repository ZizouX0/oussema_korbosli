package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "B_OBJECTIF")
public class Objectif {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "B_OBJECTIF_SEQ")
    @SequenceGenerator(name = "B_OBJECTIF_SEQ", sequenceName = "B_OBJECTIF_SEQ", allocationSize = 1)
    @Column(name = "ID_OBJECTIF")
    private Long id;

    @Column(name = "SITUATION_ADMINISTRATIVE", length = 50)
    private String situationAdministrative;

    @Column(name = "EER_PARTICULIER_OA")
    private Double eerParticulier;

    @Column(name = "EER_HORS_PARTICULIER_OA")
    private Double eerHorsParticulier;

    @Column(name = "SOUSCRIPTION_COMPTE_CHEQUES_OA")
    private Double souscriptionCompteCheques;

    @Column(name = "SOUSCRIPTION_COMPTE_EPARGNES_OA")
    private Double souscriptionCompteEpargnes;

    @Column(name = "SOUSCRIPTION_COMPTE_COURANTS_OA")
    private Double souscriptionCompteCourants;

    @Column(name = "SOUSCRIPTION_PACKS_PARTICULIER_OA")
    private Double souscriptionPacksParticulier;

    @Column(name = "SOUSCRIPTION_PACKS_PRO_OA")
    private Double souscriptionPacksPro;

    @Column(name = "SOUSCRIPTION_CARTES_UNITE_OA")
    private Double souscriptionCartesUnite;

    @Column(name = "DAV_PP_ADD_OA")
    private Double davPp;

    @Column(name = "DAV_PM_ADD_OA")
    private Double davPm;

    @Column(name = "EPARGNE_ADD_OA")
    private Double epargne;

    @Column(name = "PRODUCTION_CREDITS_CONSO_OA")
    private Double productionCreditsConso;

    @Column(name = "PRODUCTION_CREDITS_IMMO_OA")
    private Double productionCreditsImmo;

    @Column(name = "PRODUCTION_CREDITS_INVESTISSEMENT_OA")
    private Double productionCreditsInvest;

    @Column(name = "EVOL_ENCOURS_ESCOMPTE_OA")
    private Double evolEncours;

    @Column(name = "EVOL_ENCOURS_CREDITS_GESTION_OA")
    private Double evolCreditsGestion;

    @Column(name = "EVOL_ENCOURS_ENGAGEMENTS_PAR_SIGNATURE_OA")
    private Double evolEngagements;

    @Column(name = "ANNEE_MOIS", length = 20)
    private String anneeMois;

    @Column(name = "SK_GESTIONNAIRE")
    private Long skGestionnaire;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "SK_UTILISATEUR")
    private Long skUtilisateur;

    public Objectif() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getSituationAdministrative() { return situationAdministrative; }
    public void setSituationAdministrative(String v) { this.situationAdministrative = v; }

    public Double getEerParticulier() { return eerParticulier; }
    public void setEerParticulier(Double v) { this.eerParticulier = v; }

    public Double getEerHorsParticulier() { return eerHorsParticulier; }
    public void setEerHorsParticulier(Double v) { this.eerHorsParticulier = v; }

    public Double getSouscriptionCompteCheques() { return souscriptionCompteCheques; }
    public void setSouscriptionCompteCheques(Double v) { this.souscriptionCompteCheques = v; }

    public Double getSouscriptionCompteEpargnes() { return souscriptionCompteEpargnes; }
    public void setSouscriptionCompteEpargnes(Double v) { this.souscriptionCompteEpargnes = v; }

    public Double getSouscriptionCompteCourants() { return souscriptionCompteCourants; }
    public void setSouscriptionCompteCourants(Double v) { this.souscriptionCompteCourants = v; }

    public Double getSouscriptionPacksParticulier() { return souscriptionPacksParticulier; }
    public void setSouscriptionPacksParticulier(Double v) { this.souscriptionPacksParticulier = v; }

    public Double getSouscriptionPacksPro() { return souscriptionPacksPro; }
    public void setSouscriptionPacksPro(Double v) { this.souscriptionPacksPro = v; }

    public Double getSouscriptionCartesUnite() { return souscriptionCartesUnite; }
    public void setSouscriptionCartesUnite(Double v) { this.souscriptionCartesUnite = v; }

    public Double getDavPp() { return davPp; }
    public void setDavPp(Double v) { this.davPp = v; }

    public Double getDavPm() { return davPm; }
    public void setDavPm(Double v) { this.davPm = v; }

    public Double getEpargne() { return epargne; }
    public void setEpargne(Double v) { this.epargne = v; }

    public Double getProductionCreditsConso() { return productionCreditsConso; }
    public void setProductionCreditsConso(Double v) { this.productionCreditsConso = v; }

    public Double getProductionCreditsImmo() { return productionCreditsImmo; }
    public void setProductionCreditsImmo(Double v) { this.productionCreditsImmo = v; }

    public Double getProductionCreditsInvest() { return productionCreditsInvest; }
    public void setProductionCreditsInvest(Double v) { this.productionCreditsInvest = v; }

    public Double getEvolEncours() { return evolEncours; }
    public void setEvolEncours(Double v) { this.evolEncours = v; }

    public Double getEvolCreditsGestion() { return evolCreditsGestion; }
    public void setEvolCreditsGestion(Double v) { this.evolCreditsGestion = v; }

    public Double getEvolEngagements() { return evolEngagements; }
    public void setEvolEngagements(Double v) { this.evolEngagements = v; }

    public String getAnneeMois() { return anneeMois; }
    public void setAnneeMois(String v) { this.anneeMois = v; }

    public Long getSkGestionnaire() { return skGestionnaire; }
    public void setSkGestionnaire(Long v) { this.skGestionnaire = v; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long v) { this.skAgence = v; }

    public Long getSkUtilisateur() { return skUtilisateur; }
    public void setSkUtilisateur(Long v) { this.skUtilisateur = v; }
}