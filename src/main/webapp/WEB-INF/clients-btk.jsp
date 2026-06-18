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
        <jsp:include page="top-bar.jsp" />
        <div class="container" style="padding-top: 1.5rem;">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Clients BTK Bank</h1>
                <p>Gestion et suivi des clients</p>
            </div>

            <c:if test="${param.success == 1}">
                <div class="alert alert-success fade-up" style="max-width: 600px; margin: 0 auto 1.5rem; text-align: center;">
                    Client enregistré avec succès.
                </div>
            </c:if>
            <c:if test="${param.pending == 1}">
                <div class="alert fade-up" style="max-width: 600px; margin: 0 auto 1.5rem; text-align: center; background: rgba(0,150,214,0.1); border: 1px solid var(--btk-accent); color: var(--btk-accent);">
                    Demande d'ajout de client soumise. En attente de validation par l'administrateur.
                </div>
            </c:if>

            <c:if test="${sessionScope.role == 'ADMIN'}">
            <!-- SLIM QUICK ADD -->
            <div class="fade-up" style="margin-bottom: 2.5rem; display: flex; justify-content: center;">
                <div class="search-bar" style="max-width: 1100px; padding: 0.75rem 1.25rem; border-radius: 12px; background: rgba(0,150,214,0.05); border: 1px dashed rgba(0,150,214,0.2);">
                    <form method="post" action="${pageContext.request.contextPath}/clients-btk" style="width: 100%;">
                        <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
                            
                            <div style="display: flex; align-items: center; gap: 0.5rem; color: var(--btk-accent); margin-right: 0.5rem; border-right: 1px solid rgba(255,255,255,0.1); padding-right: 1rem;">
                                <i data-lucide="user-plus" style="width: 18px; height: 18px;"></i>
                                <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; white-space: nowrap;">Ajout Rapide</span>
                            </div>

                            <input type="text" name="nom" class="form-control" style="flex: 2; min-width: 130px; padding: 0.5rem 0.8rem; height: 38px;" placeholder="Nom du client" required/>
                            <input type="text" name="prenom" class="form-control" style="flex: 2; min-width: 130px; padding: 0.5rem 0.8rem; height: 38px;" placeholder="Prénom" required/>
                            
                            <select name="type" class="form-control" style="flex: 1.5; min-width: 120px; padding: 0.5rem 0.8rem; height: 38px;">
                                <option value="Particulier">Particulier</option>
                                <option value="Société">Société</option>
                            </select>
                            
                            <input type="number" name="agenceId" class="form-control" style="flex: 1; min-width: 90px; padding: 0.5rem 0.8rem; height: 38px;" placeholder="Code Agence"/>

                            <button type="submit" class="btn btn-primary" style="padding: 0 1.5rem; height: 38px; display: flex; align-items: center; gap: 0.5rem; font-weight: 600;">
                                <i data-lucide="plus-circle" style="width: 16px; height: 16px;"></i>
                                Enregistrer
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            </c:if>

            <!-- SEARCH -->
            <div class="form-card fade-up" style="margin-bottom:1.5rem;">
                <form method="get" action="${pageContext.request.contextPath}/clients-btk">
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-end;">
                        <div class="form-group" style="margin-bottom:0; flex:2; min-width:200px;">
                            <label class="form-label">Rechercher</label>
                            <input type="text" name="keyword" class="form-control"
                                   placeholder="Nom ou prénom..." value="${keyword}"/>
                        </div>
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:130px;">
                            <label class="form-label">Agence (SK)</label>
                            <input type="number" name="agenceId" class="form-control"
                                   placeholder="ex: 4" value="${selectedAgenceId}"/>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">Rechercher</button>
                        <a href="${pageContext.request.contextPath}/clients-btk" class="btn btn-outline">Réinitialiser</a>
                    </div>
                </form>
            </div>

            <!-- TABLE -->
            <div class="fade-up">
                <div style="display:flex; justify-content:center; align-items:center; margin-bottom:1.5rem; gap: 1.5rem;">
                    <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted);">
                        Liste des clients
                    </h3>
                    <span style="font-size:0.8rem; color:var(--btk-accent); background:rgba(0,150,214,0.1); border:1px solid var(--border); padding:3px 10px; border-radius:20px;">
                        ${clients.size()} résultats
                    </span>
                </div>
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
                                                    <span class="status">${c.typeClient}</span>
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
                        <div style="display:flex; justify-content:center; gap:0.5rem; margin-top:1.5rem; align-items:center;">
                            <c:if test="${currentPage > 1}">
                                <a href="${pageContext.request.contextPath}/clients-btk?page=${currentPage - 1}" class="btn btn-outline">Précédent</a>
                            </c:if>
                            <span style="color:var(--text-muted); font-size:0.85rem; padding:0 0.5rem;">Page ${currentPage}</span>
                            <a href="${pageContext.request.contextPath}/clients-btk?page=${currentPage + 1}" class="btn btn-outline">Suivant</a>
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

