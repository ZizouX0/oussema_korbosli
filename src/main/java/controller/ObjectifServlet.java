package controller;

import entity.Objectif; // ✅ important
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import service.ObjectifService;

import java.io.IOException;
import java.util.List;

@WebServlet("/objectifs")
public class ObjectifServlet extends HttpServlet {

    @EJB
    private ObjectifService objectifService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String agenceIdStr = request.getParameter("agenceId");
        String gestionnaireIdStr = request.getParameter("gestionnaireId");


        List<ObjectifService> objectifs;

        if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            Long agenceId = Long.parseLong(agenceIdStr);
            objectifs= objectifService.findByAgence(agenceId);
            request.setAttribute("selectedAgenceId", agenceId);

        } else if (gestionnaireIdStr != null && !gestionnaireIdStr.isEmpty()) {
            Long gestionnaireId = Long.parseLong(gestionnaireIdStr);
            objectifs = objectifService.findByGestionnaire(gestionnaireId);
            request.setAttribute("selectedGestionnaireId", gestionnaireId);

        } else {
            objectifs = objectifService.findAll();
        }
        request.setAttribute("objectifs", objectifs);
        request.getRequestDispatcher("/WEB-INF/objectifs.jsp").forward(request, response);
    }
}