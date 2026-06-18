package controller;

import entity.DemandeAgence;
import entity.Notification;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.DemandeAgenceService;
import service.JournalService;
import service.NotificationService;
import service.UtilisateurService;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/demandes-agence")
public class DemandeAgenceServlet extends HttpServlet {

    @EJB
    private DemandeAgenceService demandeAgenceService;

    @EJB
    private NotificationService notificationService;

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private JournalService journalService;

    @EJB
    private service.SecurityService securityService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String userRole = (String) session.getAttribute("role");
        if (!"DIRECTEUR_COMMERCIAL".equals(userRole) && !"ADMIN".equals(userRole)) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        Long userId = (Long) session.getAttribute("userId");
        Utilisateur directeur = utilisateurService.findById(userId);

        List<DemandeAgence> demandes = demandeAgenceService.findByDirecteur(directeur);
        List<Utilisateur> utilisateurs = utilisateurService.findAll();
        List<Notification> notifications = notificationService.findUnread(directeur);

        request.setAttribute("demandes", demandes);
        request.setAttribute("utilisateurs", utilisateurs);
        request.setAttribute("notifications", notifications);

        request.getRequestDispatcher("/WEB-INF/demandes-agence.jsp")
                .forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String userRole = (String) session.getAttribute("role");
        if (!"DIRECTEUR_COMMERCIAL".equals(userRole) && !"ADMIN".equals(userRole)) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        Long userId = (Long) session.getAttribute("userId");
        String role = (String) session.getAttribute("role");
        Utilisateur directeur = utilisateurService.findById(userId);

        String code = request.getParameter("code");
        String nom = request.getParameter("nom");
        String adresse = request.getParameter("adresse");

        String[] utilisateurIds = request.getParameterValues("utilisateurIds");
        List<Utilisateur> utilisateurs = new ArrayList<>();
        if (utilisateurIds != null) {
            for (String idStr : utilisateurIds) {
                if (idStr != null && !idStr.isEmpty()) {
                    Long id = Long.valueOf(idStr);
                    Utilisateur u = utilisateurService.findById(id);
                    if (u != null) {
                        utilisateurs.add(u);
                    }
                }
            }
        }

        DemandeAgence demande = demandeAgenceService.createDemande(
                directeur, code, nom, adresse, utilisateurs
        );

        notificationService.notifyUser(directeur,
                "DEMANDE_AGENCE_CREEE",
                "Votre demande d'agence " + code + " a été créée.");

        // Send Notifications to all Admins
        List<entity.SecurityUser> admins = securityService.findAllAdmins();
        for (entity.SecurityUser adminSec : admins) {
            entity.Utilisateur adminBiz = utilisateurService.findOrCreate(adminSec.getUsername(), adminSec.getRole());
            if (adminBiz != null) {
                notificationService.notifyUser(adminBiz, "DEMANDE_AGENCE", 
                    "Nouvelle demande d'ouverture d'agence " + code + " par " + directeur.getLibelleUtilisateur());
            }
        }

        journalService.log(userId, role,
                "CREATE_DEMANDE_AGENCE", "DEMANDE_AGENCE", demande.getId(),
                "Création demande agence code=" + code);

        response.sendRedirect(request.getContextPath() + "/demandes-agence");
    }
}
