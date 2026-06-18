package controller;

import entity.DemandeModification;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.DemandeModificationService;
import service.UtilisateurService;

import java.io.IOException;
import java.util.List;

@WebServlet("/mes-demandes")
public class MesDemandesServlet extends HttpServlet {

    @EJB
    private DemandeModificationService demandeModificationService;

    @EJB
    private UtilisateurService utilisateurService;

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

        Long userId = (Long) session.getAttribute("userId");
        Utilisateur user = utilisateurService.findById(userId);
        
        List<DemandeModification> demandes = demandeModificationService.findByUser(user);
        request.setAttribute("demandes", demandes);
        request.setAttribute("userProfile", user);
        
        request.getRequestDispatcher("/WEB-INF/profil.jsp").forward(request, response);
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
            Long userId = (Long) session.getAttribute("userId");
            Utilisateur user = utilisateurService.findById(userId);
            
            String champ = request.getParameter("champ");
            String nouvelleVal = request.getParameter("nouvelleVal");
            
            if (champ == null || nouvelleVal == null || nouvelleVal.trim().isEmpty()) {
                throw new Exception("Veuillez remplir tous les champs.");
            }
            
            demandeModificationService.submitRequest(user, champ, nouvelleVal);
            
            // Notify all Directors
            List<entity.SecurityUser> directors = securityService.findAllDirectors();
            String typeLabel = "feature".equals(champ) ? "suggestion de fonctionnalité" : "demande de modification";
            String msg = "Nouvelle " + typeLabel + " par " + user.getLibelleUtilisateur();
            
            for (entity.SecurityUser dirSec : directors) {
                entity.Utilisateur dirBiz = utilisateurService.findByLogin(dirSec.getUsername());
                if (dirBiz != null) {
                    notificationService.notifyUser(dirBiz, "DEMANDE_MODIF", msg);
                }
            }
            
            response.sendRedirect(request.getContextPath() + "/mes-demandes?success=1");
        } catch (Exception e) {
            request.setAttribute("error", e.getMessage());
            doGet(request, response);
        }
    }
}
