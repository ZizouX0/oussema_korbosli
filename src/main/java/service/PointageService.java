package service;

import entity.Pointage;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

/**
 * Logique métier du pointage des employés (présence / arrivée / départ).
 */
@Stateless
public class PointageService {

    /** Heure limite au-delà de laquelle une arrivée est considérée en retard. */
    private static final LocalTime HEURE_LIMITE = LocalTime.of(9, 0);

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    @EJB
    private UtilisateurService utilisateurService;

    /** Pointage d'arrivée d'un employé (bouton « Pointer », heure système). */
    public Pointage pointerArrivee(Long userId) {
        Pointage p = findTodayByUser(userId);
        if (p != null && p.getHeureArrivee() != null) {
            return p; // arrivée déjà enregistrée aujourd'hui
        }
        if (p == null) {
            p = new Pointage();
            p.setEmploye(utilisateurService.findById(userId));
            p.setDatePointage(LocalDate.now());
            p.setSource("AUTO");
        }
        LocalDateTime now = LocalDateTime.now();
        p.setHeureArrivee(now);
        p.setStatut(now.toLocalTime().isAfter(HEURE_LIMITE) ? "RETARD" : "PRESENT");
        if (p.getId() == null) {
            em.persist(p);
        } else {
            em.merge(p);
        }
        return p;
    }

    /** Pointage de départ d'un employé. */
    public Pointage pointerDepart(Long userId) {
        Pointage p = findTodayByUser(userId);
        if (p == null) {
            return null; // pas d'arrivée enregistrée
        }
        p.setHeureDepart(LocalDateTime.now());
        return em.merge(p);
    }

    /** Saisie ou correction manuelle d'un pointage par l'administrateur. */
    public void saveManuel(Pointage p) {
        p.setSource("MANUEL");
        if (p.getId() == null) {
            em.persist(p);
        } else {
            em.merge(p);
        }
    }

    /** Pointage du jour d'un employé (ou null s'il n'a pas encore pointé). */
    public Pointage findTodayByUser(Long userId) {
        List<Pointage> res = em.createQuery(
                "SELECT p FROM Pointage p WHERE p.employe.id = :uid AND p.datePointage = :jour",
                Pointage.class)
                .setParameter("uid", userId)
                .setParameter("jour", LocalDate.now())
                .getResultList();
        return res.isEmpty() ? null : res.get(0);
    }

    public Pointage findById(Long id) {
        return em.find(Pointage.class, id);
    }

    /** Liste des pointages les plus récents. */
    public List<Pointage> findRecent(int limit) {
        return em.createQuery(
                "SELECT p FROM Pointage p ORDER BY p.datePointage DESC, p.heureArrivee DESC",
                Pointage.class)
                .setMaxResults(limit)
                .getResultList();
    }

    /** Pointages d'une date donnée. */
    public List<Pointage> findByDate(LocalDate date) {
        return em.createQuery(
                "SELECT p FROM Pointage p WHERE p.datePointage = :jour ORDER BY p.heureArrivee",
                Pointage.class)
                .setParameter("jour", date)
                .getResultList();
    }

    /** Nombre de pointages d'un statut donné sur une période (pour le BI). */
    public long countByStatutBetween(String statut, LocalDate debut, LocalDate fin) {
        TypedQuery<Long> q = em.createQuery(
                "SELECT COUNT(p) FROM Pointage p WHERE p.statut = :st " +
                "AND p.datePointage BETWEEN :d AND :f", Long.class);
        q.setParameter("st", statut);
        q.setParameter("d", debut);
        q.setParameter("f", fin);
        return q.getSingleResult();
    }

    /** Nombre de présents (présents + retards) du jour. */
    public long countPresentsToday() {
        return em.createQuery(
                "SELECT COUNT(p) FROM Pointage p WHERE p.datePointage = :jour " +
                "AND p.statut IN ('PRESENT','RETARD')", Long.class)
                .setParameter("jour", LocalDate.now())
                .getSingleResult();
    }
}
