<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Clients</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="clients" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Clients BTK Bank</h1>
                <p>Gestion et suivi des clients</p>
            </div>

            <!-- STATS -->
            <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px,1fr)); gap:1rem; margin-bottom:2rem;" class="fade-up">
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; font-weight:700; color:var(--btk-accent);">${totalClients}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Total clients</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; font-weight:700; color:var(--success);">${totalParticuliers}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Particuliers</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; font-weight:700; color:var(--warning);">${totalSocietes}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Sociétés</div>
                </div>
            </div>

            <!-- SEARCH & FILTER -->
            <div class="form-card fade-up" style="margin-bottom:1.5rem;">
                <form method="get" action="${pageContext.request.contextPath}/clients">
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-end;">
                        <div class="form-group" style="margin-bottom:0; flex:2; min-width:200px;">
                            <label class="form-label">Rechercher un client</label>
                            <input type="text" name="keyword" class="form-control"
                                   placeholder="Nom ou prénom..."
                                   value="${keyword}"/>
                        </div>
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:150px;">
                            <label class="form-label">Agence (SK)</label>
                            <input type="number" name="agenceId" class="form-control"
                                   placeholder="ex: 4"
                                   value="${selectedAgenceId}"/>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">
                            Rechercher
                        </button>
                        <a href="${pageContext.request.contextPath}/clients" class="btn btn-outline">
                            Réinitialiser
                        </a>
                    </div>
                </form>
            </div>

            <!-- TABLE -->
            <div class="fade-up">
                <c:choose>
                    <c:when test="${empty clients}">
                        <div class="empty-state">
                            <span class="icon">CL</span>
                            <p>Aucun client trouvé.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom</th>
                                    <th>Prénom</th>
                                    <th>Type</th>
                                    <th>Gouvernorat</th>
                                    <th>Secteur</th>
                                    <th>Profil</th>
                                    <th>Agence</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="c" items="${clients}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${c.id}</td>
                                        <td style="font-weight:500;">${c.nomClient}</td>
                                        <td>${c.prenomClient}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${c.typeClient == 'Particulier'}">
                                                    <span class="status status-approuvee">Particulier</span>
                                                </c:when>
                                                <c:when test="${c.typeClient == 'Société'}">
                                                    <span class="status status-en_attente">Société</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span class="status status-refusee">${c.typeClient}</span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td style="color:var(--text-muted);">${c.gouvernorat}</td>
                                        <td style="color:var(--text-muted); font-size:0.8rem;">${c.secteurActivite}</td>
                                        <td style="color:var(--text-muted); font-size:0.8rem;">${c.libelleProfil}</td>
                                        <td>Agence ${c.skAgence}</td>
                                    </tr>
                                </c:forEach>
                                </tbody>
                            </table>
                        </div>

                        <!-- PAGINATION -->
                        <div style="display:flex; justify-content:center; gap:0.5rem; margin-top:1.5rem;">
                            <c:if test="${currentPage > 1}">
                                <a href="${pageContext.request.contextPath}/clients?page=${currentPage - 1}" class="btn btn-outline">Précédent</a>
                            </c:if>
                            <span style="padding:0.5rem 1rem; color:var(--text-muted); font-size:0.85rem;">
                                Page ${currentPage}
                            </span>
                            <a href="${pageContext.request.contextPath}/clients?page=${currentPage + 1}" class="btn btn-outline">Suivant</a>
                        </div>
                    </c:otherwise>
                </c:choose>
            </div>
        </div>
    </main>
</div>

<!-- LUCIDE ICONS -->
<script src="https://unpkg.com/lucide@latest"></script>
<script>
    lucide.createIcons();
</script>

</body>
</html>
