package entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.List;

@Entity
@Table(name = "DEMANDE_AGENCE")
public class DemandeAgence {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "DEMANDE_AGENCE_SEQ")
    @SequenceGenerator(name = "DEMANDE_AGENCE_SEQ", sequenceName = "DEMANDE_AGENCE_SEQ", allocationSize = 1)
    @Column(name = "ID_DEMANDE")
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ID_DIRECTEUR", nullable = false)
    private Utilisateur directeur;

    @Column(name = "TYPE_DEMANDE", nullable = false, length = 30)
    private String typeDemande;

    @Column(name = "STATUT", length = 20)
    private String statut = "EN_ATTENTE";

    @Column(name = "CODE_AGENCE_PROP", nullable = false, length = 20)
    private String codeAgencePropose;

    @Column(name = "NOM_AGENCE_PROP", nullable = false, length = 200)
    private String nomAgencePropose;

    @Column(name = "ADRESSE_PROP", length = 500)
    private String adresseProposee;

    @Column(name = "DATE_CREATION")
    private Instant dateCreation;

    @Column(name = "DATE_DECISION")
    private Instant dateDecision;

    @Column(name = "COMMENTAIRE_ADMIN", length = 1000)
    private String commentaireAdmin;

    @ManyToMany
    @JoinTable(
            name = "DEMANDE_AGENCE_UTILISATEUR",
            joinColumns = @JoinColumn(name = "ID_DEMANDE"),
            inverseJoinColumns = @JoinColumn(name = "SK_UTILISATEUR")
    )
    private List<Utilisateur> utilisateursDemandes;

    public DemandeAgence() {
    }

    public Long getId() {
        return id;
    }

    public Utilisateur getDirecteur() {
        return directeur;
    }

    public void setDirecteur(Utilisateur directeur) {
        this.directeur = directeur;
    }

    public String getTypeDemande() {
        return typeDemande;
    }

    public void setTypeDemande(String typeDemande) {
        this.typeDemande = typeDemande;
    }

    public String getStatut() {
        return statut;
    }

    public void setStatut(String statut) {
        this.statut = statut;
    }

    public String getCodeAgencePropose() {
        return codeAgencePropose;
    }

    public void setCodeAgencePropose(String codeAgencePropose) {
        this.codeAgencePropose = codeAgencePropose;
    }

    public String getNomAgencePropose() {
        return nomAgencePropose;
    }

    public void setNomAgencePropose(String nomAgencePropose) {
        this.nomAgencePropose = nomAgencePropose;
    }

    public String getAdresseProposee() {
        return adresseProposee;
    }

    public void setAdresseProposee(String adresseProposee) {
        this.adresseProposee = adresseProposee;
    }

    public Instant getDateCreation() {
        return dateCreation;
    }

    public void setDateCreation(Instant dateCreation) {
        this.dateCreation = dateCreation;
    }

    public Instant getDateDecision() {
        return dateDecision;
    }

    public void setDateDecision(Instant dateDecision) {
        this.dateDecision = dateDecision;
    }

    public String getCommentaireAdmin() {
        return commentaireAdmin;
    }

    public void setCommentaireAdmin(String commentaireAdmin) {
        this.commentaireAdmin = commentaireAdmin;
    }

    public List<Utilisateur> getUtilisateursDemandes() {
        return utilisateursDemandes;
    }

    public void setUtilisateursDemandes(List<Utilisateur> utilisateursDemandes) {
        this.utilisateursDemandes = utilisateursDemandes;
    }
}

