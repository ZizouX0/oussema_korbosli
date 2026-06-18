package entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "AGENCE")
public class Agence {

    @Id
    @Column(name = "SK_AGENCE")
    private Long id;

    @Column(name = "LIBELLE_AGENCE", nullable = false, length = 200)
    private String nom;

    @Column(name = "ADRESSE_AGENCE", length = 500)
    private String adresse;

    @Column(name = "DISTRICT", length = 200)
    private String district;

    public Agence() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String v) {
        this.nom = v;
    }

    public String getAdresse() {
        return adresse;
    }

    public void setAdresse(String v) {
        this.adresse = v;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String v) {
        this.district = v;
    }
}
