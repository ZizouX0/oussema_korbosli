package controller;

import entity.DemandeAgence;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.DemandeAgenceService;
import service.DemandeEmployeService;
import service.JournalService;
import service.NotificationService;
import service.UtilisateurService;
import entity.DemandeEmploye;
import entity.DemandeClient;
import entity.Utilisateur;
import entity.BClient;
import service.BClientService;
import service.DemandeClientService;

import java.io.IOException;
import java.time.Instant;
import java.util.List;

@WebServlet("/demandes-admin")
public class DemandeAgenceAdminServlet extends HttpServlet {

    @EJB
    private DemandeAgenceService demandeAgenceService;

    @EJB
    private NotificationService notificationService;

    @EJB
    private JournalService journalService;

    @EJB
    private DemandeEmployeService demandeEmployeService;

    @EJB
    private UtilisateurService utilisateurService;

    @EJB
    private DemandeClientService demandeClientService;

    @EJB
    private BClientService bClientService;

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

        List<DemandeAgence> demandes = demandeAgenceService.findEnAttente();
        request.setAttribute("demandes", demandes);

        List<DemandeEmploye> demandesEmployes = demandeEmployeService.findEnAttente();
        request.setAttribute("demandesEmployes", demandesEmployes);

        List<DemandeClient> demandesClients = demandeClientService.findAllPending();
        request.setAttribute("demandesClients", demandesClients);

        request.getRequestDispatcher("/WEB-INF/demandes-admin.jsp")
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
        String idStr = request.getParameter("id");

        if (idStr != null && !idStr.isEmpty() && action != null) {
            Long id = Long.valueOf(idStr);
            DemandeAgence demande = demandeAgenceService.findById(id);

            Long userId = (Long) session.getAttribute("userId");
            String role = (String) session.getAttribute("role");

            if (demande != null) {
                if ("approve".equals(action)) {
                    demande.setStatut("APPROUVEE");
                    demande.setDateDecision(Instant.now());
                    demandeAgenceService.save(demande);

                    notificationService.notifyUser(
                            demande.getDirecteur(),
                            "DEMANDE_AGENCE_VALIDEE",
                            "Votre demande d'agence " + demande.getCodeAgencePropose() + " a été approuvée."
                    );

                    journalService.log(userId, role,
                            "APPROVE_DEMANDE_AGENCE", "DEMANDE_AGENCE", demande.getId(),
                            "Approbation de la demande d'agence code=" + demande.getCodeAgencePropose());

                } else if ("refuse".equals(action)) {
                    String commentaire = request.getParameter("commentaire");
                    demande.setStatut("REFUSEE");
                    demande.setDateDecision(Instant.now());
                    demande.setCommentaireAdmin(commentaire);
                    demandeAgenceService.save(demande);

                    notificationService.notifyUser(
                            demande.getDirecteur(),
                            "DEMANDE_AGENCE_REFUSEE",
                            "Votre demande d'agence " + demande.getCodeAgencePropose() + " a été refusée."
                    );

                    journalService.log(userId, role,
                            "REFUSE_DEMANDE_AGENCE", "DEMANDE_AGENCE", demande.getId(),
                            "Refus de la demande d'agence code=" + demande.getCodeAgencePropose()
                                    + " commentaire=" + commentaire);
                }
            }
        }

        // EMPLOYEE REQUESTS
        String actionEmp = request.getParameter("actionEmp");
        String idEmpStr = request.getParameter("idEmp");

