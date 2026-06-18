package service;

import entity.Client;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class ClientService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<Client> findAll(int page, int size) {
        return em.createQuery("SELECT c FROM Client c ORDER BY c.nomClient", Client.class)
                .setFirstResult((page - 1) * size)
                .setMaxResults(size)
                .getResultList();
    }

    public List<Client> findByAgence(Long skAgence) {
        return em.createQuery("SELECT c FROM Client c WHERE c.skAgence = :agence ORDER BY c.nomClient", Client.class)
                .setParameter("agence", skAgence)
                .setMaxResults(100)
                .getResultList();
    }

    public List<Client> findByGestionnaire(Long skGestionnaire) {
        return em.createQuery("SELECT c FROM Client c WHERE c.skGestionnaire = :gest ORDER BY c.nomClient", Client.class)
                .setParameter("gest", skGestionnaire)
                .setMaxResults(100)
                .getResultList();
    }

    public List<Client> search(String keyword) {
        String kw = "%" + keyword.toUpperCase() + "%";
        return em.createQuery("SELECT c FROM Client c WHERE UPPER(c.nomClient) LIKE :kw OR UPPER(c.prenomClient) LIKE :kw ORDER BY c.nomClient", Client.class)
                .setParameter("kw", kw)
                .setMaxResults(50)
                .getResultList();
    }

    public long countTotal() {
        return em.createQuery("SELECT COUNT(c) FROM Client c", Long.class).getSingleResult();
    }

    public long countByAgence(Long skAgence) {
        return em.createQuery("SELECT COUNT(c) FROM Client c WHERE c.skAgence = :agence", Long.class)
                .setParameter("agence", skAgence).getSingleResult();
    }

    public long countByType(String type) {
        return em.createQuery("SELECT COUNT(c) FROM Client c WHERE c.typeClient = :type", Long.class)
                .setParameter("type", type).getSingleResult();
    }
}