package entity;

import jakarta.persistence.*;

@Entity
@Table(name = "B_UTILISATEURS")
public class Utilisateur {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "UTILISATEUR_SEQ")
    @SequenceGenerator(name = "UTILISATEUR_SEQ", sequenceName = "UTILISATEUR_SEQ", allocationSize = 1)
    @Column(name = "SK_UTILISATEUR")
    private Long id;

    @Column(name = "LIBELLE_UTILISATEUR", length = 200)
    private String libelleUtilisateur;

    @Column(name = "EST_GESTIONNAIRE")
    private Double estGestionnaire;

    @Column(name = "EMAIL_UTILISATEUR", length = 200)
    private String emailUtilisateur;

    @Column(name = "EST_SUSPENDU")
    private Integer estSuspendu;

    @Column(name = "SK_GESTIONNAIRE")
    private Long skGestionnaire;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    public Utilisateur() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getLibelleUtilisateur() {
        return libelleUtilisateur;
    }

    public void setLibelleUtilisateur(String v) {
        this.libelleUtilisateur = v;
    }

    // Alias for JSP compatibility
    public String getLogin() {
        return libelleUtilisateur;
    }

    public void setLogin(String v) {
        this.libelleUtilisateur = v;
    }

    public Double getEstGestionnaire() {
        return estGestionnaire;
    }

    public void setEstGestionnaire(Double v) {
        this.estGestionnaire = v;
    }

    public String getEmailUtilisateur() {
        return emailUtilisateur;
    }

    public void setEmailUtilisateur(String v) {
        this.emailUtilisateur = v;
    }

    public Integer getEstSuspendu() {
        return estSuspendu;
    }

    public void setEstSuspendu(Integer v) {
        this.estSuspendu = v;
    }

    public Long getSkGestionnaire() {
        return skGestionnaire;
    }

    public void setSkGestionnaire(Long v) {
        this.skGestionnaire = v;
    }

    public Long getSkAgence() {
        return skAgence;
    }

    public void setSkAgence(Long v) {
        this.skAgence = v;
    }

    public boolean isGestionnaire() {
        return estGestionnaire != null && estGestionnaire == 1.0;
    }

    public boolean isSuspendu() {
        return estSuspendu != null && estSuspendu == 1;
    }

    /**
     * Logic centralisée basée sur vos requêtes SQL :
     * 1. EST_GESTIONNAIRE = 1 -> Gestionnaire
     * 2. EST_GESTIONNAIRE = 0 ET SK_AGENCE = 31 -> Conseiller
     * 3. Reste -> Hors Commercial
     */
    public String getRoleLabel() {
        if (estGestionnaire != null && estGestionnaire == 1.0) {
            return "Gestionnaire";
        } else if (estGestionnaire != null && estGestionnaire == 0.0 && (skAgence != null && skAgence == 31)) {
            return "Hors Commercial";
        } else {
            return "Conseiller";
        }
    }

    public String getRoleClass() {
        if (estGestionnaire != null && estGestionnaire == 1.0) {
            return "status-approuvee";
        } else if (estGestionnaire != null && estGestionnaire == 0.0 && (skAgence != null && skAgence == 31)) {
            return "status-hors";
        } else {
            return "status-en_attente";
        }
    }
}