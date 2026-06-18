package service;

import entity.BClient;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class BClientService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<BClient> findAll(int page, int size) {
        return em.createQuery("SELECT c FROM BClient c ORDER BY c.nomClient", BClient.class)
                .setFirstResult((page - 1) * size)
                .setMaxResults(size)
                .getResultList();
    }

    public List<BClient> findByAgence(Long skAgence) {
        return em.createQuery(
                        "SELECT c FROM BClient c WHERE c.skAgence = :agence ORDER BY c.nomClient",
                        BClient.class)
                .setParameter("agence", skAgence)
                .setMaxResults(100)
                .getResultList();
    }

    public List<BClient> findByGestionnaire(Long skGestionnaire) {
        return em.createQuery(
                        "SELECT c FROM BClient c WHERE c.skGestionnaire = :gest ORDER BY c.nomClient",
                        BClient.class)
                .setParameter("gest", skGestionnaire)
                .setMaxResults(100)
                .getResultList();
    }

    public List<BClient> search(String keyword) {
        String kw = "%" + keyword.toUpperCase() + "%";
        return em.createQuery(
                        "SELECT c FROM BClient c WHERE UPPER(c.nomClient) LIKE :kw OR UPPER(c.prenomClient) LIKE :kw ORDER BY c.nomClient",
                        BClient.class)
                .setParameter("kw", kw)
                .setMaxResults(50)
                .getResultList();
    }

    public long countTotal() {
        return em.createQuery("SELECT COUNT(c) FROM BClient c", Long.class).getSingleResult();
    }

    public long countByType(String type) {
        return em.createQuery("SELECT COUNT(c) FROM BClient c WHERE c.typeClient = :type", Long.class)
                .setParameter("type", type).getSingleResult();
    }

    public long countByAgence(Long skAgence) {
        return em.createQuery("SELECT COUNT(c) FROM BClient c WHERE c.skAgence = :agence", Long.class)
                .setParameter("agence", skAgence).getSingleResult();
    }

    public void save(BClient client) {
        if (client.getId() == null) {
            em.persist(client);
        } else {
            em.merge(client);
        }
    }
}