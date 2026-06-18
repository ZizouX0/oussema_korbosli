package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "CLIENT")
public class Client {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "CLIENT_SEQ")
    @SequenceGenerator(name = "CLIENT_SEQ", sequenceName = "CLIENT_SEQ", allocationSize = 1)
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

    @Column(name = "GOUVERNORAT", length = 100)
    private String gouvernorat;

    @Column(name = "REGION", length = 100)
    private String region;

    @Column(name = "SECTEUR_ACTIVITE", length = 200)
    private String secteurActivite;

    @Column(name = "LIBELLE_PROFIL", length = 200)
    private String libelleProfil;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "SK_GESTIONNAIRE")
    private Long skGestionnaire;

    public Client() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNomClient() { return nomClient; }
    public void setNomClient(String nomClient) { this.nomClient = nomClient; }

    public String getPrenomClient() { return prenomClient; }
    public void setPrenomClient(String prenomClient) { this.prenomClient = prenomClient; }

    public String getSexe() { return sexe; }
    public void setSexe(String sexe) { this.sexe = sexe; }

    public String getTypeClient() { return typeClient; }
    public void setTypeClient(String typeClient) { this.typeClient = typeClient; }

    public String getStatutClient() { return statutClient; }
    public void setStatutClient(String statutClient) { this.statutClient = statutClient; }

    public String getGouvernorat() { return gouvernorat; }
    public void setGouvernorat(String gouvernorat) { this.gouvernorat = gouvernorat; }

    public String getRegion() { return region; }
    public void setRegion(String region) { this.region = region; }

    public String getSecteurActivite() { return secteurActivite; }
    public void setSecteurActivite(String secteurActivite) { this.secteurActivite = secteurActivite; }

    public String getLibelleProfil() { return libelleProfil; }
    public void setLibelleProfil(String libelleProfil) { this.libelleProfil = libelleProfil; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long skAgence) { this.skAgence = skAgence; }

    public Long getSkGestionnaire() { return skGestionnaire; }
    public void setSkGestionnaire(Long skGestionnaire) { this.skGestionnaire = skGestionnaire; }
}