package entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "JOURNAL_ACTION")
public class JournalAction {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "JOURNAL_ACTION_SEQ")
    @SequenceGenerator(name = "JOURNAL_ACTION_SEQ", sequenceName = "JOURNAL_ACTION_SEQ", allocationSize = 1)
    @Column(name = "ID_JOURNAL")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "ID_UTILISATEUR")
    private Utilisateur utilisateur;

    @Column(name = "ROLE", length = 30)
    private String role;

    @Column(name = "ACTION_CODE", nullable = false, length = 50)
    private String actionCode;

    @Column(name = "ENTITE", length = 50)
    private String entite;

    @Column(name = "ID_ENTITE")
    private Long idEntite;

    @Column(name = "DATE_ACTION")
    private Instant dateAction;

    @Lob
    @Column(name = "DETAILS")
    private String details;

    public JournalAction() {
    }

    public Long getId() {
        return id;
    }

    public Utilisateur getUtilisateur() {
        return utilisateur;
    }

    public void setUtilisateur(Utilisateur utilisateur) {
        this.utilisateur = utilisateur;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getActionCode() {
        return actionCode;
    }

    public void setActionCode(String actionCode) {
        this.actionCode = actionCode;
    }

    public String getEntite() {
        return entite;
    }

    public void setEntite(String entite) {
        this.entite = entite;
    }

    public Long getIdEntite() {
        return idEntite;
    }

    public void setIdEntite(Long idEntite) {
        this.idEntite = idEntite;
    }

    public Instant getDateAction() {
        return dateAction;
    }

    public void setDateAction(Instant dateAction) {
        this.dateAction = dateAction;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }
}

