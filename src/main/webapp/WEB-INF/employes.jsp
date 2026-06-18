<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Employés</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="employes" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <jsp:include page="top-bar.jsp" />
        <div class="container" style="padding-top: 1.5rem;">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>


            <!-- ACTIONS & QUICK ADD (HIDDEN FOR REGULAR USERS) -->
            <c:if test="${sessionScope.role == 'ADMIN' || sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
                <div class="fade-up" style="margin-bottom: 2.5rem; display: flex; justify-content: center;">
                    <div class="search-bar" style="max-width: 1000px; padding: 1rem 1.5rem;">
                        <form method="post" action="${pageContext.request.contextPath}/ajouter-employe" style="width: 100%;">
                            <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: flex-end; justify-content: space-between;">
                                
                                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; flex: 1;">
                                    <div class="form-group" style="margin-bottom: 0; min-width: 120px;">
                                        <label class="form-label" style="font-size: 0.65rem;">Matricule</label>
                                        <input type="text" name="matricule" class="form-control" style="padding: 0.4rem 0.6rem;" required placeholder="ex: BTK001"/>
                                    </div>
                                    <div class="form-group" style="margin-bottom: 0; min-width: 150px;">
                                        <label class="form-label" style="font-size: 0.65rem;">Nom & Prénom</label>
                                        <div style="display: flex; gap: 0.4rem;">
                                            <input type="text" name="nom" class="form-control" style="padding: 0.4rem 0.6rem;" placeholder="Nom" required/>
                                            <input type="text" name="prenom" class="form-control" style="padding: 0.4rem 0.6rem;" placeholder="Prénom" required/>
                                        </div>
                                    </div>
                                    <div class="form-group" style="margin-bottom: 0; min-width: 180px;">
                                        <label class="form-label" style="font-size: 0.65rem;">Email</label>
                                        <input type="email" name="email" class="form-control" style="padding: 0.4rem 0.6rem;" placeholder="email@btk.tn"/>
                                    </div>
                                    <div class="form-group" style="margin-bottom: 0; min-width: 80px;">
                                        <label class="form-label" style="font-size: 0.65rem;">Agence</label>
                                        <input type="number" name="banqueId" class="form-control" style="padding: 0.4rem 0.6rem;" required placeholder="ID"/>
                                    </div>
                                    <div class="form-group" style="margin-bottom: 0; min-width: 140px;">
                                        <label class="form-label" style="font-size: 0.65rem;">Rôle Prévu</label>
                                        <select name="role" class="form-control" style="padding: 0.4rem 0.6rem;">
                                            <option value="1">Gestionnaire</option>
                                            <option value="2">Conseiller</option>
                                            <option value="3">Hors Commercial</option>
                                        </select>
                                    </div>
                                </div>

                                <button type="submit" class="btn btn-primary" style="padding: 0.5rem 1.25rem; align-self: flex-end;">
                                    <c:choose>
                                        <c:when test="${sessionScope.role == 'ADMIN'}">Enregistrer</c:when>
                                        <c:otherwise>Soumettre demande</c:otherwise>
                                    </c:choose>
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <c:if test="${param.success == 1}">
                    <div class="alert alert-success fade-up" style="max-width: 600px; margin: 0 auto 1.5rem; text-align: center;">
                        Employé enregistré avec succès.
                    </div>
                </c:if>
                <c:if test="${param.pending == 1}">
                    <div class="alert fade-up" style="max-width: 600px; margin: 0 auto 1.5rem; text-align: center; background: rgba(0,150,214,0.1); border: 1px solid var(--btk-accent); color: var(--btk-accent);">
                        Demande d'ajout soumise. En attente de validation par l'administrateur.
                    </div>
                </c:if>
            </c:if>

            <!-- STATS -->
            <div style="display:flex; justify-content:center; gap:1.5rem; margin-bottom:2.5rem;" class="fade-up">
                <div class="card" style="text-align:center; min-width: 250px;">
                    <div style="font-size:2rem; font-weight:700; color:var(--btk-accent);">${totalEmployes}</div>
                    <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-top:0.25rem;">Total Employés</div>
                </div>
            </div>

            <!-- FILTER -->
            <div class="form-card fade-up" style="margin-bottom:1.5rem;">
                <form method="get" action="${pageContext.request.contextPath}/employes">
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:flex-end;">
                        <div class="form-group" style="margin-bottom:0; flex:1; min-width:150px;">
                            <label class="form-label">Agence (SK)</label>
                            <input type="number" name="agenceId" class="form-control"
                                   placeholder="ex: 4" value="${selectedAgenceId}"/>
                        </div>
                        <div class="form-group" style="margin-bottom:0;">
                            <label class="form-label">Rôle</label>
                            <select name="roleFilter" class="form-control">
                                <option value="">Tous</option>
                                <option value="conseiller" ${roleFilter == 'conseiller' ? 'selected' : ''}>Conseillers (Agences)</option>
                                <option value="hors_commercial" ${roleFilter == 'hors_commercial' ? 'selected' : ''}>Hors Commercial (Siège)</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">Filtrer</button>
                        <a href="${pageContext.request.contextPath}/employes" class="btn btn-outline">Tout afficher</a>
                    </div>
                </form>
            </div>

            <!-- TABLE -->
            <div class="fade-up">
                <div style="display:flex; justify-content:center; align-items:center; margin-bottom:1.5rem; gap: 1.5rem;">
                    <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted);">
                        Liste des employés
                    </h3>
                    <span style="font-size:0.8rem; color:var(--btk-accent); background:rgba(0,150,214,0.1); border:1px solid var(--border); padding:3px 10px; border-radius:20px;">
                        ${employes.size()} résultats
                    </span>
                </div>
                <c:choose>
                    <c:when test="${empty employes}">
                        <div class="empty-state">
                            <span class="icon">EM</span>
                            <p>Aucun employé trouvé.</p>
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
                                <c:forEach var="e" items="${employes}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${e.id}</td>
                                        <td style="font-weight:500;">${e.libelleUtilisateur}</td>
                                        <td style="color:var(--text-muted); font-size:0.8rem;">${e.emailUtilisateur}</td>
                                        <td>
                                            <span class="status ${e.roleClass}">${e.roleLabel}</span>

                                        </td>
                                        <td>Agence ${e.skAgence}</td>
                                        <td>
                                            <c:choose>
                                                <c:when test="${e.estSuspendu == 1}">
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

    // Validation métier : Pas de Conseiller au Siège (31) pour les Directeurs
    const form = document.querySelector('form[action$="ajouter-employe"]');
    const userRole = "${sessionScope.role}";

    if (form && userRole !== "ADMIN") {
        form.addEventListener('submit', function(e) {
            const agenceInput = this.querySelector('input[name="banqueId"]');
            const roleSelect = this.querySelector('select[name="role"]');
            
            if (agenceInput && roleSelect) {
                const agenceId = agenceInput.value;
                const roleId = roleSelect.value;
                
                // 31 = Siège, 2 = Conseiller
                if (agenceId === "31" && roleId === "2") {
                    e.preventDefault();
                    alert("Règle métier : Un 'Conseiller' ne peut pas être affecté au Siège (Agence 31). Veuillez modifier le rôle ou l'agence.");
                }
            }
        });
    }
</script>

</body>
</html>

