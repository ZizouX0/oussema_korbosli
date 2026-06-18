<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Demandes d'agence</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="mes_demandes" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Demandes d'agence</h1>
                <p>Soumettre et suivre vos demandes d'ouverture d'agence</p>
            </div>

            <!-- FORM - only for DIRECTEUR_COMMERCIAL -->
            <c:if test="${sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
                <div class="form-card fade-up" style="margin-bottom:2.5rem;">
                    <h3 style="font-family:'Playfair Display',serif; color:var(--btk-accent); margin-bottom:1.5rem;">
                        Nouvelle demande
                    </h3>
                    <form method="post" action="${pageContext.request.contextPath}/demandes-agence">
                        <div class="form-group">
                            <label class="form-label">Code agence proposé</label>
                            <input type="text" name="code" class="form-control" placeholder="ex: AG-TUNIS-01" required/>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Nom de l'agence</label>
                            <input type="text" name="nom" class="form-control" placeholder="ex: Agence Tunis Centre" required/>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Adresse</label>
                            <input type="text" name="adresse" class="form-control" placeholder="ex: Avenue Habib Bourguiba, Tunis"/>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Collaborateurs souhaités</label>
                            <select name="utilisateurIds" multiple class="form-control" style="height:120px;">
                                <c:forEach var="u" items="${utilisateurs}">
                                    <option value="${u.id}">${u.libelleUtilisateur} — ID: ${u.id}</option>
                                </c:forEach>
                            </select>
                            <small style="color:var(--text-muted); font-size:0.75rem; margin-top:0.4rem; display:block;">
                                Maintenez Ctrl pour sélectionner plusieurs collaborateurs
                            </small>
                        </div>
                        <button type="submit" class="btn btn-primary">Soumettre la demande</button>
                    </form>
                </div>
            </c:if>

            <!-- NOTIFICATIONS -->
            <c:if test="${not empty notifications}">
                <div style="margin: 0 auto 2rem; max-width: 800px; text-align: center;" class="fade-up">
                    <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:1rem;">
                        Notifications
                    </h3>
                    <c:forEach var="n" items="${notifications}">
                        <div style="background:rgba(0,150,214,0.08); border:1px solid var(--border); border-radius:8px; padding:0.85rem 1.25rem; margin-bottom:0.5rem; font-size:0.875rem; color:var(--text-light);">
                                ${n.message}
                        </div>
                    </c:forEach>
                </div>
            </c:if>

            <!-- LIST OF DEMANDES -->
            <div class="fade-up" style="text-align: center;">
                <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:1.5rem;">
                    Historique des demandes
                </h3>
                <c:choose>
                    <c:when test="${empty demandes}">
                        <div class="empty-state">
                            <span class="icon">DM</span>
                            <p>Aucune demande soumise pour le moment.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>Code</th>
                                    <th>Nom</th>
                                    <th>Adresse</th>
                                    <th>Statut</th>
                                    <th>Date</th>
                                    <th>Commentaire</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="d" items="${demandes}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${d.codeAgencePropose}</td>
                                        <td>${d.nomAgencePropose}</td>
                                        <td>${d.adresseProposee}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${d.statut == 'APPROUVEE'}">
                                                    <span class="status status-approuvee">Approuvée</span>
                                                </c:when>
                                                <c:when test="${d.statut == 'REFUSEE'}">
                                                    <span class="status status-refusee">Refusée</span>
                                                </c:when>
                                                <c:otherwise>
                                                    <span class="status status-en_attente">En attente</span>
                                                </c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td>${d.dateCreation}</td>
                                        <td style="color:var(--text-muted);">${d.commentaireAdmin}</td>
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