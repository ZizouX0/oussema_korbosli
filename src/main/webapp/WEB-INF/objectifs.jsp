<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Objectifs Commerciaux</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="objectifs" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Objectifs Commerciaux</h1>
                <p>Suivi des objectifs par agence et gestionnaire</p>
            </div>

            <!-- FILTER -->
            <div class="form-card fade-up" style="margin-bottom:1.5rem;">
                <form method="get" action="${pageContext.request.contextPath}/objectifs">
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-end;">
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:150px;">
                            <label class="form-label">Agence (SK)</label>
                            <input type="number" name="agenceId" class="form-control"
                                   placeholder="ex: 4" value="${selectedAgenceId}"/>
                        </div>
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:150px;">
                            <label class="form-label">Gestionnaire (SK)</label>
                            <input type="number" name="gestionnaireId" class="form-control"
                                   placeholder="ex: 76" value="${selectedGestionnaireId}"/>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">
                            Filtrer
                        </button>
                        <a href="${pageContext.request.contextPath}/objectifs" class="btn btn-outline">
                            Tout afficher
                        </a>
                    </div>
                </form>
            </div>

            <!-- TABLE -->
            <div class="fade-up">
                <c:choose>
                    <c:when test="${empty objectifs}">
                        <div class="empty-state">
                            <span class="icon">OB</span>
                            <p>Aucun objectif trouvé.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>Agence</th>
                                    <th>Gestionnaire</th>
                                    <th>Situation</th>
                                    <th>EER Particulier</th>
                                    <th>EER Hors Part.</th>
                                    <th>Cpt Chèques</th>
                                    <th>Cpt Épargnes</th>
                                    <th>Crédits Conso</th>
                                    <th>Crédits Immo</th>
                                    <th>Période</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="o" items="${objectifs}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">Agence ${o.skAgence}</td>
                                        <td>Gest. ${o.skGestionnaire}</td>
                                        <td>
                                            <span class="status status-approuvee">${o.situationAdministrative}</span>
                                        </td>
                                        <td>${o.eerParticulier}</td>
                                        <td>${o.eerHorsParticulier}</td>
                                        <td>${o.souscriptionCompteCheques}</td>
                                        <td>${o.souscriptionCompteEpargnes}</td>
                                        <td style="color:var(--success);">${o.productionCreditsConso}</td>
                                        <td style="color:var(--success);">${o.productionCreditsImmo}</td>
                                        <td style="color:var(--text-muted);">${o.anneeMois}</td>
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
