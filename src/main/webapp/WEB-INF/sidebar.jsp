<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<aside class="sidebar">
    <div class="sidebar-header">
        <a href="${pageContext.request.contextPath}/home" style="text-decoration: none;">
            <h1 class="navbar-brand"><span>BTK</span> BANK</h1>
            <p style="color:var(--text-muted); font-size:0.65rem; margin-top:0.2rem; letter-spacing:1px; text-transform:uppercase;">Gestion Agences</p>
        </a>
    </div>

    <nav class="sidebar-nav">
        <div class="nav-label">Menu Principal</div>
        <a href="${pageContext.request.contextPath}/home" class="nav-item ${activePage == 'dashboard' ? 'active' : ''}">
            <i data-lucide="layout-dashboard"></i>
            <span>Tableau de Bord</span>
        </a>

        <div class="nav-label">Ressources</div>
        <a href="${pageContext.request.contextPath}/employes" class="nav-item ${activePage == 'employes' ? 'active' : ''}">
            <i data-lucide="users"></i>
            <span>Employés</span>
        </a>
        <a href="${pageContext.request.contextPath}/pointage" class="nav-item ${activePage == 'pointage' ? 'active' : ''}">
            <i data-lucide="clock"></i>
            <span>Pointage</span>
        </a>
        <c:if test="${sessionScope.role == 'ADMIN' || sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
            <a href="${pageContext.request.contextPath}/clients-btk" class="nav-item ${activePage == 'clients' ? 'active' : ''}">
                <i data-lucide="user-check"></i>
                <span>Clients BTK</span>
            </a>
            <a href="${pageContext.request.contextPath}/banques" class="nav-item ${activePage == 'agences_btk' ? 'active' : ''}">
                <i data-lucide="building-2"></i>
                <span>Agences</span>
            </a>

            <div class="nav-label">Performance</div>
            <a href="${pageContext.request.contextPath}/objectifs-btk" class="nav-item ${activePage == 'objectifs' ? 'active' : ''}">
                <i data-lucide="trending-up"></i>
                <span>Objectifs</span>
            </a>
        </c:if>

        <div class="nav-label">Opérations</div>
        <a href="${pageContext.request.contextPath}/demandes-agence" class="nav-item ${activePage == 'mes_demandes' ? 'active' : ''}">
            <i data-lucide="file-text"></i>
            <span>Mes Demandes</span>
        </a>
        <a href="${pageContext.request.contextPath}/mes-demandes" class="nav-item ${activePage == 'profile' ? 'active' : ''}">
            <i data-lucide="user"></i>
            <span>Mon Profil</span>
        </a>

        <c:if test="${sessionScope.role == 'ADMIN' || sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
            <div class="nav-label">Administration</div>
            <c:if test="${sessionScope.role == 'ADMIN'}">
                <a href="${pageContext.request.contextPath}/agences" class="nav-item ${activePage == 'admin_agences' ? 'active' : ''}">
                    <i data-lucide="settings"></i>
                    <span>Gérer les Agences</span>
                </a>
            </c:if>
            <a href="${pageContext.request.contextPath}/demandes-admin" class="nav-item ${activePage == 'admin_demandes' ? 'active' : ''}">
                <i data-lucide="check-square"></i>
                <span>Valider Demandes</span>
            </a>
            <a href="${pageContext.request.contextPath}/gestion-demandes" class="nav-item ${activePage == 'manage_requests' ? 'active' : ''}">
                <i data-lucide="edit-3"></i>
                <span>Modifications Profil</span>
            </a>
        </c:if>
    </nav>

    <div class="sidebar-footer">
        <div class="user-profile-mini">
            <div class="user-avatar">${sessionScope.user.substring(0,1).toUpperCase()}</div>
            <div class="user-info-text">
                <span class="name">${sessionScope.user}</span>
                <span class="role">${sessionScope.role}</span>
            </div>
            <a href="${pageContext.request.contextPath}/logout" style="color:var(--text-muted); transition: color 0.2s;" title="Déconnexion">
                <i data-lucide="log-out" style="width:18px;"></i>
            </a>
        </div>
    </div>
</aside>
