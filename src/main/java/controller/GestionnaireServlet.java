package controller;

import entity.Gestionnaire;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.GestionnaireService;

import java.io.IOException;
import java.util.List;

@WebServlet("/gestionnaires")
public class GestionnaireServlet extends HttpServlet {

    @EJB
    private GestionnaireService gestionnaireService;

    @EJB
    private service.JournalService journalService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String role = (String) session.getAttribute("role");
        String agenceIdStr = request.getParameter("agenceId");

        List<Gestionnaire> gestionnaires;
        if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            gestionnaires = gestionnaireService.findByAgence(Long.valueOf(agenceIdStr));
            request.setAttribute("selectedAgenceId", Long.valueOf(agenceIdStr));
        } else if ("ADMIN".equals(role)) {
            gestionnaires = gestionnaireService.findAll();
        } else {
            gestionnaires = gestionnaireService.findGestionnairesOnly();
        }

        request.setAttribute("gestionnaires", gestionnaires);
        request.setAttribute("totalGestionnaires", gestionnaireService.countTotal());
        request.getRequestDispatcher("/WEB-INF/gestionnaires.jsp").forward(request, response);
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
            Gestionnaire gest = new Gestionnaire();
            gest.setId(Long.valueOf(request.getParameter("id"))); // Matricule as ID
            gest.setNomComplet(request.getParameter("nomComplet"));
            gest.setEmail(request.getParameter("email"));
            gest.setEstGestionnaire(1);
            gest.setEstSuspendu(0);

            String agId = request.getParameter("agenceId");
            if (agId != null && !agId.isEmpty()) {
                gest.setSkAgence(Long.valueOf(agId));
            }

            gestionnaireService.save(gest);

            // LOG ACTION
            journalService.log(
                (Long) session.getAttribute("userId"),
                (String) session.getAttribute("role"),
                "CREATE_MANAGER",
                "GESTIONNAIRE",
                gest.getId(),
                "Création du gestionnaire: " + gest.getNomComplet()
            );

        } catch (Exception e) {
            request.setAttribute("error", "Erreur lors de la création du gestionnaire: " + e.getMessage());
        }

        response.sendRedirect(request.getContextPath() + "/gestionnaires");
    }
}