package service;

import entity.DemandeModification;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.time.Instant;
import java.util.List;

@Stateless
public class DemandeModificationService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    @EJB
    private NotificationService notificationService;

    @EJB
    private JournalService journalService;

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private SecurityService securityService;

    public DemandeModification submitRequest(Utilisateur user, String champ, String nouvelleVal) {
        DemandeModification demande = new DemandeModification();
        demande.setUtilisateur(user);
        demande.setChamp(champ);
        
        String ancienneVal = champ.equals("nom") ? user.getLibelleUtilisateur() : user.getEmailUtilisateur();
        demande.setAncienneVal(ancienneVal);
        demande.setNouvelleVal(nouvelleVal);
        demande.setStatut("EN_ATTENTE");
        
        em.persist(demande);

        // Notify Director(s) - In this system, we can notify the agency manager or all directors
        // For simplicity, let's notify the security users with role DIRECTOR
        // Actually, let's just log it and the director will see it in their dashboard
        journalService.log(user.getId(), "USER", "DEMANDE_MODIF_SUBMIT", "DemandeModification", demande.getId(),
            "Demande de changement de " + champ + " (" + nouvelleVal + ") soumise.");
            
        return demande;
    }

    public void approveRequest(Long demandeId, String commentaire) {
        DemandeModification demande = em.find(DemandeModification.class, demandeId);
        if (demande != null && "EN_ATTENTE".equals(demande.getStatut())) {
            demande.setStatut("EN_COURS");
            demande.setDateDecision(Instant.now());
            demande.setCommentaire(commentaire);
            
            // Notify Admin
            List<entity.SecurityUser> admins = securityService.findAllAdmins();
            for (entity.SecurityUser adminSec : admins) {
                entity.Utilisateur adminBiz = utilisateurService.findOrCreate(adminSec.getUsername(), adminSec.getRole());
                if (adminBiz != null) {
                    notificationService.notifyUser(adminBiz, "DEMANDE_MODIF_APPROUVEE", 
                        "Demande de modification de " + demande.getUtilisateur().getLibelleUtilisateur() + " approuvée par le directeur. En attente d'exécution.");
                }
            }

            journalService.log(null, "DIRECTOR", "DEMANDE_MODIF_APPROVE", "DemandeModification", demande.getId(),
                "Demande approuvée par le directeur. En attente d'exécution par l'admin.");
        }
    }

    public void rejectRequest(Long demandeId, String commentaire) {
        DemandeModification demande = em.find(DemandeModification.class, demandeId);
        if (demande != null && "EN_ATTENTE".equals(demande.getStatut())) {
            demande.setStatut("REFUSE");
            demande.setDateDecision(Instant.now());
            demande.setCommentaire(commentaire);
            
            // Notify User
            notificationService.notifyUser(demande.getUtilisateur(), "DEMANDE_MODIF_REFUSE", 
                "Votre demande de changement de " + demande.getChamp() + " a été refusée : " + commentaire);
            
            journalService.log(null, "DIRECTOR", "DEMANDE_MODIF_REJECT", "DemandeModification", demande.getId(),
                "Demande refusée par le directeur.");
        }
    }

    public void executeRequest(Long demandeId) {
        DemandeModification demande = em.find(DemandeModification.class, demandeId);
        if (demande != null && "EN_COURS".equals(demande.getStatut())) {
            Utilisateur user = demande.getUtilisateur();
            
            if ("nom".equals(demande.getChamp())) {
                user.setLibelleUtilisateur(demande.getNouvelleVal());
            } else if ("email".equals(demande.getChamp())) {
                user.setEmailUtilisateur(demande.getNouvelleVal());
            }
            
            utilisateurService.save(user);
            
            demande.setStatut("EFFECTUE");
            demande.setDateDecision(Instant.now());
            
            // Notify User and Director
            notificationService.notifyUser(user, "DEMANDE_MODIF_COMPLETE", 
                "Votre " + demande.getChamp() + " a été mis à jour avec succès.");
            
            journalService.log(null, "ADMIN", "DEMANDE_MODIF_EXECUTE", "DemandeModification", demande.getId(),
                "Changement appliqué en base de données par l'administrateur.");
        }
    }

    public List<DemandeModification> findAll() {
        return em.createQuery("SELECT d FROM DemandeModification d ORDER BY d.dateDemande DESC", DemandeModification.class)
                .getResultList();
    }

    public List<DemandeModification> findByUser(Utilisateur user) {
        return em.createQuery("SELECT d FROM DemandeModification d WHERE d.utilisateur = :u ORDER BY d.dateDemande DESC", 
                DemandeModification.class)
                .setParameter("u", user)
                .getResultList();
    }
    
    public long countPending() {
        return em.createQuery("SELECT COUNT(d) FROM DemandeModification d WHERE d.statut = 'EN_ATTENTE'", Long.class)
                .getSingleResult();
    }

    public long countInCours() {
        return em.createQuery("SELECT COUNT(d) FROM DemandeModification d WHERE d.statut = 'EN_COURS'", Long.class)
                .getSingleResult();
    }
}
