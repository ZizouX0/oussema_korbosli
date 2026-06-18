<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Validation des demandes</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head><body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="validations" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Validation des demandes</h1>
                <p>Gérer les demandes d'ouverture d'agence, d'ajout d'employés et de clients</p>
            </div>

            <!-- SECTION 1: AGENCES -->
            <div class="section-divider fade-up" style="margin-top: 2rem;">Ouverture d'Agences</div>
            <div class="fade-up">
                <c:choose>
                    <c:when test="${empty demandes}">
                        <div class="empty-state">
                            <p>Aucune demande d'agence en attente.</p>
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
                                    <th>Directeur</th>
                                    <th>Date</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="d" items="${demandes}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${d.codeAgencePropose}</td>
                                        <td>${d.nomAgencePropose}</td>
                                        <td>${d.adresseProposee}</td>
                                        <td>${d.directeur.login}</td>
                                        <td>${d.dateCreation}</td>
                                        <td>
                                            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;">
                                                    <input type="hidden" name="action" value="approve"/>
                                                    <input type="hidden" name="id" value="${d.id}"/>
                                                    <button type="submit" class="btn btn-success">Approuver</button>
                                                </form>
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;" onsubmit="return confirmRefus(this)">
                                                    <input type="hidden" name="action" value="refuse"/>
                                                    <input type="hidden" name="id" value="${d.id}"/>
                                                    <input type="text" name="commentaire" class="form-control" placeholder="Motif..." style="display:inline-block; width:120px; padding:0.4rem 0.5rem;"/>
                                                    <button type="submit" class="btn btn-danger">Refuser</button>
                                                </form>
                                            </div>
                                        </td>
                                    </tr>
                                </c:forEach>
                                </tbody>
                            </table>
                        </div>
                    </c:otherwise>
                </c:choose>
            </div>

            <!-- SECTION 2: EMPLOYES -->
            <div class="section-divider fade-up" style="margin-top: 3rem;">Ajout d'Employés</div>
            <div class="fade-up" style="margin-bottom: 3rem;">
                <c:choose>
                    <c:when test="${empty demandesEmployes}">
                        <div class="empty-state">
                            <p>Aucune demande d'employé en attente.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>Matricule</th>
                                    <th>Nom & Prénom</th>
                                    <th>Email</th>
                                    <th>Rôle Prévu</th>
                                    <th>Agence</th>
                                    <th>Par</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="e" items="${demandesEmployes}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${e.matricule}</td>
                                        <td>${e.prenom} ${e.nom}</td>
                                        <td>${e.email}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${e.rolePrevu == 1.0}"><span class="badge role-gestionnaire">Gestionnaire</span></c:when>
                                                <c:otherwise><span class="badge role-conseiller">Conseiller</span></c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td>Agence ${e.skAgence}</td>
                                        <td>${e.directeur.login}</td>
                                        <td>
                                            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;">
                                                    <input type="hidden" name="actionEmp" value="approve"/>
                                                    <input type="hidden" name="idEmp" value="${e.id}"/>
                                                    <button type="submit" class="btn btn-success">Valider</button>
                                                </form>
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;" onsubmit="return confirmRefus(this)">
                                                    <input type="hidden" name="actionEmp" value="refuse"/>
                                                    <input type="hidden" name="idEmp" value="${e.id}"/>
                                                    <input type="text" name="commentaire" class="form-control" placeholder="Motif..." style="display:inline-block; width:120px; padding:0.4rem 0.5rem;"/>
                                                    <button type="submit" class="btn btn-danger">Refuser</button>
                                                </form>
                                            </div>
                                        </td>
                                    </tr>
                                </c:forEach>
                                </tbody>
                            </table>
                        </div>
                    </c:otherwise>
                </c:choose>
            <!-- SECTION 3: CLIENTS -->
            <div class="section-divider fade-up" style="margin-top: 3rem;">Ajout de Clients</div>
            <div class="fade-up" style="margin-bottom: 5rem;">
                <c:choose>
                    <c:when test="${empty demandesClients}">
                        <div class="empty-state">
                            <p>Aucune demande de client en attente.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>Nom & Prénom</th>
                                    <th>Type</th>
                                    <th>Sexe</th>
                                    <th>Agence</th>
                                    <th>Par</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="c" items="${demandesClients}">
                                    <tr>
                                        <td style="font-weight: 600;">${c.prenomClient} ${c.nomClient}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${c.typeClient == 'Particulier'}"><span class="status status-approuvee">Particulier</span></c:when>
                                                <c:otherwise><span class="status status-en_attente">Société</span></c:otherwise>
                                            </c:choose>
                                        </td>
                                        <td>${c.sexe}</td>
                                        <td>Agence ${c.skAgence}</td>
                                        <td>${c.directeur.login}</td>
                                        <td>
                                            <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;">
                                                    <input type="hidden" name="actionCli" value="approve"/>
                                                    <input type="hidden" name="idCli" value="${c.id}"/>
                                                    <button type="submit" class="btn btn-success">Valider</button>
                                                </form>
                                                <form method="post" action="${pageContext.request.contextPath}/demandes-admin" style="display:inline;" onsubmit="return confirmRefus(this)">
                                                    <input type="hidden" name="actionCli" value="refuse"/>
                                                    <input type="hidden" name="idCli" value="${c.id}"/>
                                                    <input type="text" name="commentaire" class="form-control" placeholder="Motif..." style="display:inline-block; width:120px; padding:0.4rem 0.5rem;"/>
                                                    <button type="submit" class="btn btn-danger">Refuser</button>
                                                </form>
                                            </div>
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

<script>
    function confirmRefus(form) {
        const commentaire = form.querySelector('[name="commentaire"]').value.trim();
        if (!commentaire) {
            alert('Veuillez saisir un motif de refus.');
            return false;
        }
        return confirm('Confirmer le refus de cette demande ?');
    }
</script>

<!-- LUCIDE ICONS -->
<script src="https://unpkg.com/lucide@latest"></script>
<script>
    lucide.createIcons();
</script>

</body>
</html>