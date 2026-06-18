<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Gestion des Demandes</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>

<div class="app-layout">
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="manage_requests" />
    </jsp:include>

    <main class="main-wrapper">
        <jsp:include page="top-bar.jsp" />
        <div class="container" style="padding-top: 1.5rem;">
            <div class="page-header fade-up">
                <h1>Validation des Modifications</h1>
                <p>Cycle d'approbation et d'exécution des changements de données employés</p>
            </div>

            <div class="section-label-accent fade-up">File d'attente des demandes</div>
            
            <div class="fade-up">
                <c:choose>
                    <c:when test="${empty demandes}">
                        <div class="card" style="padding: 4rem; text-align: center; opacity: 0.6;">
                            <i data-lucide="check-circle-2" style="width: 48px; height: 48px; margin-bottom: 1rem; color: var(--success);"></i>
                            <p>Toutes les demandes ont été traitées. Félicitations !</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                            <c:forEach var="d" items="${demandes}">
                                <div class="card" style="padding: 1.5rem; display: grid; grid-template-columns: auto 1fr auto; gap: 2rem; align-items: center;">
                                    
                                    <!-- USER ICON -->
                                    <div style="width: 50px; height: 50px; background: var(--btk-accent-soft); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--btk-accent);">
                                        <i data-lucide="user"></i>
                                    </div>

                                    <!-- INFO -->
                                    <div>
                                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                                            <span style="font-weight: 700; font-size: 1.1rem;">${d.utilisateur.libelleUtilisateur}</span>
                                            <span class="status-badge ${d.statut == 'EN_ATTENTE' ? 'status-en_attente' : 
                                                                         d.statut == 'EN_COURS' ? 'status-hors' : 
                                                                         d.statut == 'EFFECTUE' ? 'status-approuvee' : 'status-refusee'}">
                                                ${d.statut}
                                            </span>
                                        </div>
                                        <div style="font-size: 0.9rem; color: var(--text-light);">
                                            <c:choose>
                                                <c:when test="${d.champ == 'feature'}">
                                                    <i data-lucide="lightbulb" style="width: 16px; color: var(--warning); vertical-align: middle; margin-right: 0.5rem;"></i>
                                                    Suggestion : <strong style="color: var(--white); font-style: italic;">"${d.nouvelleVal}"</strong>
                                                </c:when>
                                                <c:otherwise>
                                                    Changement de <strong style="color: var(--btk-accent);">${d.champ == 'nom' ? 'Nom' : 'Email'}</strong> : 
                                                    <span style="text-decoration: line-through; opacity: 0.6; margin-left: 0.5rem;">${d.ancienneVal}</span>
                                                    <i data-lucide="arrow-right" style="width: 14px; margin: 0 0.5rem; vertical-align: middle;"></i>
                                                    <strong style="color: var(--success);">${d.nouvelleVal}</strong>
                                                </c:otherwise>
                                            </c:choose>
                                        </div>
                                        <div style="margin-top: 0.75rem; font-size: 0.75rem; color: var(--text-muted);">
                                            Soumis le ${d.dateDemande}
                                        </div>
                                        <c:if test="${not empty d.commentaire}">
                                            <div style="margin-top: 1rem; font-style: italic; font-size: 0.8rem; color: var(--warning);">
                                                Note : ${d.commentaire}
                                            </div>
                                        </c:if>
                                    </div>

                                    <!-- ACTIONS -->
                                    <div style="display: flex; gap: 0.75rem;">
                                        <!-- DIRECTOR ACTIONS (Approve/Reject) -->
                                        <c:if test="${sessionScope.role == 'DIRECTEUR_COMMERCIAL' && d.statut == 'EN_ATTENTE'}">
                                            <form action="${pageContext.request.contextPath}/gestion-demandes" method="post" style="display: flex; gap: 0.5rem;">
                                                <input type="hidden" name="id" value="${d.id}">
                                                <input type="text" name="commentaire" placeholder="Commentaire..." class="form-control" style="width: 150px; font-size: 0.8rem; padding: 0.4rem 0.75rem;">
                                                <button type="submit" name="action" value="approve" class="btn btn-primary" style="padding: 0.5rem 1rem; background: var(--success);">Approver</button>
                                                <button type="submit" name="action" value="reject" class="btn btn-outline" style="padding: 0.5rem 1rem; border-color: var(--danger); color: var(--danger);">Refuser</button>
                                            </form>
                                        </c:if>

                                        <c:if test="${sessionScope.role == 'ADMIN' && d.statut == 'EN_COURS'}">
                                            <form action="${pageContext.request.contextPath}/gestion-demandes" method="post">
                                                <input type="hidden" name="id" value="${d.id}">
                                                <input type="hidden" name="action" value="execute">
                                                <button type="submit" class="btn btn-primary" style="padding: 0.5rem 1.5rem; background: ${d.champ == 'feature' ? 'var(--btk-accent)' : 'var(--success)'};">
                                                    ${d.champ == 'feature' ? 'Planifier / Terminer' : 'Appliquer le changement'}
                                                </button>
                                            </form>
                                        </c:if>

                                        <c:if test="${d.statut == 'EFFECTUE'}">
                                            <div style="color: var(--success); display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600;">
                                                <i data-lucide="check"></i> Terminé
                                            </div>
                                        </c:if>
                                        <c:if test="${d.statut == 'REFUSE'}">
                                            <div style="color: var(--danger); display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600;">
                                                <i data-lucide="x"></i> Refusé
                                            </div>
                                        </c:if>
                                    </div>

                                </div>
                            </c:forEach>
                        </div>
                    </c:otherwise>
                </c:choose>
            </div>

            <c:if test="${not empty error}">
                <div class="alert alert-error fade-up" style="margin-top: 2rem;">${error}</div>
            </c:if>
        </div>
    </main>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>
</body>
</html>
