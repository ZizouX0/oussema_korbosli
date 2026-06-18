<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Gestionnaires</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="gestionnaires" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Gestionnaires</h1>
                <p>Liste des gestionnaires et employés BTK Bank — Total : ${totalGestionnaires}</p>
            </div>

            <!-- STATS -->
            <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px,1fr)); gap:1rem; margin-bottom:2rem;" class="fade-up">
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; font-weight:700; color:var(--btk-accent);">${totalGestionnaires}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Total employés</div>
                </div>
                <div class="card" style="text-align:center;">
                    <div style="font-size:2rem; font-weight:700; color:var(--success);">49</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px;">Agences</div>
                </div>
            </div>

            <!-- ACTIONS & QUICK ADD -->
            <div class="fade-up" style="margin-bottom: 2rem;">
                <details class="glass-collapse">
                    <summary class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 0.5rem; cursor: pointer; list-style: none;">
                        <span style="font-size: 1.2rem; line-height: 1;">+</span> Ajouter un gestionnaire
                    </summary>
                    <div class="form-card" style="margin-top: 1rem; border: 1px solid var(--btk-accent);">
                        <form method="post" action="${pageContext.request.contextPath}/gestionnaires">
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.25rem;">
                                <div class="form-group">
                                    <label class="form-label">Identifiant (SK)</label>
                                    <input type="number" name="id" class="form-control" required placeholder="ex: 1001"/>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Nom Complet</label>
                                    <input type="text" name="nomComplet" class="form-control" required placeholder="ex: Jean Dupont"/>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Email</label>
                                    <input type="email" name="email" class="form-control" required placeholder="ex: jean@btk.tn"/>
                                </div>
                                <div class="form-group">
                                    <label class="form-label">Agence (SK)</label>
                                    <input type="number" name="agenceId" class="form-control" placeholder="ex: 4"/>
                                </div>
                            </div>
                            <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                                <button type="submit" class="btn btn-primary">Enregistrer le gestionnaire</button>
                            </div>
                        </form>
                    </div>
                </details>
            </div>

            <!-- SEARCH -->
            <div class="form-card fade-up" style="margin-bottom:1.5rem;">
                <form method="get" action="${pageContext.request.contextPath}/gestionnaires">
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-end;">
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:200px;">
                            <label class="form-label">Filtrer par agence (SK)</label>
                            <input type="number" name="agenceId" class="form-control"
                                   placeholder="ex: 4"
                                   value="${selectedAgenceId}"/>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">Filtrer</button>
                        <a href="${pageContext.request.contextPath}/gestionnaires" class="btn btn-outline">
                            Tout afficher
                        </a>
                    </div>
                </form>
            </div>

            <!-- TABLE -->
            <div class="fade-up">
                <c:choose>
                    <c:when test="${empty gestionnaires}">
                        <div class="empty-state">
                            <span class="icon">GR</span>
                            <p>Aucun gestionnaire trouvé.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom complet</th>
                                    <th>Email</th>
                                    <th>Rôle</th>
                                    <th>Agence</th>
                                    <th>Statut</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="g" items="${gestionnaires}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${g.id}</td>
                                        <td>${g.nomComplet}</td>
                                        <td style="color:var(--text-muted); font-size:0.8rem;">${g.email}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${g.estGestionnaire == 1}">
                                                    <span class="status status-approuvee">Gestionnaire</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span class="status status-en_attente">Employé</span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td>Agence ${g.skAgence}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${g.estSuspendu == 1}">
                                                    <span class="status status-refusee">Suspendu</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span class="status status-approuvee">Actif</span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>
                                    </tr>
                                </c:forEach>
                                </tbody>
                            </table>
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
