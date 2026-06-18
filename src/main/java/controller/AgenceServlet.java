package controller;

import entity.Agence;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.AgenceService;
import service.JournalService;

import java.io.IOException;
import java.util.List;

@WebServlet("/agences")
public class AgenceServlet extends HttpServlet {

    @EJB
    private AgenceService agenceService;

    @EJB
    private JournalService journalService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null
                || session.getAttribute("user") == null
                || !"ADMIN".equals(session.getAttribute("role"))) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        List<Agence> agences = agenceService.findAll();
        request.setAttribute("agences", agences);
        request.getRequestDispatcher("/WEB-INF/agences.jsp")
                .forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null
                || session.getAttribute("user") == null
                || !"ADMIN".equals(session.getAttribute("role"))) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String action = request.getParameter("action");
        if (action == null || action.isEmpty()) {
            action = "create";
        }

        Long userId = (Long) session.getAttribute("userId");
        String role = (String) session.getAttribute("role");

        if ("create".equals(action)) {
            String code = request.getParameter("code");
            String nom = request.getParameter("nom");
            String adresse = request.getParameter("adresse");

            Agence agence = new Agence();
            // agence.setCode(code); // Supprimé : n'existe pas en BD
            agence.setNom(nom);
            agence.setAdresse(adresse);

            agenceService.create(agence);
            journalService.log(userId, role,
                    "CREATE_AGENCE", "AGENCE", agence.getId(),
                    "Création agence nom=" + nom);

        } else if ("delete".equals(action)) {
            String idStr = request.getParameter("id");
            if (idStr != null && !idStr.isEmpty()) {
                Long id = Long.valueOf(idStr);
                agenceService.delete(id);
                journalService.log(userId, role,
                        "DELETE_AGENCE", "AGENCE", id,
                        "Suppression agence id=" + id);
            }
        }

        response.sendRedirect(request.getContextPath() + "/agences");
    }
}

