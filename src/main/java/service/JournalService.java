package service;

import entity.JournalAction;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.time.Instant;

@Stateless
public class JournalService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    @EJB
    private UtilisateurService utilisateurService;

    public void log(Long userId, String role, String actionCode,
                    String entite, Long idEntite, String details) {

        JournalAction journal = new JournalAction();

        Utilisateur utilisateur = null;
        if (userId != null) {
            utilisateur = utilisateurService.findById(userId);
        }

        journal.setUtilisateur(utilisateur);
        journal.setRole(
                role != null
                        ? role
                        : (utilisateur != null
                        ? (utilisateur.isGestionnaire() ? "GESTIONNAIRE" : "CLIENT")
                        : null)
        );
        journal.setActionCode(actionCode);
        journal.setEntite(entite);
        journal.setIdEntite(idEntite);
        journal.setDateAction(Instant.now());
        journal.setDetails(details);

        em.persist(journal);
    }

    public java.util.List<JournalAction> findRecent(int limit) {
        return em.createQuery("SELECT j FROM JournalAction j ORDER BY j.dateAction DESC", JournalAction.class)
                .setMaxResults(limit)
                .getResultList();
    }
}