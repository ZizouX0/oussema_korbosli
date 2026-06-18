<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Connexion</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>
<div class="login-wrapper">
    <div class="login-box fade-up">
        <div class="login-logo">
            <h1><span>BTK</span> BANK</h1>
            <div class="login-divider"></div>
            <p>Système de Gestion des Agences</p>
        </div>

        <c:if test="${not empty error}">
            <div class="alert alert-error">${error}</div>
        </c:if>

        <form method="post" action="${pageContext.request.contextPath}/login">
            <div class="form-group">
                <label class="form-label">Identifiant</label>
                <input type="text" name="username" class="form-control"
                       placeholder="Entrez votre identifiant" required autofocus/>
            </div>
            <div class="form-group">
                <label class="form-label">Mot de passe</label>
                <input type="password" name="password" class="form-control"
                       placeholder="••••••••" required/>
            </div>
            <button type="submit" class="btn btn-primary"
                    style="width:100%; justify-content:center; padding:0.75rem; margin-top:0.5rem; font-size:0.95rem;">
                Se connecter
            </button>
        </form>

        <div class="login-options-bar fade-up">
            <a href="${pageContext.request.contextPath}/forgot-password" class="forgot-password">Mot de passe oublié ?</a>
        </div>

        <p style="text-align:center; color:var(--text-muted); font-size:0.75rem; margin-top:2rem;">
            © 2026 Banque Tuniso-Koweïtienne — Tous droits réservés
        </p>
    </div>
</div>
</body>
</html>