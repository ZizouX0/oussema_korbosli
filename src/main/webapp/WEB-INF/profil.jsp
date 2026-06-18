<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Mon Profil</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>

<div class="app-layout">
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="profile" />
    </jsp:include>

    <main class="main-wrapper">
        <jsp:include page="top-bar.jsp" />
        <div class="container" style="padding-top: 1.5rem;">
            <div class="page-header fade-up">
                <h1>Mon Profil</h1>
                <p>Gérez vos informations personnelles et suivez vos demandes de modification</p>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 2rem;" class="fade-up">
                <!-- PROFILE INFO -->
                <div class="card" style="padding: 2rem;">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <div style="width: 80px; height: 80px; background: var(--btk-accent-soft); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; color: var(--btk-accent);">
                            <i data-lucide="user" style="width: 40px; height: 40px;"></i>
                        </div>
                        <h2 style="font-size: 1.25rem;">${userProfile.libelleUtilisateur}</h2>
                        <span class="status-badge ${userProfile.roleClass}" style="margin-top: 0.5rem; display: inline-block;">
                            ${userProfile.roleLabel}
                        </span>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                        <div style="border-bottom: 1px solid var(--glass-border); padding-bottom: 0.75rem;">
                            <label style="display: block; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.25rem;">Email Actuel</label>
                            <div style="font-weight: 500;">${userProfile.emailUtilisateur}</div>
                        </div>
                        <div style="border-bottom: 1px solid var(--glass-border); padding-bottom: 0.75rem;">
                            <label style="display: block; font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.25rem;">Matricule</label>
                            <div style="font-weight: 500;">${userProfile.id}</div>
                        </div>
                    </div>

                    <!-- REQUEST FORM -->
                    <div style="margin-top: 3rem;">
                        <h3 style="font-size: 0.9rem; margin-bottom: 1.5rem; color: var(--btk-accent);">Demander une modification</h3>
                        <form action="${pageContext.request.contextPath}/mes-demandes" method="post" style="display: flex; flex-direction: column; gap: 1rem;">
                            <div class="form-group">
                                <label class="form-label" style="font-size: 0.75rem;">Champ à modifier</label>
                                <select name="champ" class="form-control" required>
                                    <option value="nom">Nom Complet</option>
                                    <option value="email">Email Personnel</option>
                                    <option value="feature">Suggérer une fonctionnalité / Demande</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label" style="font-size: 0.75rem;">Nouvelle Valeur</label>
                                <input type="text" name="nouvelleVal" class="form-control" placeholder="Entrez la nouvelle valeur" required>
                            </div>
                            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 0.5rem;">Envoyer la demande</button>
                        </form>
                    </div>
                </div>

                <!-- REQUEST HISTORY -->
                <div>
                    <div class="section-label-accent" style="margin-bottom: 1rem;">Historique de mes demandes</div>
                    <c:choose>
                        <c:when test="${empty demandes}">
                            <div class="card" style="padding: 3rem; text-align: center; opacity: 0.6;">
                                <i data-lucide="inbox" style="width: 48px; height: 48px; margin-bottom: 1rem; color: var(--text-muted);"></i>
                                <p>Vous n'avez aucune demande en cours ou passée.</p>
                            </div>
                        </c:when>
                        <c:otherwise>
                            <div style="display: flex; flex-direction: column; gap: 1rem;">
                                <c:forEach var="d" items="${demandes}">
                                    <div class="card" style="padding: 1.25rem; border-left: 4px solid 
                                        ${d.statut == 'EN_ATTENTE' ? 'var(--warning)' : 
                                          d.statut == 'EN_COURS' ? 'var(--btk-accent)' : 
                                          d.statut == 'EFFECTUE' ? 'var(--success)' : 'var(--danger)'}">
                                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                            <div>
                                                <div style="font-weight: 600; margin-bottom: 0.25rem;">
                                                    <c:choose>
                                                        <c:when test="${d.champ == 'feature'}">Suggestion de <span style="color: var(--btk-accent);">Fonctionnalité</span></c:when>
                                                        <c:otherwise>Changement de <span style="color: var(--btk-accent);">${d.champ == 'nom' ? 'Nom' : 'Email'}</span></c:otherwise>
                                                    </c:choose>
                                                </div>
                                                <c:if test="${d.champ != 'feature'}">
                                                    <div style="font-size: 0.85rem; color: var(--text-muted);">
                                                        De: <span style="text-decoration: line-through;">${d.ancienneVal}</span> → <span style="color: var(--white);">${d.nouvelleVal}</span>
                                                    </div>
                                                </c:if>
                                                <c:if test="${d.champ == 'feature'}">
                                                    <div style="font-size: 0.85rem; color: var(--text-light); font-style: italic;">
                                                        " ${d.nouvelleVal} "
                                                    </div>
                                                </c:if>
                                            </div>
                                            <span class="status-badge ${d.statut == 'EN_ATTENTE' ? 'status-en_attente' : 
                                                                         d.statut == 'EN_COURS' ? 'status-hors' : 
                                                                         d.statut == 'EFFECTUE' ? 'status-approuvee' : 'status-refusee'}">
                                                ${d.statut}
                                            </span>
                                        </div>
                                        <c:if test="${not empty d.commentaire}">
                                            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 8px; font-size: 0.8rem;">
                                                <strong style="color: var(--btk-accent);">Commentaire :</strong> ${d.commentaire}
                                            </div>
                                        </c:if>
                                        <div style="margin-top: 1rem; font-size: 0.7rem; color: var(--text-muted); display: flex; justify-content: space-between;">
                                            <span>Soumis le ${d.dateDemande}</span>
                                            <c:if test="${not empty d.dateDecision}">
                                                <span>Traité le ${d.dateDecision}</span>
                                            </c:if>
                                        </div>
                                    </div>
                                </c:forEach>
                            </div>
                        </c:otherwise>
                    </c:choose>
                </div>
            </div>

            <c:if test="${not empty success}">
                <div class="alert alert-success fade-up" style="margin-top: 2rem;">Demande envoyée avec succès ! Elle est en attente d'approbation.</div>
            </c:if>
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
