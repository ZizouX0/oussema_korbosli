package controller;

import entity.Utilisateur;
import jakarta.ejb.EJB;
import service.UtilisateurService;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.logging.Logger;

@WebServlet("/forgot-password")
public class ForgotPasswordServlet extends HttpServlet {

    private static final Logger LOGGER = Logger.getLogger(ForgotPasswordServlet.class.getName());

    @EJB
    private UtilisateurService utilisateurService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.getRequestDispatcher("/forgot-password.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String identifier = request.getParameter("identifier");

        if (identifier == null || identifier.trim().isEmpty()) {
            request.setAttribute("error", "Veuillez entrer un identifiant ou un email.");
            request.getRequestDispatcher("/forgot-password.jsp").forward(request, response);
            return;
        }

        Utilisateur utilisateur = utilisateurService.findByLogin(identifier);
        
        // Simuler la recherche par email si l'identifiant ne correspond pas
        if (utilisateur == null) {
            // Dans un système réel, on filtrerait par email dans le service
            LOGGER.info("Tentative de récupération pour : " + identifier);
        }

        if (utilisateur != null || "admin".equals(identifier) || "directeur".equals(identifier)) {
            // On simule le succès pour les comptes connus ou existants
            request.setAttribute("success", "Un email de récupération a été envoyé à l'adresse associée à ce compte.");
            LOGGER.info("Demande de récupération de mot de passe réussie pour : " + identifier);
        } else {
            request.setAttribute("error", "Aucun compte trouvé pour cet identifiant.");
            LOGGER.warning("Échec de récupération de mot de passe pour : " + identifier);
        }

        request.getRequestDispatcher("/forgot-password.jsp").forward(request, response);
    }
}
