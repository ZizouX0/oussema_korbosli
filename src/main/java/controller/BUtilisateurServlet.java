package controller;

import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.UtilisateurService;

import java.io.IOException;
import java.util.List;

@WebServlet("/employes")
public class BUtilisateurServlet extends HttpServlet {

    @EJB
    private UtilisateurService utilisateurService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String agenceIdStr = request.getParameter("agenceId");
        String roleFilter = request.getParameter("roleFilter");

        List<Utilisateur> employes;

        if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            Long agenceId = Long.valueOf(agenceIdStr);
            if ("gestionnaire".equals(roleFilter)) {
                employes = utilisateurService.findGestionnairesByAgence(agenceId);
            } else {
                employes = utilisateurService.findByAgence(agenceId);
            }
            request.setAttribute("selectedAgenceId", agenceId);
        } else if ("gestionnaire".equals(roleFilter)) {
            employes = utilisateurService.findGestionnaires();
        } else if ("conseiller".equals(roleFilter)) {
            employes = utilisateurService.findConseillers();
        } else if ("hors_commercial".equals(roleFilter)) {
            employes = utilisateurService.findHorsCommercial();
        } else {
            employes = utilisateurService.findAll();
        }

        request.setAttribute("employes", employes);
        request.setAttribute("totalEmployes", utilisateurService.countTotal());
        request.setAttribute("totalGestionnaires", utilisateurService.countGestionnaires());
        request.setAttribute("totalConseillers", utilisateurService.countConseillers());
        request.setAttribute("totalHorsCommercial", utilisateurService.countHorsCommercial());
        request.setAttribute("roleFilter", roleFilter);
        request.getRequestDispatcher("/WEB-INF/employes.jsp").forward(request, response);
    }
}