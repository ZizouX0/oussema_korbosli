package service;

import entity.DemandeEmploye;
import entity.Utilisateur;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.time.Instant;
import java.util.List;

@Stateless
public class DemandeEmployeService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public DemandeEmploye submitRequest(Utilisateur directeur, String nom, String prenom, 
                                       String email, String matricule, Long skAgence, Double rolePrevu) {
        DemandeEmploye demande = new DemandeEmploye();
        demande.setDirecteur(directeur);
        demande.setNom(nom);
        demande.setPrenom(prenom);
        demande.setEmail(email);
        demande.setMatricule(matricule);
        demande.setSkAgence(skAgence);
        demande.setRolePrevu(rolePrevu);
        demande.setDateCreation(Instant.now());
        demande.setStatut("EN_ATTENTE");
        
        em.persist(demande);
        return demande;
    }

    public List<DemandeEmploye> findEnAttente() {
        return em.createQuery("SELECT d FROM DemandeEmploye d WHERE d.statut = 'EN_ATTENTE' ORDER BY d.dateCreation DESC", 
                DemandeEmploye.class).getResultList();
    }

    public DemandeEmploye findById(Long id) {
        return em.find(DemandeEmploye.class, id);
    }

    public void save(DemandeEmploye demande) {
        if (demande.getId() == null) {
            em.persist(demande);
        } else {
            em.merge(demande);
        }
    }

    public long countEnAttente() {
        return em.createQuery("SELECT COUNT(d) FROM DemandeEmploye d WHERE d.statut = 'EN_ATTENTE'", Long.class)
                .getSingleResult();
    }
}
