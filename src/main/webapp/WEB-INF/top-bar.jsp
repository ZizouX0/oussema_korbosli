<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<header class="navbar" style="position: sticky; top: 0; background: rgba(0, 26, 61, 0.8); backdrop-filter: blur(20px); border-bottom: 1px solid var(--glass-border); z-index: 900; margin-bottom: 0;">
    <div style="flex: 1; display: flex; align-items: center; padding-left: 2rem;">
        <!-- You can add a breadcrumb here if needed -->
    </div>
    <div class="navbar-actions" style="display: flex; gap: 1.5rem; align-items: center; padding-right: 2rem;">
        <c:if test="${sessionScope.role == 'ADMIN' || sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
            <div class="notification-wrapper" style="position: relative;">
                <c:set var="notifCount" value="${sessionScope.role == 'ADMIN' ? (pendingClientDemandes + pendingEmployeDemandes + approvedModifs) : pendingModifs}" />
                <c:set var="notifLink" value="${sessionScope.role == 'ADMIN' ? 'demandes-admin' : 'gestion-demandes'}" />
                
                <a href="${pageContext.request.contextPath}/${notifLink}" style="color: var(--white); text-decoration: none; display: flex; align-items: center; gap: 0.5rem;" title="Actions en attente">
                    <i data-lucide="bell" style="width: 20px; height: 20px;"></i>
                    <c:if test="${notifCount > 0}">
                        <span class="badge" style="position: absolute; top: -8px; right: -8px; background: var(--danger); color: white; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 700; border: 2px solid var(--btk-blue-deep); box-shadow: 0 0 10px rgba(255, 94, 87, 0.4);">
                            ${notifCount}
                        </span>
                    </c:if>
                </a>
            </div>
        </c:if>
        
        <div style="width: 1px; height: 24px; background: var(--glass-border);"></div>
        
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <div style="text-align: right;">
                <div style="font-size: 0.8rem; font-weight: 600; color: var(--white);">${sessionScope.user}</div>
                <div style="font-size: 0.65rem; color: var(--btk-accent); text-transform: uppercase; letter-spacing: 0.5px;">${sessionScope.role}</div>
            </div>
        </div>
    </div>
</header>
