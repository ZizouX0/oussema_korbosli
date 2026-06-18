package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "CLIENT_BTK")
public class BtkClient {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "CLIENT_BTK_SEQ")
    @SequenceGenerator(name = "CLIENT_BTK_SEQ", sequenceName = "CLIENT_BTK_SEQ", allocationSize = 1)
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

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    public BtkClient() {}

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

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long v) { this.skAgence = v; }
}
