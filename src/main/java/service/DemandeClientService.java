package service;

import entity.DemandeClient;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.util.List;

@Stateless
public class DemandeClientService {

    @PersistenceContext
    private EntityManager em;

    public void save(DemandeClient demande) {
        if (demande.getId() == null) {
            em.persist(demande);
        } else {
            em.merge(demande);
        }
    }

    public List<DemandeClient> findAllPending() {
        return em.createQuery("SELECT d FROM DemandeClient d WHERE d.statut = 'EN_ATTENTE' ORDER BY d.dateCreation DESC", DemandeClient.class)
                .getResultList();
    }

    public DemandeClient findById(Long id) {
        return em.find(DemandeClient.class, id);
    }

    public void delete(Long id) {
        DemandeClient d = findById(id);
        if (d != null) {
            em.remove(d);
        }
    }

    public long countPending() {
        return em.createQuery("SELECT COUNT(d) FROM DemandeClient d WHERE d.statut = 'EN_ATTENTE'", Long.class)
                .getSingleResult();
    }
}
