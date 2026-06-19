# Guide du code — application gestion-agences (BTK)

Ce document explique **comment le code est organisé et comment il fonctionne**,
pour comprendre et présenter facilement le projet. Il ne change rien au
comportement de l'application : c'est une aide à la lecture.

---

## 1. Vue d'ensemble

Application web **Jakarta EE 10** (Java 21) de gestion d'un réseau d'agences
bancaires, avec un volet décisionnel (Business Intelligence).

| Brique | Technologie |
|---|---|
| Vues (pages) | JSP / JSTL + CSS + ApexCharts |
| Contrôleurs | Servlets (`@WebServlet`) |
| Logique métier | EJB (`@Stateless` / `@Singleton`) |
| Persistance | JPA / Hibernate |
| Base de données | Oracle |
| Serveur | WildFly / JBoss (archive **WAR**) |
| Reporting | Power BI (vues `V_BI_*`) |

---

## 2. Architecture en couches (très important pour la soutenance)

Chaque requête traverse **4 couches** bien séparées :

```
Navigateur
   │  HTTP
   ▼
[1] Présentation   src/main/webapp/**.jsp  (+ css/style.css, ApexCharts)
   │
   ▼
[2] Contrôle       src/main/java/controller/*Servlet.java   (@WebServlet)
   │   appelle un service
   ▼
[3] Métier (EJB)   src/main/java/service/*Service.java      (@Stateless)
   │   EntityManager (JPA)
   ▼
[4] Persistance    src/main/java/entity/*.java  +  Hibernate
   │   JDBC / JTA
   ▼
Base Oracle
```

**Idée clé :** un Servlet ne contient **pas** de logique métier ni de SQL ; il
lit la requête, appelle un **Service**, puis renvoie une **JSP**. Toute la
logique et les requêtes (JPQL) sont dans les **Services**. Les **entités** ne
font que représenter les tables.

---

## 3. Organisation des packages (`src/main/java`)

| Package | Rôle | Exemples |
|---|---|---|
| `controller` | Reçoit les requêtes HTTP, appelle les services, choisit la JSP. | `HomeServlet`, `AgenceServlet`, `PointageServlet`, `LoginServlet` |
| `service` | Logique métier + requêtes JPQL via `EntityManager`. | `UtilisateurService`, `PointageService`, `SecurityService`, `JournalService` |
| `entity` | Classes JPA = tables de la base. | `Utilisateur`, `Agence`, `Client`, `Objectif`, `Pointage` |
| `filter` | Traitement transversal avant les servlets. | `NotificationFilter` (compte les demandes en attente) |

Vues : `src/main/webapp/WEB-INF/*.jsp` (protégées) + `index.jsp` (login).
Configuration : `WEB-INF/web.xml`, `WEB-INF/jboss-web.xml`,
`META-INF/persistence.xml` (connexion BD + liste des entités).

---

## 4. Flux complet d'une requête (exemple : afficher les agences)

1. L'utilisateur clique « Gérer les Agences » → le navigateur appelle `/agences`.
2. `AgenceServlet.doGet()` vérifie la **session** et le **rôle** (`ADMIN`).
3. Il appelle `agenceService.findAll()`.
4. `AgenceService` exécute une requête JPQL via l'`EntityManager` → Hibernate →
   SQL → Oracle → renvoie une `List<Agence>`.
5. Le servlet place la liste dans la requête (`setAttribute`) et **forward** vers
   `WEB-INF/agences.jsp`.
6. La JSP affiche la liste (boucle `<c:forEach>`).

C'est **le même schéma pour tous les modules** (employés, clients, objectifs,
demandes, pointage).

---

## 5. Sécurité et rôles

- `LoginServlet` → `SecurityService.authenticate()` vérifie l'identifiant/mot de
  passe dans la table `SECURITY_USERS`, puis ouvre une **session** avec le rôle.
- 3 rôles : `ADMIN`, `DIRECTEUR_COMMERCIAL`, `USER`. Chaque servlet **vérifie le
  rôle au début** de `doGet`/`doPost` ; les JSP masquent/affichent selon le rôle
  (`<c:if test="${sessionScope.role == 'ADMIN'}">`).
- `JournalService.log(...)` enregistre les actions importantes (audit) dans
  `JOURNAL_ACTION`.

---

## 6. Le module de pointage (nouveau)

But : suivre la **présence des employés** (arrivée, départ, statut).

| Fichier | Rôle |
|---|---|
| `entity/Pointage.java` | Table `POINTAGE` : employé, date, heure d'arrivée/départ, statut, source. |
| `service/PointageService.java` | Pointer arrivée/départ (heure système, **retard** au-delà de 9h), saisie manuelle, comptages pour le BI. |
| `controller/PointageServlet.java` | URL `/pointage` : boutons employé + formulaire manuel (admin). |
| `WEB-INF/pointage.jsp` | Page : mon pointage du jour, saisie manuelle, historique. |
| `sql/setup_pointage.sql` | Crée la table, la séquence et la **vue BI** `V_BI_POINTAGE`. |

Statuts possibles : `PRESENT`, `RETARD`, `ABSENT` (cycle de vie simple).

---

## 7. Le tableau de bord (`/home`)

- `HomeServlet` **calcule les indicateurs** (employés, clients, demandes en
  attente, **présents du jour / taux de présence** via `PointageService`) et
  prépare les **données des graphiques** (séries pour ApexCharts), puis forward
  vers `home.jsp`.
- `home.jsp` affiche :
  - une **rangée de KPI** (cartes chiffres) ;
  - des **graphiques ApexCharts** : effectif par agence (barres), répartition des
    rôles (donut), **présence du jour** (donut) ;
  - des raccourcis de navigation.

Pour ajouter un indicateur : 1) une méthode de comptage dans le `Service`,
2) un `request.setAttribute(...)` dans `HomeServlet`, 3) l'affichage dans
`home.jsp`.

---

## 8. Base de données et scripts (`sql/`)

| Script | Contenu |
|---|---|
| `setup_security_db.sql` | Table `SECURITY_USERS` + comptes par défaut. |
| `setup_demandes.sql` | Tables des demandes (clients, employés). |
| `setup_modifications.sql` | Table des demandes de modification. |
| `setup_pointage.sql` | Table `POINTAGE` + vue `V_BI_POINTAGE`. |
| `v_bi_clients.sql`, `v_bi_employes.sql`, `v_bi_objectifs.sql` | Vues décisionnelles pour Power BI. |

> Les **vues `V_BI_*`** « aplatissent » les données pour Power BI (un fait +
> des dimensions agence/période/…), sans alourdir les tables de production.

---

## 9. Lancer le projet (rappel)

1. Oracle : exécuter les scripts `sql/` (dont `setup_pointage.sql`).
2. WildFly : datasource `java:/OracleDS` + driver Oracle.
3. `mvn package` → déployer `target/gestion-agences-1.0-SNAPSHOT.war`.
4. Ouvrir `http://localhost:8080/gestion-agences/`.

---

### Mémo « où est quoi ? »
- *« Je veux changer une page »* → `webapp/WEB-INF/<page>.jsp`
- *« Je veux changer une règle métier / une requête »* → `service/<X>Service.java`
- *« Je veux ajouter un champ en base »* → `entity/<X>.java` + le script SQL
- *« Je veux une nouvelle page »* → un `Servlet` + une `JSP` + un lien dans `sidebar.jsp`
