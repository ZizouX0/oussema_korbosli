<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="jakarta.tags.core" prefix="c" %>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BTK Bank — Tableau de bord</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css"/>
</head>
<body>

<div class="app-layout">
    <!-- SIDEBAR -->
    <jsp:include page="sidebar.jsp">
        <jsp:param name="activePage" value="dashboard" />
    </jsp:include>

    <!-- MAIN CONTENT -->
    <main class="main-wrapper">
        <jsp:include page="top-bar.jsp" />
        <div class="container" style="padding-top: 1.5rem;">
            <div class="page-header fade-up" style="text-align: left; margin-bottom: 2rem;">
                <h1 style="font-size: 2rem;">Bonjour, ${sessionScope.user} <span style="font-size: 0.65rem; background: var(--btk-accent); color: white; padding: 2px 6px; border-radius: 4px; vertical-align: middle; margin-left: 10px; opacity: 0.8;">BTK Dashboard</span></h1>
                <p>Bienvenue sur votre espace de gestion BTK Bank</p>
            </div>

            <c:choose>
                <c:when test="${sessionScope.role == 'ADMIN' || sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
                    <!-- KPI ROW -->
                    <div class="fade-up" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(190px,1fr)); gap:1.25rem; margin-bottom:2rem;">
                        <div class="card" style="display:flex; align-items:center; gap:1rem; padding:1.35rem;">
                            <div style="width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:var(--btk-accent-soft);color:var(--btk-accent);"><i data-lucide="users"></i></div>
                            <div><div style="font-size:1.8rem;font-weight:800;color:var(--white);line-height:1;">${totalEmployes}</div><div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:5px;">Employés</div></div>
                        </div>
                        <div class="card" style="display:flex; align-items:center; gap:1rem; padding:1.35rem;">
                            <div style="width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:rgba(26,111,212,0.15);color:#1a6fd4;"><i data-lucide="briefcase"></i></div>
                            <div><div style="font-size:1.8rem;font-weight:800;color:var(--white);line-height:1;">${totalClients}</div><div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:5px;">Clients</div></div>
                        </div>
                        <div class="card" style="display:flex; align-items:center; gap:1rem; padding:1.35rem;">
                            <div style="width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:rgba(0,210,173,0.15);color:var(--success);"><i data-lucide="user-check"></i></div>
                            <div><div style="font-size:1.8rem;font-weight:800;color:var(--white);line-height:1;">${presentsAujourdhui}</div><div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:5px;">Présents aujourd'hui</div></div>
                        </div>
                        <div class="card" style="display:flex; align-items:center; gap:1rem; padding:1.35rem;">
                            <div style="width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:rgba(0,174,239,0.12);color:var(--btk-accent);"><i data-lucide="activity"></i></div>
                            <div><div style="font-size:1.8rem;font-weight:800;color:var(--white);line-height:1;">${tauxPresence}%</div><div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:5px;">Taux de présence</div></div>
                        </div>
                        <div class="card" style="display:flex; align-items:center; gap:1rem; padding:1.35rem;">
                            <div style="width:52px;height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:rgba(255,188,75,0.15);color:var(--warning);"><i data-lucide="clock"></i></div>
                            <div><div style="font-size:1.8rem;font-weight:800;color:var(--white);line-height:1;"><c:choose><c:when test="${sessionScope.role == 'ADMIN'}">${pendingClientDemandes + pendingEmployeDemandes}</c:when><c:otherwise>${pendingModifs}</c:otherwise></c:choose></div><div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-top:5px;">Demandes en attente</div></div>
                        </div>
                    </div>

                    <!-- ADMINISTRATIVE ALERTS -->
                    <c:if test="${(sessionScope.role == 'ADMIN' && (pendingClientDemandes > 0 || pendingEmployeDemandes > 0 || approvedModifs > 0)) || (sessionScope.role == 'DIRECTEUR_COMMERCIAL' && pendingModifs > 0)}">
                        <div class="section-label-accent fade-up" style="margin-top: 2rem; color: var(--warning);">Actions Requises</div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 2rem;" class="fade-up">
                            <c:if test="${sessionScope.role == 'ADMIN'}">
                                <c:if test="${pendingClientDemandes > 0}">
                                    <a href="${pageContext.request.contextPath}/demandes-admin" class="stat-card-modern" style="border-color: var(--warning); text-decoration: none;">
                                        <div class="stat-header">
                                            <span class="stat-label-modern" style="color: var(--warning);">Demandes Clients</span>
                                            <span class="stat-state state-warning">À valider</span>
                                        </div>
                                        <div class="stat-body-modern">
                                            <div class="stat-bar-wrapper">
                                                <div class="stat-bar-fill" style="width: 70%; background: var(--warning);"></div>
                                            </div>
                                            <div class="stat-value-modern" style="color: var(--warning);">${pendingClientDemandes}</div>
                                        </div>
                                    </a>
                                </c:if>
                                <c:if test="${pendingEmployeDemandes > 0}">
                                    <a href="${pageContext.request.contextPath}/demandes-admin" class="btn fade-up" style="background: rgba(255, 188, 75, 0.15); border: 2px solid var(--warning); color: var(--warning); padding: 1.25rem 2rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; text-decoration: none; transition: all 0.3s ease; box-shadow: 0 0 20px rgba(255, 188, 75, 0.1);">
                                        <div style="width: 48px; height: 48px; background: var(--warning); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: var(--btk-blue-deep);">
                                            <i data-lucide="user-plus" style="width: 24px; height: 24px;"></i>
                                        </div>
                                        <div style="flex: 1;">
                                            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; opacity: 0.8;">Action Requise</div>
                                            <div style="font-size: 1.1rem; font-weight: 800;">${pendingEmployeDemandes} Demandes d'employés</div>
                                        </div>
                                        <i data-lucide="chevron-right" style="opacity: 0.5;"></i>
                                    </a>
                                </c:if>
                                <c:if test="${approvedModifs > 0}">
                                    <a href="${pageContext.request.contextPath}/gestion-demandes" class="stat-card-modern" style="border-color: var(--btk-accent); text-decoration: none;">
                                        <div class="stat-header">
                                            <span class="stat-label-modern" style="color: var(--btk-accent);">Modifs à appliquer</span>
                                            <span class="stat-state state-info">En cours</span>
                                        </div>
                                        <div class="stat-body-modern">
                                            <div class="stat-bar-wrapper">
                                                <div class="stat-bar-fill" style="width: 60%; background: var(--btk-accent);"></div>
                                            </div>
                                            <div class="stat-value-modern" style="color: var(--btk-accent);">${approvedModifs}</div>
                                        </div>
                                    </a>
                                </c:if>
                            </c:if>

                            <c:if test="${sessionScope.role == 'DIRECTEUR_COMMERCIAL'}">
                                <c:if test="${pendingModifs > 0}">
                                    <a href="${pageContext.request.contextPath}/gestion-demandes" class="btn fade-up" style="background: rgba(0, 174, 239, 0.15); border: 2px solid var(--btk-accent); color: var(--btk-accent); padding: 1.25rem 2rem; border-radius: 12px; display: flex; align-items: center; gap: 1rem; text-decoration: none; transition: all 0.3s ease; box-shadow: 0 0 20px rgba(0, 174, 239, 0.1);">
                                        <div style="width: 48px; height: 48px; background: var(--btk-accent); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: var(--white);">
                                            <i data-lucide="clipboard-list" style="width: 24px; height: 24px;"></i>
                                        </div>
                                        <div style="flex: 1;">
                                            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; opacity: 0.8;">Action Requise</div>
                                            <div style="font-size: 1.1rem; font-weight: 800;">${pendingModifs} Demandes & Suggestions</div>
                                        </div>
                                        <i data-lucide="chevron-right" style="opacity: 0.5;"></i>
                                    </a>
                                </c:if>
                            </c:if>
                        </div>
                    </c:if>
                    
                    <!-- CHARTS SECTION -->
                    <div class="section-divider fade-up">Analyses & Statistiques</div>
                    <div class="charts-grid fade-up" style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
                        <div class="card" style="padding: 1.5rem;">
                            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i data-lucide="bar-chart-3" style="width: 18px; height: 18px; color: var(--btk-accent);"></i>
                                Effectif par agence
                            </div>
                            <div id="agencyChart" style="min-height: 400px;"></div>
                        </div>
                        <div class="card" style="padding: 1.5rem;">
                            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i data-lucide="pie-chart" style="width: 18px; height: 18px; color: var(--btk-accent);"></i>
                                Répartition des rôles
                            </div>
                            <div id="roleChart" style="min-height: 400px;"></div>
                        </div>
                    </div>

                    <!-- POINTAGE ROW -->
                    <div class="charts-grid fade-up" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
                        <div class="card" style="padding: 1.5rem;">
                            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                                <i data-lucide="clock" style="width: 18px; height: 18px; color: var(--btk-accent);"></i>
                                Présence du jour
                            </div>
                            <div id="pointageChart" style="min-height: 320px;"></div>
                        </div>
                        <div class="card" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:center; gap:0.75rem;">
                            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 0.5rem;">Synthèse présence</div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:0.7rem 0; border-bottom:1px solid var(--glass-border);"><span style="color:var(--text-muted);"><i data-lucide="user-check" style="width:16px; vertical-align:middle; color:var(--success);"></i> Présents</span><strong style="color:var(--success); font-size:1.2rem;">${presentsAujourdhui}</strong></div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:0.7rem 0; border-bottom:1px solid var(--glass-border);"><span style="color:var(--text-muted);"><i data-lucide="alarm-clock" style="width:16px; vertical-align:middle; color:var(--warning);"></i> Retards</span><strong style="color:var(--warning); font-size:1.2rem;">${retardsAujourdhui}</strong></div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding:0.7rem 0;"><span style="color:var(--text-muted);"><i data-lucide="user-x" style="width:16px; vertical-align:middle; color:var(--danger);"></i> Absents</span><strong style="color:var(--danger); font-size:1.2rem;">${absentsAujourdhui}</strong></div>
                            <a href="${pageContext.request.contextPath}/pointage" class="btn btn-outline" style="margin-top:0.75rem; border-color:var(--btk-accent); color:var(--btk-accent); padding:0.6rem 1.5rem; border-radius:30px; text-decoration:none; text-align:center;">Gérer le pointage</a>
                        </div>
                    </div>
                </c:when>
                <c:otherwise>
                    <!-- SIMPLIFIED VIEW FOR REGULAR USERS -->
                    <div class="card fade-up" style="padding: 3rem; text-align: center; background: linear-gradient(135deg, rgba(0,174,239,0.1), transparent); border: 1px solid var(--glass-border); margin: 2rem 0;">
                        <div style="width: 64px; height: 64px; background: var(--btk-accent-soft); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;">
                            <i data-lucide="shield-check" style="width: 32px; height: 32px; color: var(--btk-accent);"></i>
                        </div>
                        <h2 style="font-size: 1.5rem; margin-bottom: 0.75rem; color: var(--white);">Espace Personnel Sécurisé</h2>
                        <p style="color: var(--text-muted); font-size: 1rem; max-width: 500px; margin: 0 auto 2rem;">
                            Bienvenue dans votre interface de gestion simplifiée. Vous pouvez consulter les annuaires et suivre vos demandes en cours via le menu de navigation.
                        </p>
                        <div style="display: flex; justify-content: center; gap: 1rem;">
                            <div class="badge-role" style="background: rgba(255,255,255,0.05); border-color: var(--glass-border); color: var(--text-muted);">Accès Read-Only</div>
                        </div>

                        <!-- SUGGESTION BOX SHORTCUT -->
                        <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--glass-border);">
                            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">UNE IDÉE POUR AMÉLIORER LA PLATEFORME ?</div>
                            <a href="${pageContext.request.contextPath}/mes-demandes" class="btn btn-outline" style="border-color: var(--btk-accent); color: var(--btk-accent); padding: 0.8rem 2rem; border-radius: 30px; text-decoration: none; display: inline-flex; align-items: center; gap: 0.75rem; transition: all 0.3s ease;">
                                <i data-lucide="lightbulb" style="width: 18px;"></i>
                                Soumettre une suggestion
                            </a>
                        </div>
                    </div>
                </c:otherwise>
            </c:choose>

            <!-- ACTION CARDS (Common for everyone) -->
            <div class="section-divider fade-up">Navigation Rapide</div>
            <div class="action-grid" style="margin-bottom:2rem;">
                <a href="${pageContext.request.contextPath}/employes" class="action-card fade-up">
                    <div class="action-icon"><i data-lucide="users"></i></div>
                    <div class="action-title">Employés</div>
                    <div class="action-desc">Annuaire BTK</div>
                </a>
                <a href="${pageContext.request.contextPath}/clients-btk" class="action-card fade-up">
                    <div class="action-icon" style="background: linear-gradient(135deg, var(--btk-accent), var(--btk-blue-mid));"><i data-lucide="briefcase"></i></div>
                    <div class="action-title">Clients</div>
                    <div class="action-desc">Gestion du portefeuille</div>
                </a>
                <a href="${pageContext.request.contextPath}/demandes-agence" class="action-card fade-up">
                    <div class="action-icon"><i data-lucide="file-text"></i></div>
                    <div class="action-title">Mes Demandes</div>
                    <div class="action-desc">Suivi des requêtes</div>
                </a>
            </div>

        </div>
    </main>
