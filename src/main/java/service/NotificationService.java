package service;

import entity.Utilisateur;
import entity.Notification;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.time.Instant;
import java.util.List;

@Stateless
public class NotificationService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public void notifyUser(Utilisateur destinataire, String type, String message) {
        Notification notification = new Notification();
        notification.setDestinataire(destinataire);
        notification.setTypeNotif(type);
        notification.setMessage(message);
        notification.setLue("N");
        notification.setDateCreation(Instant.now());
        em.persist(notification);
    }

    public List<Notification> findUnread(Utilisateur destinataire) {
        return em.createQuery("SELECT n FROM Notification n WHERE n.destinataire = :dest AND n.lue = 'N' ORDER BY n.dateCreation DESC",
                        Notification.class)
                .setParameter("dest", destinataire)
                .getResultList();
    }
}

