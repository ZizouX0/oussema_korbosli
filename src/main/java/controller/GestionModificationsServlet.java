package controller;

import entity.DemandeModification;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.DemandeModificationService;

import java.io.IOException;
import java.util.List;

@WebServlet("/gestion-demandes")
public class GestionModificationsServlet extends HttpServlet {

    @EJB
    private DemandeModificationService demandeModificationService;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String role = (String) session.getAttribute("role");
        if (!"ADMIN".equals(role) && !"DIRECTEUR_COMMERCIAL".equals(role)) {
            response.sendRedirect(request.getContextPath() + "/home");
            return;
        }

        List<DemandeModification> toutes = demandeModificationService.findAll();
        request.setAttribute("demandes", toutes);
        
        request.getRequestDispatcher("/WEB-INF/gestion-demandes.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect(request.getContextPath() + "/index.jsp");
            return;
        }

        String role = (String) session.getAttribute("role");
        String action = request.getParameter("action");
        String idStr = request.getParameter("id");
        
        if (idStr == null || action == null) {
            response.sendRedirect(request.getContextPath() + "/gestion-demandes");
            return;
        }

        Long id = Long.valueOf(idStr);

        try {
            if ("approve".equals(action) && "DIRECTEUR_COMMERCIAL".equals(role)) {
                String comment = request.getParameter("commentaire");
                demandeModificationService.approveRequest(id, comment);
            } else if ("reject".equals(action) && "DIRECTEUR_COMMERCIAL".equals(role)) {
                String comment = request.getParameter("commentaire");
                demandeModificationService.rejectRequest(id, comment);
            } else if ("execute".equals(action) && "ADMIN".equals(role)) {
                demandeModificationService.executeRequest(id);
            } else {
                throw new Exception("Action non autorisée pour votre rôle.");
            }
            
            response.sendRedirect(request.getContextPath() + "/gestion-demandes?success=1");
        } catch (Exception e) {
            request.setAttribute("error", e.getMessage());
            doGet(request, response);
        }
    }
}
