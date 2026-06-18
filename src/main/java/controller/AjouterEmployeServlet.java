package controller;

import entity.Banque;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.BanqueService;
import service.DemandeEmployeService;
import service.UtilisateurService;

import java.io.IOException;
import java.util.List;

@WebServlet("/ajouter-employe")
public class AjouterEmployeServlet extends HttpServlet {

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private service.JournalService journalService;

    @EJB
    private BanqueService banqueService;

    @EJB
    private DemandeEmployeService demandeEmployeService;

    @EJB
    private service.SecurityService securityService;

    @EJB
    private service.NotificationService notificationService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        List<entity.Agence> agences = banqueService.findAllAgences();
        request.setAttribute("banques", agences);
        request.getRequestDispatcher("/WEB-INF/add-effectif.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        try {
            String nom = request.getParameter("nom");
            String prenom = request.getParameter("prenom");
            String email = request.getParameter("email");
            String roleStr = request.getParameter("role");
            String agenceIdStr = request.getParameter("banqueId");

            if (nom == null || nom.isEmpty() || prenom == null || prenom.isEmpty() || agenceIdStr == null || roleStr == null) {
                throw new Exception("Veuillez remplir les champs obligatoires (Nom, Prénom, Agence, Rôle).");
            }

            String roleUser = (String) session.getAttribute("role");
            Long requesterId = (Long) session.getAttribute("userId");
            entity.Utilisateur requester = utilisateurService.findById(requesterId);

            Long agenceId = Long.valueOf(agenceIdStr);
            double roleVal = Double.parseDouble(roleStr);

            if ("ADMIN".equals(roleUser)) {
                // CREATE SYSTEM USER (Utilisateur) DIRECTLY
                entity.Utilisateur u = new entity.Utilisateur();
                u.setLibelleUtilisateur(prenom + " " + nom);
                u.setEmailUtilisateur(email);
                
                // Role logic for direct Admin creation
                if (roleVal == 3.0) { // Hors Commercial
                    u.setEstGestionnaire(0.0);
                    u.setSkAgence(31L);
                } else if (roleVal == 2.0) { // Conseiller
                    u.setEstGestionnaire(0.0);
                    u.setSkAgence(agenceId);
                } else { // Gestionnaire
                    u.setEstGestionnaire(1.0);
                    u.setSkAgence(agenceId);
                }

                u.setEstSuspendu(0);
                utilisateurService.save(u);

                // Log the action
                journalService.log(requesterId, "ADMIN", "CREATION_EMPLOYE", "Utilisateur", u.getId(),
                    "Création directe de l'employé : " + prenom + " " + nom);
                
                response.sendRedirect(request.getContextPath() + "/employes?success=1");
            } else {
                // REGLE METIER : Pas de Conseiller au Siège (31) pour les Directeurs
                if (agenceId == 31 && roleVal == 2.0) {
                    throw new Exception("Incompatibilité : Un 'Conseiller' ne peut pas être affecté au Siège (Agence 31).");
                }

                // SUBMIT REQUEST
                entity.DemandeEmploye demande = demandeEmployeService.submitRequest(
                    requester, nom, prenom, email, 
                    request.getParameter("matricule"), 
                    agenceId, 
                    roleVal
                );

                // Log the action
                journalService.log(requesterId, roleUser, "DEMANDE_EMPLOYE", "DemandeEmploye", demande.getId(),
                    "Soumission d'une demande d'ajout d'employé : " + prenom + " " + nom);

                // Send Notifications to all Admins
                List<entity.SecurityUser> admins = securityService.findAllAdmins();
                for (entity.SecurityUser adminSec : admins) {
                    entity.Utilisateur adminBiz = utilisateurService.findByLogin(adminSec.getUsername());
                    if (adminBiz != null) {
                        notificationService.notifyUser(adminBiz, "DEMANDE_EMPLOYE", 
                            "Nouvelle demande d'employé : " + prenom + " " + nom + " par " + requester.getLibelleUtilisateur());
                    }
                }
                
                response.sendRedirect(request.getContextPath() + "/employes?pending=1");
            }
        } catch (Exception e) {
            Throwable rootCause = e;
            while (rootCause.getCause() != null) {
                rootCause = rootCause.getCause();
            }
            request.setAttribute("error", "Erreur lors de l'ajout : " + rootCause.getMessage());
            doGet(request, response);
        }
    }
}
