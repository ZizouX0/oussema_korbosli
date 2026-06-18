<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Agences</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="admin_agences" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <div class="container">
            <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

            <div class="page-header fade-up">
                <h1>Gestion des agences</h1>
                <p>Créer, consulter et supprimer les agences BTK Bank</p>
            </div>

            <!-- CREATE FORM -->
            <div class="form-card fade-up" style="margin-bottom:2.5rem;">
                <h3 style="font-family:'Playfair Display',serif; color:var(--btk-accent); margin-bottom:1.5rem;">
                    Nouvelle agence
                </h3>
                <form method="post" action="${pageContext.request.contextPath}/agences">
                    <input type="hidden" name="action" value="create"/>
                    <div class="form-group">
                        <label class="form-label">Nom de l'agence</label>
                        <input type="text" name="nom" class="form-control"
                               placeholder="ex: Agence Sfax Centre" required/>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Adresse</label>
                        <input type="text" name="adresse" class="form-control"
                               placeholder="ex: Rue de la République, Sfax"/>
                    </div>
                    <button type="submit" class="btn btn-primary">Créer l'agence</button>
                </form>
            </div>

            <!-- AGENCES LIST -->
            <div class="fade-up" style="text-align: center;">
                <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:1.5rem;">
                    Liste des agences
                </h3>
                <c:choose>
                    <c:when test="${empty agences}">
                        <div class="empty-state">
                            <span class="icon">AG</span>
                            <p>Aucune agence enregistrée pour le moment.</p>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="table-wrapper">
                            <table>
                                <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom</th>
                                    <th>Adresse</th>
                                    <th>District</th>
                                    <th>Action</th>
                                </tr>
                                </thead>
                                <tbody>
                                <c:forEach var="a" items="${agences}">
                                    <tr>
                                        <td style="color:var(--btk-accent); font-weight:600;">${a.id}</td>
                                        <td>${a.nom}</td>
                                        <td>${a.adresse}</td>
                                        <td>${a.district}</td>
                                        <td>
                                            <form method="post" action="${pageContext.request.contextPath}/agences"
                                                  style="display:inline;"
                                                  onsubmit="return confirm('Supprimer cette agence ?')">
                                                <input type="hidden" name="action" value="delete"/>
                                                <input type="hidden" name="id" value="${a.id}"/>
                                                <button type="submit" class="btn btn-danger">Supprimer</button>
                                            </form>
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