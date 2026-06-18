package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "B_CLIENTS")
public class BClient {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "B_CLIENTS_SEQ")
    @SequenceGenerator(name = "B_CLIENTS_SEQ", sequenceName = "B_CLIENTS_SEQ", allocationSize = 1)
    @Column(name = "SK_CLIENT")
    private Long id;

    @Column(name = "NOM_CLIENT", length = 200)
    private String nomClient;

    @Column(name = "PRENOM_CLIENT", length = 200)
    private String prenomClient;

    @Column(name = "SEXE", length = 1)
    private String sexe;

    @Column(name = "TYPE_CLIENT", length = 50)
    private String typeClient;

    @Column(name = "STATUT_CLIENT", length = 50)
    private String statutClient;

    @Column(name = "SECTEUR_ACTIVITE", length = 200)
    private String secteurActivite;

    @Column(name = "REGION_ADRESSE_CLIENT", length = 100)
    private String region;

    @Column(name = "GOUVERNORAT_ADRESSE_CLIENT", length = 100)
    private String gouvernorat;

    @Column(name = "DELEGATION_ADRESSE_CLIENT", length = 100)
    private String delegation;

    @Column(name = "LIBELLE_PROFIL", length = 200)
    private String libelleProfil;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "SK_GESTIONNAIRE")
    private Long skGestionnaire;

    @Column(name = "SK_UTILISATEUR")
    private Long skUtilisateur;

    public BClient() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNomClient() { return nomClient; }
    public void setNomClient(String v) { this.nomClient = v; }

    public String getPrenomClient() { return prenomClient; }
    public void setPrenomClient(String v) { this.prenomClient = v; }

    public String getSexe() { return sexe; }
    public void setSexe(String v) { this.sexe = v; }

    public String getTypeClient() { return typeClient; }
    public void setTypeClient(String v) { this.typeClient = v; }

    public String getStatutClient() { return statutClient; }
    public void setStatutClient(String v) { this.statutClient = v; }

    public String getSecteurActivite() { return secteurActivite; }
    public void setSecteurActivite(String v) { this.secteurActivite = v; }

    public String getRegion() { return region; }
    public void setRegion(String v) { this.region = v; }

    public String getGouvernorat() { return gouvernorat; }
    public void setGouvernorat(String v) { this.gouvernorat = v; }

    public String getDelegation() { return delegation; }
    public void setDelegation(String v) { this.delegation = v; }

    public String getLibelleProfil() { return libelleProfil; }
    public void setLibelleProfil(String v) { this.libelleProfil = v; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long v) { this.skAgence = v; }

    public Long getSkGestionnaire() { return skGestionnaire; }
    public void setSkGestionnaire(Long v) { this.skGestionnaire = v; }

    public Long getSkUtilisateur() { return skUtilisateur; }
    public void setSkUtilisateur(Long v) { this.skUtilisateur = v; }
}
