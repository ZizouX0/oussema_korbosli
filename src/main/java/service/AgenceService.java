package service;

import entity.Agence;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class AgenceService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<Agence> findAll() {
        return em.createQuery("SELECT a FROM Agence a", Agence.class)
                .getResultList();
    }

    public Agence findById(Long id) {
        return em.find(Agence.class, id);
    }

    public void create(Agence agence) {
        em.persist(agence);
    }

    public Agence update(Agence agence) {
        return em.merge(agence);
    }

    public void delete(Long id) {
        Agence agence = em.find(Agence.class, id);
        if (agence != null) {
            em.remove(agence);
        }
    }
}

