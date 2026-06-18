package service;

import entity.Agence;
import entity.Banque;
import entity.Utilisateur;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.List;

@Stateless
public class BanqueService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public List<Banque> findAll() {
        return em.createQuery("SELECT b FROM Banque b", Banque.class)
                .getResultList();
    }

    public Banque findById(Long id) {
        return em.find(Banque.class, id);
    }

    public void create(Banque banque) {
        em.persist(banque);
    }

    public Banque update(Banque banque) {
        return em.merge(banque);
    }

    public void delete(Long id) {
        Banque banque = em.find(Banque.class, id);
        if (banque != null) em.remove(banque);
    }

    public List<Agence> findAllAgences() {
        return em.createQuery("SELECT a FROM Agence a", Agence.class)
                .getResultList();
    }

    public List<Utilisateur> findUtilisateursByAgence(Long agenceId) {
        return em.createQuery(
                        "SELECT u FROM Utilisateur u WHERE u.skAgence = :id",
                        Utilisateur.class)
                .setParameter("id", agenceId)
                .getResultList();
    }
}