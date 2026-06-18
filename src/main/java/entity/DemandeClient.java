package entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "DEMANDE_CLIENT")
public class DemandeClient {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "DEMANDE_CLIENT_SEQ")
    @SequenceGenerator(name = "DEMANDE_CLIENT_SEQ", sequenceName = "DEMANDE_CLIENT_SEQ", allocationSize = 1)
    @Column(name = "ID_DEMANDE")
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ID_DIRECTEUR", nullable = false)
    private Utilisateur directeur;

    @Column(name = "NOM_CLIENT", nullable = false, length = 200)
    private String nomClient;

    @Column(name = "PRENOM_CLIENT", nullable = false, length = 200)
    private String prenomClient;

    @Column(name = "SEXE", length = 1)
    private String sexe;

    @Column(name = "TYPE_CLIENT", length = 50)
    private String typeClient;

    @Column(name = "SECTEUR_ACTIVITE", length = 200)
    private String secteurActivite;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "SK_GESTIONNAIRE")
    private Long skGestionnaire;

    @Column(name = "STATUT", length = 20)
    private String statut = "EN_ATTENTE";

    @Column(name = "DATE_CREATION")
    private Instant dateCreation;

    @Column(name = "COMMENTAIRE_ADMIN", length = 1000)
    private String commentaireAdmin;

    public DemandeClient() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Utilisateur getDirecteur() { return directeur; }
    public void setDirecteur(Utilisateur directeur) { this.directeur = directeur; }

    public String getNomClient() { return nomClient; }
    public void setNomClient(String nomClient) { this.nomClient = nomClient; }

    public String getPrenomClient() { return prenomClient; }
    public void setPrenomClient(String prenomClient) { this.prenomClient = prenomClient; }

    public String getSexe() { return sexe; }
    public void setSexe(String sexe) { this.sexe = sexe; }

    public String getTypeClient() { return typeClient; }
    public void setTypeClient(String typeClient) { this.typeClient = typeClient; }

    public String getSecteurActivite() { return secteurActivite; }
    public void setSecteurActivite(String secteurActivite) { this.secteurActivite = secteurActivite; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long skAgence) { this.skAgence = skAgence; }

    public Long getSkGestionnaire() { return skGestionnaire; }
    public void setSkGestionnaire(Long skGestionnaire) { this.skGestionnaire = skGestionnaire; }

    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }

    public Instant getDateCreation() { return dateCreation; }
    public void setDateCreation(Instant dateCreation) { this.dateCreation = dateCreation; }

    public String getCommentaireAdmin() { return commentaireAdmin; }
    public void setCommentaireAdmin(String commentaireAdmin) { this.commentaireAdmin = commentaireAdmin; }
}
