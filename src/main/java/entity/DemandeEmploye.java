package entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "DEMANDE_EMPLOYE")
public class DemandeEmploye {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "DEMANDE_EMPLOYE_SEQ")
    @SequenceGenerator(name = "DEMANDE_EMPLOYE_SEQ", sequenceName = "DEMANDE_EMPLOYE_SEQ", allocationSize = 1)
    @Column(name = "ID_DEMANDE")
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ID_DIRECTEUR", nullable = false)
    private Utilisateur directeur;

    @Column(name = "NOM", nullable = false, length = 100)
    private String nom;

    @Column(name = "PRENOM", nullable = false, length = 100)
    private String prenom;

    @Column(name = "EMAIL", length = 200)
    private String email;

    @Column(name = "MATRICULE", length = 50)
    private String matricule;

    @Column(name = "SK_AGENCE")
    private Long skAgence;

    @Column(name = "ROLE_PREVU")
    private Double rolePrevu; // 1.0 for Gest, 0.0 for others

    @Column(name = "STATUT", length = 20)
    private String statut = "EN_ATTENTE";

    @Column(name = "DATE_CREATION")
    private Instant dateCreation;

    @Column(name = "COMMENTAIRE_ADMIN", length = 1000)
    private String commentaireAdmin;

    public DemandeEmploye() {
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Utilisateur getDirecteur() { return directeur; }
    public void setDirecteur(Utilisateur directeur) { this.directeur = directeur; }

    public String getNom() { return nom; }
    public void setNom(String nom) { this.nom = nom; }

    public String getPrenom() { return prenom; }
    public void setPrenom(String prenom) { this.prenom = prenom; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getMatricule() { return matricule; }
    public void setMatricule(String matricule) { this.matricule = matricule; }

    public Long getSkAgence() { return skAgence; }
    public void setSkAgence(Long skAgence) { this.skAgence = skAgence; }

    public Double getRolePrevu() { return rolePrevu; }
    public void setRolePrevu(Double rolePrevu) { this.rolePrevu = rolePrevu; }

    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }

    public Instant getDateCreation() { return dateCreation; }
    public void setDateCreation(Instant dateCreation) { this.dateCreation = dateCreation; }

    public String getCommentaireAdmin() { return commentaireAdmin; }
    public void setCommentaireAdmin(String commentaireAdmin) { this.commentaireAdmin = commentaireAdmin; }
}
