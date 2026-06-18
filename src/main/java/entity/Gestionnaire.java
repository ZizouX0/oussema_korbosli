package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "GESTIONNAIRE")
public class Gestionnaire {

    @Id
    @Column(name = "SK_UTILISATEUR")
    private Long id;

    @Column(name = "NOM_COMPLET", length = 200)
    private String nomComplet;

    @Column(name = "EMAIL", length = 200)
    private String email;

    @Column(name = "EST_GESTIONNAIRE")
    private Integer estGestionnaire;

    @Column(name = "EST_SUSPENDU")
    private Integer estSuspendu;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "SK_RESPONSABLE")
    private Long skResponsable;

    public Gestionnaire() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNomComplet() { return nomComplet; }
    public void setNomComplet(String nomComplet) { this.nomComplet = nomComplet; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public Integer getEstGestionnaire() { return estGestionnaire; }
    public void setEstGestionnaire(Integer estGestionnaire) { this.estGestionnaire = estGestionnaire; }

    public Integer getEstSuspendu() { return estSuspendu; }
    public void setEstSuspendu(Integer estSuspendu) { this.estSuspendu = estSuspendu; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long skAgence) { this.skAgence = skAgence; }

    public Long getSkResponsable() { return skResponsable; }
    public void setSkResponsable(Long skResponsable) { this.skResponsable = skResponsable; }
}
