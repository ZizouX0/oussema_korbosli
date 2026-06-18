package controller;

import entity.Client;
import jakarta.ejb.EJB;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import service.ClientService;

import java.io.IOException;
import java.util.List;

@WebServlet("/clients-old")
public class ClientServlet extends HttpServlet {

    @EJB
    private ClientService clientService;

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

        List<Client> clients;

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
}