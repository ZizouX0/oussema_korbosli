package controller;

import entity.Utilisateur;
import jakarta.ejb.EJB;
import service.UtilisateurService;

import java.io.IOException;
import java.util.logging.Logger;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    private static final Logger LOGGER = Logger.getLogger(LoginServlet.class.getName());

    @EJB
    private service.SecurityService securityService;

    @EJB
    private UtilisateurService utilisateurService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {
        request.getRequestDispatcher("/index.jsp")
                .forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        entity.SecurityUser secUser = securityService.authenticate(username, password);

        if (secUser != null) {
            String role = secUser.getRole();
            // Link to business user (B_UTILISATEURS) to maintain workflow compatibility
            Utilisateur businessUser = utilisateurService.findOrCreate(username, role);

            HttpSession session = request.getSession();
            session.setAttribute("user", username);
            session.setAttribute("role", role);
            session.setAttribute("userId", businessUser.getId());

            LOGGER.info("Authentification sécurisée réussie pour " + username + " [" + role + "]");
            response.sendRedirect(request.getContextPath() + "/home");
        } else {
            LOGGER.warning("Échec d'authentification pour l'utilisateur " + username);
            request.setAttribute("error", "Accès refusé : Identifiants de sécurité invalides");
            request.getRequestDispatcher("/index.jsp")
                    .forward(request, response);
        }
    }
}