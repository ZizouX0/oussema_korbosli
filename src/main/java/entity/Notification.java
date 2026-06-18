package entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "NOTIFICATION")
public class Notification {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "NOTIFICATION_SEQ")
    @SequenceGenerator(name = "NOTIFICATION_SEQ", sequenceName = "NOTIFICATION_SEQ", allocationSize = 1)
    @Column(name = "ID_NOTIFICATION")
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ID_UTILISATEUR", nullable = false)
    private Utilisateur destinataire;

    @Column(name = "TYPE_NOTIF", nullable = false, length = 50)
    private String typeNotif;

    @Column(name = "MESSAGE", length = 1000)
    private String message;

    @Column(name = "LUE", length = 1)
    private String lue = "N";

    @Column(name = "DATE_CREATION")
    private Instant dateCreation;

    public Notification() {
    }

    public Long getId() {
        return id;
    }

    public Utilisateur getDestinataire() {
        return destinataire;
    }

    public void setDestinataire(Utilisateur destinataire) {
        this.destinataire = destinataire;
    }

    public String getTypeNotif() {
        return typeNotif;
    }

    public void setTypeNotif(String typeNotif) {
        this.typeNotif = typeNotif;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getLue() {
        return lue;
    }

    public void setLue(String lue) {
        this.lue = lue;
    }

    public Instant getDateCreation() {
        return dateCreation;
    }

    public void setDateCreation(Instant dateCreation) {
        this.dateCreation = dateCreation;
    }
}

