package filter;

import jakarta.ejb.EJB;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import service.DemandeClientService;
import service.DemandeEmployeService;
import java.io.IOException;

@WebFilter("/*")
public class NotificationFilter implements Filter {

    @EJB
    private DemandeClientService demandeClientService;

    @EJB
    private DemandeEmployeService demandeEmployeService;

    @EJB
    private service.DemandeModificationService demandeModificationService;

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpSession session = httpRequest.getSession(false);

        if (session != null) {
            String role = (String) session.getAttribute("role");
            if ("ADMIN".equals(role)) {
                request.setAttribute("pendingClientDemandes", demandeClientService.countPending());
                request.setAttribute("pendingEmployeDemandes", demandeEmployeService.countEnAttente());
                request.setAttribute("approvedModifs", demandeModificationService.countInCours());
            } else if ("DIRECTEUR_COMMERCIAL".equals(role)) {
                request.setAttribute("pendingModifs", demandeModificationService.countPending());
            }
        }

        chain.doFilter(request, response);
    }
}
