package entity;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Pointage (présence) d'un employé pour une journée donnée.
 * Statut : PRESENT, RETARD ou ABSENT. Source : AUTO (bouton « Pointer »)
 * ou MANUEL (saisie / correction par l'administrateur).
 */
@Entity
@Table(name = "POINTAGE")
public class Pointage {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "POINTAGE_SEQ")
    @SequenceGenerator(name = "POINTAGE_SEQ", sequenceName = "POINTAGE_SEQ", allocationSize = 1)
    @Column(name = "ID_POINTAGE")
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "SK_UTILISATEUR", nullable = false)
    private Utilisateur employe;

    @Column(name = "DATE_POINTAGE", nullable = false)
    private LocalDate datePointage;

    @Column(name = "HEURE_ARRIVEE")
    private LocalDateTime heureArrivee;

    @Column(name = "HEURE_DEPART")
    private LocalDateTime heureDepart;

    @Column(name = "STATUT", length = 20)
    private String statut;

    @Column(name = "SOURCE", length = 10)
    private String source;

    @Column(name = "COMMENTAIRE", length = 1000)
    private String commentaire;

    public Pointage() {
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Utilisateur getEmploye() { return employe; }
    public void setEmploye(Utilisateur employe) { this.employe = employe; }

    public LocalDate getDatePointage() { return datePointage; }
    public void setDatePointage(LocalDate datePointage) { this.datePointage = datePointage; }

    public LocalDateTime getHeureArrivee() { return heureArrivee; }
    public void setHeureArrivee(LocalDateTime heureArrivee) { this.heureArrivee = heureArrivee; }

    public LocalDateTime getHeureDepart() { return heureDepart; }
    public void setHeureDepart(LocalDateTime heureDepart) { this.heureDepart = heureDepart; }

    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }

    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }

    public String getCommentaire() { return commentaire; }
    public void setCommentaire(String commentaire) { this.commentaire = commentaire; }
}
