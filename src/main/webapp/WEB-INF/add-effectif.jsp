<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Nouvel Employé</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="add_effectif" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Enregistrer un nouvel employé</h1>
                <p>Saisissez les informations pour ajouter un nouveau membre aux effectifs de la BTK Bank</p>
            </div>

            <div class="form-card fade-up">
                <c:if test="${not empty error}">
                    <div class="alert alert-error" style="margin-bottom:1.5rem;">${error}</div>
                </c:if>

                <form action="${pageContext.request.contextPath}/ajouter-employe" method="post">
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;">
                        
                        <div class="form-group">
                            <label class="form-label" for="matricule">Matricule (Unique)</label>
                            <input type="text" id="matricule" name="matricule" class="form-control" required placeholder="ex: BTK-2024-001"/>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="banqueId">Banque / Siège</label>
                            <select id="banqueId" name="banqueId" class="form-control" required>
                                <option value="" disabled selected>Sélectionnez une banque...</option>
                                <c:forEach var="b" items="${banques}">
                                    <option value="${b.id}">${b.nom}</option>
                                </c:forEach>
                            </select>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="nom">Nom</label>
                            <input type="text" id="nom" name="nom" class="form-control" required placeholder="Nom de famille"/>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="prenom">Prénom</label>
                            <input type="text" id="prenom" name="prenom" class="form-control" placeholder="Prénom(s)"/>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="statut">Statut</label>
                            <select id="statut" name="statut" class="form-control">
                                <option value="ACTIF">Actif</option>
                                <option value="EN_CONGE">En Congé</option>
                                <option value="SUSPENDU">Suspendu</option>
                                <option value="DETACHE">Détaché</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="dateEntree">Date d'Entrée</label>
                            <input type="date" id="dateEntree" name="dateEntree" class="form-control"/>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="role">Rôle Prévu</label>
                            <select id="role" name="role" class="form-control" required>
                                <option value="1">Gestionnaire</option>
                                <option value="2" selected>Conseiller</option>
                                <option value="3">Hors Commercial</option>
                            </select>
                        </div>

                    </div>

                    <div style="margin-top:2rem; display:flex; justify-content:flex-end; gap:1rem;">
                        <a href="${pageContext.request.contextPath}/home" class="btn btn-outline" style="padding:0.75rem 2rem;">Annuler</a>
                        <button type="submit" class="btn btn-primary" style="padding:0.75rem 2.5rem;">Enregistrer l'employé</button>
                    </div>
                </form>
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
