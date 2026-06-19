package controller;

import entity.Pointage;
import entity.Utilisateur;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.PointageService;
import service.UtilisateurService;
import service.JournalService;

import java.io.IOException;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@WebServlet("/pointage")
public class PointageServlet extends HttpServlet {

    @EJB
    private PointageService pointageService;

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private JournalService journalService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        Long userId = (Long) session.getAttribute("userId");
        String role = (String) session.getAttribute("role");

        request.setAttribute("pointageDuJour", pointageService.findTodayByUser(userId));
        request.setAttribute("pointages", pointageService.findRecent(50));
        request.setAttribute("presentsAujourdhui", pointageService.countPresentsToday());

        if ("ADMIN".equals(role)) {
            List<Utilisateur> employes = utilisateurService.findAll();
            request.setAttribute("employes", employes);
        }

        request.getRequestDispatcher("/WEB-INF/pointage.jsp")
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

        Long userId = (Long) session.getAttribute("userId");
        String role = (String) session.getAttribute("role");
        String action = request.getParameter("action");
        if (action == null) action = "";

        switch (action) {
            case "arrivee":
                pointageService.pointerArrivee(userId);
                journalService.log(userId, role, "POINTAGE_ARRIVEE", "Pointage", null,
                        "Pointage d'arrivée");
                break;
            case "depart":
                pointageService.pointerDepart(userId);
                journalService.log(userId, role, "POINTAGE_DEPART", "Pointage", null,
                        "Pointage de départ");
                break;
            case "manuel":
                if ("ADMIN".equals(role)) {
                    enregistrerManuel(request);
                    journalService.log(userId, role, "POINTAGE_MANUEL", "Pointage", null,
                            "Saisie / correction manuelle d'un pointage");
                }
                break;
            default:
                break;
        }

        response.sendRedirect(request.getContextPath() + "/pointage");
    }

    /** Construit et enregistre un pointage à partir du formulaire manuel (admin). */
    private void enregistrerManuel(HttpServletRequest request) {
        String employeId = request.getParameter("employeId");
        String dateStr = request.getParameter("datePointage");
        if (employeId == null || employeId.isEmpty() || dateStr == null || dateStr.isEmpty()) {
            return;
        }

        LocalDate date = LocalDate.parse(dateStr);
        Pointage p = new Pointage();
        p.setEmploye(utilisateurService.findById(Long.valueOf(employeId)));
        p.setDatePointage(date);
        p.setStatut(request.getParameter("statut"));
        p.setCommentaire(request.getParameter("commentaire"));

        String arr = request.getParameter("heureArrivee");
        if (arr != null && !arr.isEmpty()) {
            p.setHeureArrivee(date.atTime(LocalTime.parse(arr)));
        }
        String dep = request.getParameter("heureDepart");
        if (dep != null && !dep.isEmpty()) {
            p.setHeureDepart(date.atTime(LocalTime.parse(dep)));
        }
        pointageService.saveManuel(p);
    }
}
