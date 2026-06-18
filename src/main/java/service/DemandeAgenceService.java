package service;

import entity.DemandeAgence;
import entity.Utilisateur;
import jakarta.ejb.Stateless;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.time.Instant;
import java.util.List;

@Stateless
public class DemandeAgenceService {

    @PersistenceContext(unitName = "default")
    private EntityManager em;

    public DemandeAgence createDemande(Utilisateur directeur,
                                       String codeAgence,
                                       String nomAgence,
                                       String adresse,
                                       List<Utilisateur> utilisateurs) {

        DemandeAgence demande = new DemandeAgence();
        demande.setDirecteur(directeur);
        demande.setTypeDemande("CREATION_AGENCE");
        demande.setStatut("EN_ATTENTE");
        demande.setCodeAgencePropose(codeAgence);
        demande.setNomAgencePropose(nomAgence);
        demande.setAdresseProposee(adresse);
        demande.setDateCreation(Instant.now());
        demande.setUtilisateursDemandes(utilisateurs);

        em.persist(demande);
        return demande;
    }

    public List<DemandeAgence> findByDirecteur(Utilisateur directeur) {
        return em.createQuery("SELECT d FROM DemandeAgence d WHERE d.directeur = :dir ORDER BY d.dateCreation DESC",
                        DemandeAgence.class)
                .setParameter("dir", directeur)
                .getResultList();
    }

    public DemandeAgence findById(Long id) {
        return em.find(DemandeAgence.class, id);
    }

    public List<DemandeAgence> findEnAttente() {
        return em.createQuery("SELECT d FROM DemandeAgence d WHERE d.statut = :statut ORDER BY d.dateCreation",
                        DemandeAgence.class)
                .setParameter("statut", "EN_ATTENTE")
                .getResultList();
    }

    public DemandeAgence save(DemandeAgence demande) {
        return em.merge(demande);
    }
}

