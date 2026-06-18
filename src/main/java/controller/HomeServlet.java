package controller;

import java.io.IOException;
import java.util.List;
import entity.JournalAction;
import jakarta.ejb.EJB;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import service.UtilisateurService;
import service.JournalService;

@WebServlet("/home")
public class HomeServlet extends HttpServlet {

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private JournalService journalService;

    @EJB
    private service.BClientService clientService;

    @EJB
    private service.DemandeClientService demandeClientService;

    @EJB
    private service.DemandeEmployeService demandeEmployeService;

    @EJB
    private service.DemandeModificationService demandeModificationService;

    @Override
    protected void doGet(HttpServletRequest request,
                         HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);

        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        // Employee Stats
        request.setAttribute("totalEmployes", utilisateurService.countTotal());
        request.setAttribute("totalGestionnaires", utilisateurService.countGestionnaires());
        request.setAttribute("totalConseillers", utilisateurService.countConseillers());
        request.setAttribute("totalHorsCommercial", utilisateurService.countHorsCommercial());

        // Client Stats
        request.setAttribute("totalClients", clientService.countTotal());
        request.setAttribute("totalParticuliers", clientService.countByType("Particulier"));
        request.setAttribute("totalSocietes", clientService.countByType("Société"));

        // Demandes Stats
        request.setAttribute("pendingClientDemandes", demandeClientService.countPending());
        request.setAttribute("pendingEmployeDemandes", demandeEmployeService.countEnAttente());
        request.setAttribute("pendingModifs", demandeModificationService.countPending());
        request.setAttribute("approvedModifs", demandeModificationService.countInCours());

        // Recent Activity Feed
        List<JournalAction> recentActions = journalService.findRecent(5);
        request.setAttribute("recentActions", recentActions);

        // Chart Data: Employees by Agency
        List<Object[]> agencyStats = utilisateurService.getEmployeeCountByAgency();
        StringBuilder agencyNames = new StringBuilder();
        StringBuilder agencyCounts = new StringBuilder();
        for (int i = 0; i < agencyStats.size(); i++) {
            Object[] row = agencyStats.get(i);
            String name = row[0] != null ? row[0].toString() : "Inconnue";
            agencyNames.append("'").append(name).append("'");
            agencyCounts.append(row[1].toString());
            if (i < agencyStats.size() - 1) {
                agencyNames.append(",");
                agencyCounts.append(",");
            }
        }
        request.setAttribute("chartAgencyLabels", agencyNames.toString());
        request.setAttribute("chartAgencyData", agencyCounts.toString());

        // Chart Data: Role Distribution
        java.util.Map<String, Long> roleStats = utilisateurService.getRoleDistribution();
        request.setAttribute("chartRoleLabels", "'Gestionnaires','Conseillers','Hors Com.'");
        request.setAttribute("chartRoleData", 
            roleStats.get("Gestionnaires") + "," + 
            roleStats.get("Conseillers") + "," + 
            roleStats.get("Hors Commercial"));

        // Chart Data: Growth (Mock for demo since no dates in DB)
        request.setAttribute("chartGrowthLabels", "'Jan','Feb','Mar','Apr','May','Jun'");
        request.setAttribute("chartGrowthData", "12,19,25,32,45,58");

        request.getRequestDispatcher("/WEB-INF/home.jsp")
                .forward(request, response);
    }
}