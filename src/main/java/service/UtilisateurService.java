package service;

import entity.Utilisateur;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import java.util.List;

@Stateless
public class UtilisateurService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public Utilisateur findById(Long id) {
        return em.find(Utilisateur.class, id);
    }

    public Utilisateur findByLogin(String login) {
        TypedQuery<Utilisateur> query = em.createQuery(
                "SELECT u FROM Utilisateur u WHERE u.libelleUtilisateur = :login", Utilisateur.class);
        query.setParameter("login", login);

        List<Utilisateur> results = query.getResultList();
        return results.isEmpty() ? null : results.get(0);
    }

    public Utilisateur findOrCreate(String login, String role) {
        Utilisateur utilisateur = findByLogin(login);

        if (utilisateur == null) {
            utilisateur = new Utilisateur();
            utilisateur.setLibelleUtilisateur(login);
            utilisateur.setEmailUtilisateur(login + "@mail.com");
            utilisateur.setEstGestionnaire(role.equals("GEST") ? 1.0 : 0.0);
            utilisateur.setEstSuspendu(0);
            em.persist(utilisateur);
        } else {
            utilisateur.setEstGestionnaire(role.equals("GEST") ? 1.0 : 0.0);
            utilisateur = em.merge(utilisateur);
        }
        return utilisateur;
    }

    public List<Utilisateur> findAll() {
        return em.createQuery("SELECT u FROM Utilisateur u", Utilisateur.class).getResultList();
    }

    public List<Utilisateur> findGestionnaires() {
        return em.createQuery("SELECT u FROM Utilisateur u WHERE u.estGestionnaire = 1.0", Utilisateur.class)
                .getResultList();
    }

    public List<Utilisateur> findConseillers() {
        return em.createQuery("SELECT u FROM Utilisateur u WHERE u.estGestionnaire = 0.0 AND (u.skAgence <> 31 AND u.skAgence IS NOT NULL)", Utilisateur.class)
                .getResultList();
    }

    public List<Utilisateur> findHorsCommercial() {
        return em.createQuery("SELECT u FROM Utilisateur u WHERE u.estGestionnaire = 0.0 AND (u.skAgence = 31 OR u.skAgence IS NULL)", Utilisateur.class)
                .getResultList();
    }

    public List<Utilisateur> findByAgence(Long skAgence) {
        return em.createQuery("SELECT u FROM Utilisateur u WHERE u.skAgence = :agence", Utilisateur.class)
                .setParameter("agence", skAgence)
                .getResultList();
    }

    public List<Utilisateur> findGestionnairesByAgence(Long skAgence) {
        return em.createQuery("SELECT u FROM Utilisateur u WHERE u.skAgence = :agence AND u.estGestionnaire = 1.0", Utilisateur.class)
                .setParameter("agence", skAgence)
                .getResultList();
    }

    public long countTotal() {
        return (long) em.createQuery("SELECT COUNT(u) FROM Utilisateur u").getSingleResult();
    }

    public long countGestionnaires() {
        return (long) em.createQuery("SELECT COUNT(u) FROM Utilisateur u WHERE u.estGestionnaire = 1.0").getSingleResult();
    }

    public long countConseillers() {
        return (long) em.createQuery("SELECT COUNT(u) FROM Utilisateur u WHERE u.estGestionnaire = 0.0 AND (u.skAgence <> 31 AND u.skAgence IS NOT NULL)").getSingleResult();
    }

    public long countHorsCommercial() {
        return (long) em.createQuery("SELECT COUNT(u) FROM Utilisateur u WHERE u.estGestionnaire = 0.0 AND (u.skAgence = 31 OR u.skAgence IS NULL)").getSingleResult();
    }

    /**
     * Retourne le nombre d'employés par agence.
     * Utilise une jointure native pour récupérer les noms des agences.
     */
    public java.util.List<Object[]> getEmployeeCountByAgency() {
        String sql = "SELECT a.LIBELLE_AGENCE, COUNT(u.SK_UTILISATEUR) " +
                     "FROM B_UTILISATEURS u " +
                     "LEFT JOIN AGENCE a ON u.SK_AGENCE = a.SK_AGENCE " +
                     "GROUP BY a.LIBELLE_AGENCE " +
                     "ORDER BY COUNT(u.SK_UTILISATEUR) DESC";
        return em.createNativeQuery(sql).getResultList();
    }

    /**
     * Retourne la répartition des rôles.
     */
    public java.util.Map<String, Long> getRoleDistribution() {
        java.util.Map<String, Long> stats = new java.util.HashMap<>();
        stats.put("Gestionnaires", countGestionnaires());
        stats.put("Conseillers", countConseillers());
        stats.put("Hors Commercial", countHorsCommercial());
        return stats;
    }

    public void save(Utilisateur u) {
        if (u.getId() == null) {
            em.persist(u);
        } else {
            em.merge(u);
        }
    }
}