        if (idEmpStr != null && !idEmpStr.isEmpty() && actionEmp != null) {
            Long idEmp = Long.valueOf(idEmpStr);
            DemandeEmploye de = demandeEmployeService.findById(idEmp);
            Long userId = (Long) session.getAttribute("userId");
            String role = (String) session.getAttribute("role");

            if (de != null && "EN_ATTENTE".equals(de.getStatut())) {
                if ("approve".equals(actionEmp)) {
                    de.setStatut("APPROUVEE");
                    demandeEmployeService.save(de);

                    // Actually create the user
                    Utilisateur u = new Utilisateur();
                    u.setLibelleUtilisateur(de.getPrenom() + " " + de.getNom());
                    u.setEmailUtilisateur(de.getEmail());
                    u.setEstGestionnaire(de.getRolePrevu());
                    u.setSkAgence(de.getSkAgence());
                    u.setEstSuspendu(0);
                    utilisateurService.save(u);

                    notificationService.notifyUser(de.getDirecteur(), "DEMANDE_EMPLOYE_VALIDEE",
                            "L'employé " + de.getPrenom() + " " + de.getNom() + " a été validé.");

                    journalService.log(userId, role, "APPROVE_DEMANDE_EMPLOYE", "DEMANDE_EMPLOYE", de.getId(),
                            "Validation de l'employé " + de.getPrenom() + " " + de.getNom());

                } else if ("refuse".equals(actionEmp)) {
                    String commentaire = request.getParameter("commentaire");
                    de.setStatut("REFUSEE");
                    de.setCommentaireAdmin(commentaire);
                    demandeEmployeService.save(de);

                    notificationService.notifyUser(de.getDirecteur(), "DEMANDE_EMPLOYE_REFUSEE",
                            "La demande pour " + de.getPrenom() + " " + de.getNom() + " a été refusée.");

                    journalService.log(userId, role, "REFUSE_DEMANDE_EMPLOYE", "DEMANDE_EMPLOYE", de.getId(),
                            "Refus de l'employé " + de.getPrenom() + " " + de.getNom());
                }
            }
        }

        // CLIENT REQUESTS
        String actionCli = request.getParameter("actionCli");
        String idCliStr = request.getParameter("idCli");

        if (idCliStr != null && !idCliStr.isEmpty() && actionCli != null) {
            Long idCli = Long.valueOf(idCliStr);
            DemandeClient dc = demandeClientService.findById(idCli);
            Long userId = (Long) session.getAttribute("userId");
            String role = (String) session.getAttribute("role");

            if (dc != null && "EN_ATTENTE".equals(dc.getStatut())) {
                if ("approve".equals(actionCli)) {
                    dc.setStatut("APPROUVEE");
                    demandeClientService.save(dc);

                    // Actually create the client
                    BClient client = new BClient();
                    client.setNomClient(dc.getNomClient());
                    client.setPrenomClient(dc.getPrenomClient());
                    client.setTypeClient(dc.getTypeClient());
                    client.setSexe(dc.getSexe());
                    client.setSkAgence(dc.getSkAgence());
                    client.setSkGestionnaire(dc.getSkGestionnaire());
                    client.setStatutClient("ACTIF");
                    bClientService.save(client);

                    notificationService.notifyUser(dc.getDirecteur(), "DEMANDE_CLIENT_VALIDEE",
                            "Le client " + dc.getPrenomClient() + " " + dc.getNomClient() + " a été validé.");

                    journalService.log(userId, role, "APPROVE_DEMANDE_CLIENT", "DEMANDE_CLIENT", dc.getId(),
                            "Validation du client " + dc.getPrenomClient() + " " + dc.getNomClient());

                } else if ("refuse".equals(actionCli)) {
                    String commentaire = request.getParameter("commentaire");
                    dc.setStatut("REFUSEE");
                    dc.setCommentaireAdmin(commentaire);
                    demandeClientService.save(dc);

                    notificationService.notifyUser(dc.getDirecteur(), "DEMANDE_CLIENT_REFUSEE",
                            "La demande pour le client " + dc.getPrenomClient() + " " + dc.getNomClient() + " a été refusée.");

                    journalService.log(userId, role, "REFUSE_DEMANDE_CLIENT", "DEMANDE_CLIENT", dc.getId(),
                            "Refus du client " + dc.getPrenomClient() + " " + dc.getNomClient());
                }
            }
        }

        response.sendRedirect(request.getContextPath() + "/demandes-admin");
    }
}

    