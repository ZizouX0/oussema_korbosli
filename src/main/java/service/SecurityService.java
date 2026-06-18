package service;

import entity.SecurityUser;
import jakarta.ejb.Singleton;
import jakarta.ejb.Startup;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import java.util.List;

@Singleton
@Startup
public class SecurityService {

    @PersistenceContext
    private EntityManager em;

    public void save(SecurityUser user) {
        if (user.getId() == null) {
            em.persist(user);
        } else {
            em.merge(user);
        }
    }

    public SecurityUser authenticate(String username, String password) {
        TypedQuery<SecurityUser> query = em.createQuery(
                "SELECT s FROM SecurityUser s WHERE s.username = :username AND s.password = :password",
                SecurityUser.class);
        query.setParameter("username", username);
        query.setParameter("password", password);

        List<SecurityUser> results = query.getResultList();
        
        // Plus de valeurs codées en dur pour la sécurité : on vérifie uniquement la DB
        return results.isEmpty() ? null : results.get(0);
    }

    public List<SecurityUser> findAllAdmins() {
        return em.createQuery("SELECT s FROM SecurityUser s WHERE s.role = 'ADMIN'", SecurityUser.class)
                .getResultList();
    }

    public List<SecurityUser> findAllDirectors() {
        return em.createQuery("SELECT s FROM SecurityUser s WHERE s.role = 'DIRECTEUR_COMMERCIAL'", SecurityUser.class)
                .getResultList();
    }
}
