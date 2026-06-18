package controller;

import entity.BClient;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.BClientService;

import java.io.IOException;
import java.util.List;

@WebServlet("/clients-btk")
public class BClientServlet extends HttpServlet {

    @EJB
    private BClientService clientService;

    @EJB
    private service.JournalService journalService;

    @EJB
    private service.DemandeClientService demandeClientService;

    @EJB
    private service.UtilisateurService utilisateurService;

    @EJB
    private service.SecurityService securityService;

    @EJB
    private service.NotificationService notificationService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String keyword = request.getParameter("keyword");
        String agenceIdStr = request.getParameter("agenceId");
        String pageStr = request.getParameter("page");
        int page = (pageStr != null && !pageStr.isEmpty()) ? Integer.parseInt(pageStr) : 1;

        List<BClient> clients;

        if (keyword != null && !keyword.trim().isEmpty()) {
            clients = clientService.search(keyword.trim());
            request.setAttribute("keyword", keyword);
        } else if (agenceIdStr != null && !agenceIdStr.isEmpty()) {
            Long agenceId = Long.valueOf(agenceIdStr);
            clients = clientService.findByAgence(agenceId);
            request.setAttribute("selectedAgenceId", agenceId);
        } else {
            clients = clientService.findAll(page, 50);
        }

        request.setAttribute("clients", clients);
        request.setAttribute("currentPage", page);
        request.setAttribute("totalClients", clientService.countTotal());
        request.setAttribute("totalParticuliers", clientService.countByType("Particulier"));
        request.setAttribute("totalSocietes", clientService.countByType("Société"));
        request.getRequestDispatcher("/WEB-INF/clients-btk.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String action = request.getParameter("action");
        String role = (String) session.getAttribute("role");
        Long userId = (Long) session.getAttribute("userId");

        try {
            if ("ADMIN".equals(role)) {
                // Direct creation for Admin
                BClient client = new BClient();
                client.setNomClient(request.getParameter("nom").toUpperCase());
                client.setPrenomClient(request.getParameter("prenom"));
                client.setTypeClient(request.getParameter("type"));
                client.setStatutClient("ACTIF");

                String agId = request.getParameter("agenceId");
                if (agId != null && !agId.isEmpty()) {
                    client.setSkAgence(Long.valueOf(agId));
                }

                clientService.save(client);

                journalService.log(userId, role, "CREATE_CLIENT", "B_CLIENTS", client.getId(),
                        "Ajout direct du client: " + client.getNomClient() + " " + client.getPrenomClient());

                response.sendRedirect(request.getContextPath() + "/clients-btk?success=1");
            } else {
                // Demand for other roles (Directeur, etc.)
                entity.DemandeClient demande = new entity.DemandeClient();
                demande.setNomClient(request.getParameter("nom").toUpperCase());
                demande.setPrenomClient(request.getParameter("prenom"));
                demande.setTypeClient(request.getParameter("type"));
                demande.setDirecteur(utilisateurService.findById(userId));
                demande.setDateCreation(java.time.Instant.now());

                String agId = request.getParameter("agenceId");
                if (agId != null && !agId.isEmpty()) {
                    demande.setSkAgence(Long.valueOf(agId));
                }

                demandeClientService.save(demande);

                // Notify director
                notificationService.notifyUser(demande.getDirecteur(),
                        "DEMANDE_CLIENT_CREEE",
                        "Votre demande de création de client " + demande.getPrenomClient() + " " + demande.getNomClient() + " a été créée.");

                // Notify all Admins
                List<entity.SecurityUser> admins = securityService.findAllAdmins();
                for (entity.SecurityUser adminSec : admins) {
                    entity.Utilisateur adminBiz = utilisateurService.findOrCreate(adminSec.getUsername(), adminSec.getRole());
                    if (adminBiz != null) {
                        notificationService.notifyUser(adminBiz, "DEMANDE_CLIENT", 
                            "Nouvelle demande de création de client " + demande.getPrenomClient() + " " + demande.getNomClient() + " par " + demande.getDirecteur().getLibelleUtilisateur());
                    }
                }

                journalService.log(userId, role, "REQUEST_CLIENT", "DEMANDE_CLIENT", demande.getId(),
                        "Demande de création de client: " + demande.getNomClient() + " " + demande.getPrenomClient());

                response.sendRedirect(request.getContextPath() + "/clients-btk?pending=1");
            }
            return;
        } catch (Exception e) {
            request.setAttribute("error", "Erreur: " + e.getMessage());
            doGet(request, response);
        }
    }
}