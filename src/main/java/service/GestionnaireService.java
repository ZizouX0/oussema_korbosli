package service;

import entity.Gestionnaire;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class GestionnaireService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<Gestionnaire> findAll() {
        return em.createQuery("SELECT g FROM Gestionnaire g ORDER BY g.nomComplet", Gestionnaire.class)
                .getResultList();
    }

    public List<Gestionnaire> findByAgence(Long skAgence) {
        return em.createQuery("SELECT g FROM Gestionnaire g WHERE g.skAgence = :agence ORDER BY g.nomComplet", Gestionnaire.class)
                .setParameter("agence", skAgence)
                .getResultList();
    }

    public List<Gestionnaire> findGestionnairesOnly() {
        return em.createQuery("SELECT g FROM Gestionnaire g WHERE g.estGestionnaire = 1 ORDER BY g.nomComplet", Gestionnaire.class)
                .getResultList();
    }

    public Gestionnaire findById(Long id) {
        return em.find(Gestionnaire.class, id);
    }

    public long countTotal() {
        return em.createQuery("SELECT COUNT(g) FROM Gestionnaire g", Long.class).getSingleResult();
    }

    public long countByAgence(Long skAgence) {
        return em.createQuery("SELECT COUNT(g) FROM Gestionnaire g WHERE g.skAgence = :agence", Long.class)
                .setParameter("agence", skAgence).getSingleResult();
    }

    public void save(Gestionnaire gest) {
        if (gest.getId() == null) {
            em.persist(gest);
        } else {
            em.merge(gest);
        }
    }
}