<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Pointage</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="pointage" />
    </jsp:include>

    <main class="main-wrapper">
        <jsp:include page="top-bar.jsp"/>
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Pointage des employés</h1>
                <p>Présence quotidienne : arrivée, départ et statut</p>
            </div>

            <!-- POINTER (employé connecté) -->
            <div class="form-card fade-up" style="margin-bottom:2.5rem;">
                <h3 style="color:var(--btk-accent); margin-bottom:1rem;">Mon pointage du jour</h3>
                <c:choose>
                    <c:when test="${not empty pointageDuJour}">
                        <p>Arrivée :
                            <strong>${not empty pointageDuJour.heureArrivee ? pointageDuJour.heureArrivee.toLocalTime() : '—'}</strong>
                            &nbsp;|&nbsp; Départ :
                            <strong>${not empty pointageDuJour.heureDepart ? pointageDuJour.heureDepart.toLocalTime() : '—'}</strong>
                            &nbsp;|&nbsp; Statut : <strong>${pointageDuJour.statut}</strong>
                        </p>
                    </c:when>
                    <c:otherwise>
                        <p>Vous n'avez pas encore pointé aujourd'hui.</p>
                    </c:otherwise>
                </c:choose>
                <div style="display:flex; gap:1rem; margin-top:1rem;">
                    <form method="post" action="${pageContext.request.contextPath}/pointage">
                        <input type="hidden" name="action" value="arrivee"/>
                        <button type="submit" class="btn btn-primary">Pointer l'arrivée</button>
                    </form>
                    <form method="post" action="${pageContext.request.contextPath}/pointage">
                        <input type="hidden" name="action" value="depart"/>
                        <button type="submit" class="btn btn-secondary">Pointer le départ</button>
                    </form>
                </div>
            </div>

            <!-- SAISIE MANUELLE (admin) -->
            <c:if test="${sessionScope.role == 'ADMIN'}">
            <div class="form-card fade-up" style="margin-bottom:2.5rem;">
                <h3 style="color:var(--btk-accent); margin-bottom:1.5rem;">Saisie / correction manuelle</h3>
                <form method="post" action="${pageContext.request.contextPath}/pointage">
                    <input type="hidden" name="action" value="manuel"/>
                    <div class="form-group">
                        <label class="form-label">Employé</label>
                        <select name="employeId" class="form-control" required>
                            <c:forEach var="e" items="${employes}">
                                <option value="${e.id}">${e.libelleUtilisateur}</option>
                            </c:forEach>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Date</label>
                        <input type="date" name="datePointage" class="form-control" required/>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Statut</label>
                        <select name="statut" class="form-control">
                            <option value="PRESENT">Présent</option>
                            <option value="RETARD">Retard</option>
                            <option value="ABSENT">Absent</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Heure d'arrivée</label>
                        <input type="time" name="heureArrivee" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Heure de départ</label>
                        <input type="time" name="heureDepart" class="form-control"/>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Commentaire</label>
                        <input type="text" name="commentaire" class="form-control"/>
                    </div>
                    <button type="submit" class="btn btn-primary">Enregistrer</button>
                </form>
            </div>
            </c:if>

            <!-- HISTORIQUE -->
            <div class="fade-up">
                <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:1rem;">
                    Historique des pointages (présents aujourd'hui : ${presentsAujourdhui})
                </h3>
                <c:choose>
                    <c:when test="${empty pointages}">
                        <div class="empty-state"><p>Aucun pointage enregistré.</p></div>
                    </c:when>
                    <c:otherwise>
                        <table class="data-table" style="width:100%;">
                            <thead>
                                <tr>
                                    <th>Employé</th><th>Date</th><th>Arrivée</th>
                                    <th>Départ</th><th>Statut</th><th>Source</th>
                                </tr>
                            </thead>
                            <tbody>
                            <c:forEach var="p" items="${pointages}">
                                <tr>
                                    <td>${p.employe.libelleUtilisateur}</td>
                                    <td>${p.datePointage}</td>
                                    <td>${not empty p.heureArrivee ? p.heureArrivee.toLocalTime() : '—'}</td>
                                    <td>${not empty p.heureDepart ? p.heureDepart.toLocalTime() : '—'}</td>
                                    <td>${p.statut}</td>
                                    <td>${p.source}</td>
                                </tr>
                            </c:forEach>
                            </tbody>
                        </table>
                    </c:otherwise>
                </c:choose>
            </div>
        </div>
    </main>
</div>

<script src="https://unpkg.com/lucide@latest"></script>
<script>lucide.createIcons();</script>
</body>
</html>
