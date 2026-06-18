<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Récupération</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>
<div class="login-wrapper">
    <div class="login-box fade-up">
        <div class="login-logo">
            <h1><span>BTK</span> BANK</h1>
            <div class="login-divider"></div>
            <p>Récupération de mot de passe</p>
        </div>

        <c:if test="${not empty error}">
            <div class="alert alert-error">${error}</div>
        </c:if>

        <c:if test="${not empty success}">
            <div class="alert alert-success" style="background: rgba(0, 210, 173, 0.15); border: 1px solid rgba(0, 210, 173, 0.3); color: var(--success);">
                ${success}
            </div>
            <div style="text-align:center; margin-top:1.5rem;">
                <a href="${pageContext.request.contextPath}/login" class="btn btn-primary" style="text-decoration:none; display:inline-block;">
                    Retour à la connexion
                </a>
            </div>
        </c:if>

        <c:if test="${empty success}">
            <p style="color:var(--text-muted); font-size:0.85rem; text-align:center; margin-bottom:1.5rem; line-height:1.5;">
                Saisissez votre identifiant ou votre email pour recevoir les instructions de récupération.
            </p>

            <form method="post" action="${pageContext.request.contextPath}/forgot-password">
                <div class="form-group">
                    <label class="form-label">Identifiant ou Email</label>
                    <input type="text" name="identifier" class="form-control"
                           placeholder="Ex: admin@mail.com" required autofocus/>
                </div>
                <button type="submit" class="btn btn-primary"
                        style="width:100%; justify-content:center; padding:0.75rem; margin-top:0.5rem; font-size:0.95rem;">
                    Réinitialiser mon mot de passe
                </button>
            </form>

            <div class="login-options-bar">
                <a href="${pageContext.request.contextPath}/login" class="forgot-password">
                    ← Retour à la connexion
                </a>
            </div>
        </c:if>

        <p style="text-align:center; color:var(--text-muted); font-size:0.75rem; margin-top:2rem;">
            © 2025 Banque Tuniso-Koweïtienne — Tous droits réservés
        </p>
    </div>
</div>
</body>
</html>
