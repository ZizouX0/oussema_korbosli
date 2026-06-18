package controller;

import entity.Agence;
import entity.Banque;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.BanqueService;

import java.io.IOException;
import java.util.List;

@WebServlet("/banques")
public class BanqueServlet extends HttpServlet {

    @EJB
    private BanqueService banqueService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        // Toujours charger les agences (La table B_BANQUE n'existe pas dans votre BD)
        // List<Banque> banques = banqueService.findAll(); 
        List<Agence> agences = banqueService.findAllAgences();
        request.setAttribute("agences", agences);

        String banqueIdStr = request.getParameter("banqueId");
        String agenceIdStr = request.getParameter("agenceId");

        if (banqueIdStr != null && !banqueIdStr.isEmpty()) {
            request.setAttribute("selectedBanqueId", Long.valueOf(banqueIdStr));
        }

        if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            Long agenceId = Long.valueOf(agenceIdStr);
            request.setAttribute("selectedAgenceId", agenceId);
            List<Utilisateur> utilisateurs = banqueService.findUtilisateursByAgence(agenceId);
            request.setAttribute("utilisateurs", utilisateurs);
        }

        request.getRequestDispatcher("/WEB-INF/banques.jsp")
                .forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null
                || !"ADMIN".equals(session.getAttribute("role"))) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String action = request.getParameter("action");

        if ("create".equals(action)) {
            Banque banque = new Banque();
            banque.setCode(request.getParameter("code"));
            banque.setNom(request.getParameter("nom"));
            banque.setObjectif(request.getParameter("objectif"));
            banque.setSecteur(request.getParameter("secteur"));
            banqueService.create(banque);

        } else if ("delete".equals(action)) {
            String idStr = request.getParameter("id");
            if (idStr != null && !idStr.isEmpty()) {
                banqueService.delete(Long.valueOf(idStr));
            }
        }

        response.sendRedirect(request.getContextPath() + "/banques");
    }
}