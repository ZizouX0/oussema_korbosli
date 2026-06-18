<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>BTK Bank — Agences & Effectifs</title>
  <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
  <!-- SIDEBAR -->
  <jsp:include page="sidebar.jsp">
    <jsp:param name="activePage" value="agences_btk" />
  </jsp:include>

  <!-- MAIN CONTENT -->
  <main class="main-wrapper">
    <div class="container">
      <a href="${pageContext.request.contextPath}/home" class="back-link fade-up">Retour au tableau de bord</a>

      <div class="page-header fade-up">
        <h1>Agences & Membres</h1>
        <p>Sélectionnez une agence pour afficher ses membres et leurs détails</p>
      </div>

      <!-- SÉLECTEUR D'AGENCE -->
      <div class="form-card fade-up" style="margin-bottom:2rem;">
        <form method="get" action="${pageContext.request.contextPath}/banques">
          <div style="display:flex; align-items:flex-end; gap:1rem; flex-wrap:wrap;">
            <div class="form-group" style="margin-bottom:0; flex:1; min-width:200px;">
              <label class="form-label">Sélectionner une agence</label>
              <select name="agenceId" class="form-control">
                <option value="">-- Choisir une agence --</option>
                <c:forEach var="a" items="${agences}">
                  <option value="${a.id}"
                    ${a.id == selectedAgenceId ? 'selected' : ''}>
                      ${a.id} — ${a.nom}
                  </option>
                </c:forEach>
              </select>
            </div>
            <button type="submit" class="btn btn-primary" style="padding:0.65rem 1.5rem;">
              Voir les membres
            </button>
          </div>
        </form>
      </div>

      <!-- INFOS AGENCE SÉLECTIONNÉE -->
      <c:if test="${not empty selectedAgenceId}">
        <c:forEach var="a" items="${agences}">
          <c:if test="${a.id == selectedAgenceId}">
            <div class="card fade-up" style="margin: 0 auto 2rem; border-left:3px solid var(--btk-accent); text-align: center; max-width: 600px;">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                <div>
                  <div style="font-size:0.75rem; color:var(--btk-accent); font-weight:600; letter-spacing:1px; text-transform:uppercase;">
                      District: ${a.district}
                  </div>
                  <div style="font-family:'Playfair Display',serif; font-size:1.4rem; margin:0.25rem 0;">
                      ${a.nom}
                  </div>
                  <div style="font-size:0.85rem; color:var(--text-muted);">
                    ${a.adresse}
                  </div>
                </div>
              </div>
            </div>
          </c:if>
        </c:forEach>

        <!-- TABLEAU DES EFFECTIFS -->
        <div class="fade-up">
          <div style="display:flex; justify-content:center; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:1.5rem;">
            <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:0;">
              Membres de l'agence
            </h3>
            
            <!-- CALCUL DES STATTS -->
            <c:set var="countGest" value="0"/>
            <c:set var="countCons" value="0"/>
            <c:set var="countHors" value="0"/>
            <c:forEach var="u" items="${utilisateurs}">
                <c:choose>
                    <c:when test="${u.estGestionnaire == 1.0}">
                        <c:set var="countGest" value="${countGest + 1}"/>
                    </c:when>
                    <c:when test="${u.estGestionnaire == 0.0 && not empty u.skAgence && u.skAgence == 31}">
                        <c:set var="countHors" value="${countHors + 1}"/>
                    </c:when>
                    <c:otherwise>
                        <c:set var="countCons" value="${countCons + 1}"/>
                    </c:otherwise>
                </c:choose>
            </c:forEach>

            <div style="display:flex; gap:0.75rem;">
                <span class="badge role-gestionnaire" style="padding:0.4rem 0.8rem; font-size:0.75rem;">
                    ${countGest} Gestionnaires
                </span>
                <span class="badge role-conseiller" style="padding:0.4rem 0.8rem; font-size:0.75rem;">
                    ${countCons} Conseillers
                </span>
                <span class="badge role-hors" style="padding:0.4rem 0.8rem; font-size:0.75rem;">
                    ${countHors} Hors Commercial
                </span>
            </div>
          </div>
          <c:choose>
            <c:when test="${empty utilisateurs}">
              <div class="empty-state">
                <span class="icon">MB</span>
                <p>Aucun membre affecté à cette agence pour le moment.</p>
              </div>
            </c:when>
            <c:otherwise>
              <div class="table-wrapper">
                <table>
                  <thead>
                  <tr>
                    <th>ID</th>
                    <th>Nom & Prénom</th>
                    <th>Email</th>
                    <th>Rôle</th>
                  </tr>
                  </thead>
                  <tbody>
                  <c:forEach var="u" items="${utilisateurs}">
                    <tr>
                      <td style="color:var(--btk-accent); font-weight:600;">${u.id}</td>
                      <td>${u.libelleUtilisateur}</td>
                      <td>${u.emailUtilisateur}</td>
                      <td>
                        <span class="badge ${u.roleClass}">${u.roleLabel}</span>

                      </td>
                    </tr>
                  </c:forEach>
                  </tbody>
                </table>
              </div>
            </c:otherwise>
          </c:choose>
        </div>
      </c:if>

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