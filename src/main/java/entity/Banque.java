
package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "B_BANQUE")
public class Banque {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "BANQUE_SEQ")
    @SequenceGenerator(name = "BANQUE_SEQ", sequenceName = "BANQUE_SEQ", allocationSize = 1)
    @Column(name = "ID_BANQUE")
    private Long id;

    @Column(name = "CODE_BANQUE", nullable = false, unique = true, length = 20)
    private String code;

    @Column(name = "NOM_BANQUE", nullable = false, length = 200)
    private String nom;

    @Column(name = "OBJECTIF", length = 1000)
    private String objectif;

    @Column(name = "SECTEUR", length = 100)
    private String secteur;

    @Column(name = "STATUT", length = 20)
    private String statut = "ACTIVE";

    public Banque() {}

    public Long getId() { return id; }

    public String getCode() { return code; }
    public void setCode(String code) { this.code = code; }

    public String getNom() { return nom; }
    public void setNom(String nom) { this.nom = nom; }

    public String getObjectif() { return objectif; }
    public void setObjectif(String objectif) { this.objectif = objectif; }

    public String getSecteur() { return secteur; }
    public void setSecteur(String secteur) { this.secteur = secteur; }

    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }
}