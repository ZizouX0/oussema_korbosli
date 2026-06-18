package service;

import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class ObjectifService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<ObjectifService> findAll() {
        return em.createQuery("SELECT o FROM Objectif o ORDER BY o.skAgence", ObjectifService.class)
                .getResultList();
    }

    public List<ObjectifService> findByAgence(Long skAgence) {
        return em.createQuery(
                        "SELECT o FROM Objectif o WHERE o.skAgence = :agence",
                        ObjectifService.class)
                .setParameter("agence", skAgence)
                .getResultList();
    }

    public List<ObjectifService> findByGestionnaire(Long skGestionnaire) {
        return em.createQuery(
                        "SELECT o FROM Objectif o WHERE o.skGestionnaire = :gest",
                        ObjectifService.class)
                .setParameter("gest", skGestionnaire)
                .getResultList();
    }

    public long countTotal() {
        return em.createQuery("SELECT COUNT(o) FROM Objectif o", Long.class).getSingleResult();
    }
}