</div>

<!-- APEXCHARTS -->
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
<!-- LUCIDE ICONS -->
<script src="https://unpkg.com/lucide@latest"></script>
<script>
    lucide.createIcons();

    const chartTheme = { mode: 'dark', palette: 'palette1' };

    // Agency Chart (Vertical Columns - Top 10)
    if (document.querySelector("#agencyChart")) {
        const fullLabels = [${chartAgencyLabels}];
        const fullData = [${chartAgencyData}];
        
        // Take only top 10
        const topLabels = fullLabels.slice(0, 10);
        const topData = fullData.slice(0, 10);

        new ApexCharts(document.querySelector("#agencyChart"), {
            series: [{ name: 'Employés', data: topData }],
            chart: { type: 'bar', height: 500, toolbar: { show: false }, background: 'transparent' },
            theme: chartTheme,
            plotOptions: { 
                bar: { 
                    borderRadius: 10, 
                    columnWidth: '70%',
                    distributed: true,
                    dataLabels: { position: 'top' }
                } 
            },
            dataLabels: { 
                enabled: true, 
                offsetY: -25, 
                style: { fontSize: '14px', fontWeight: 'bold', colors: ['#fff'] } 
            },
            xaxis: { 
                categories: topLabels, 
                labels: { style: { fontSize: '12px', fontWeight: 600 } } 
            },
            yaxis: {
                labels: { style: { fontSize: '12px' } }
            },
            colors: ['#00AEEF', '#0057B8', '#003F88', '#1a6fd4', '#00d2ad', '#ffbc4b', '#ff5e57', '#a29bfe', '#6c5ce7', '#00cec9'],
            grid: { borderColor: 'rgba(255,255,255,0.05)' }
        }).render();
    }

    // Role Chart (Donut)
    if (document.querySelector("#roleChart")) {
        new ApexCharts(document.querySelector("#roleChart"), {
            series: [${chartRoleData}],
            chart: { type: 'donut', height: 350, background: 'transparent' },
            theme: chartTheme,
            labels: [${chartRoleLabels}],
            colors: ['#00AEEF', '#00d2ad', '#ffbc4b'],
            stroke: { show: false },
            legend: { position: 'bottom' }
        }).render();
    }

    // Pointage Chart (Donut) — présence du jour
    if (document.querySelector("#pointageChart")) {
        new ApexCharts(document.querySelector("#pointageChart"), {
            series: [${chartPointageData}],
            chart: { type: 'donut', height: 320, background: 'transparent' },
            theme: chartTheme,
            labels: [${chartPointageLabels}],
            colors: ['#00d2ad', '#ffbc4b', '#ff5e57'],
            stroke: { show: false },
            legend: { position: 'bottom' },
            plotOptions: { pie: { donut: { labels: { show: true, total: { show: true, label: 'Total' } } } } }
        }).render();
    }
</script>

</body>
</html>
