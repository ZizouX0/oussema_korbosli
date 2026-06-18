package entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "DEMANDES_MODIFICATION")
public class DemandeModification {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "DEMANDE_MODIF_SEQ")
    @SequenceGenerator(name = "DEMANDE_MODIF_SEQ", sequenceName = "DEMANDE_MODIF_SEQ", allocationSize = 1)
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ID_USER", nullable = false)
    private Utilisateur utilisateur;

    @Column(name = "CHAMP", nullable = false, length = 20)
    private String champ; // 'nom' ou 'email'

    @Column(name = "ANCIENNE_VAL", length = 200)
    private String ancienneVal;

    @Column(name = "NOUVELLE_VAL", nullable = false, length = 200)
    private String nouvelleVal;

    @Column(name = "STATUT", length = 20)
    private String statut = "EN_ATTENTE";

    @Column(name = "DATE_DEMANDE")
    private Instant dateDemande = Instant.now();

    @Column(name = "DATE_DECISION")
    private Instant dateDecision;

    @Column(name = "COMMENTAIRE", length = 1000)
    private String commentaire;

    public DemandeModification() {
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Utilisateur getUtilisateur() { return utilisateur; }
    public void setUtilisateur(Utilisateur utilisateur) { this.utilisateur = utilisateur; }

    public String getChamp() { return champ; }
    public void setChamp(String champ) { this.champ = champ; }

    public String getAncienneVal() { return ancienneVal; }
    public void setAncienneVal(String ancienneVal) { this.ancienneVal = ancienneVal; }

    public String getNouvelleVal() { return nouvelleVal; }
    public void setNouvelleVal(String nouvelleVal) { this.nouvelleVal = nouvelleVal; }

    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }

    public Instant getDateDemande() { return dateDemande; }
    public void setDateDemande(Instant dateDemande) { this.dateDemande = dateDemande; }

    public Instant getDateDecision() { return dateDecision; }
    public void setDateDecision(Instant dateDecision) { this.dateDecision = dateDecision; }

    public String getCommentaire() { return commentaire; }
    public void setCommentaire(String commentaire) { this.commentaire = commentaire; }
}
