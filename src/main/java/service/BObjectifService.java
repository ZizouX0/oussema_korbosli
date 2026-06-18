package service;

import entity.Objectif;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class BObjectifService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<Objectif> findAll() {
        return em.createQuery("SELECT o FROM Objectif o ORDER BY o.skAgence", Objectif.class)
                .getResultList();
    }

    public List<Objectif> findByAgence(Long skAgence) {
        return em.createQuery(
                        "SELECT o FROM Objectif o WHERE o.skAgence = :agence",
                        Objectif.class)
                .setParameter("agence", skAgence)
                .getResultList();
    }

    public List<Objectif> findByGestionnaire(Long skGestionnaire) {
        return em.createQuery(
                        "SELECT o FROM Objectif o WHERE o.skGestionnaire = :gest",
                        Objectif.class)
                .setParameter("gest", skGestionnaire)
                .getResultList();
    }

    public long countTotal() {
        return em.createQuery("SELECT COUNT(o) FROM Objectif o", Long.class).getSingleResult();
    }
}