package controller;

import entity.Objectif;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.BObjectifService;

import java.io.IOException;
import java.util.List;

@WebServlet("/objectifs-btk")
public class BObjectifServlet extends HttpServlet {

    @EJB
    private BObjectifService objectifService;

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

        List<Objectif> objectifs;

        if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            objectifs = objectifService.findByAgence(Long.valueOf(agenceIdStr));
            request.setAttribute("selectedAgenceId", Long.valueOf(agenceIdStr));
        } else if (gestionnaireIdStr != null && !gestionnaireIdStr.isEmpty()) {
            objectifs = objectifService.findByGestionnaire(Long.valueOf(gestionnaireIdStr));
            request.setAttribute("selectedGestionnaireId", Long.valueOf(gestionnaireIdStr));
        } else {
            objectifs = objectifService.findAll();
        }

        request.setAttribute("objectifs", objectifs);
        request.setAttribute("totalObjectifs", objectifService.countTotal());
        request.getRequestDispatcher("/WEB-INF/objectifs-btk.jsp").forward(request, response);
    }
}