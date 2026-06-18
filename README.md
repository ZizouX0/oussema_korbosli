# Gestion des Agences — BTK Bank

A **Jakarta EE 10** web application for managing a bank's branch network
("gestion des agences"). It provides an administrative back-office for branches
(*agences*), employees, clients, commercial objectives, and a multi-level
request/approval workflow, on top of an Oracle database — branded for **BTK
Bank** (*Banque Tuniso-Koweïtienne*).

> The application code, UI labels, and database comments are in **French**, as
> it targets a French-speaking banking context.

---

## Tech stack

| Layer        | Technology |
|--------------|------------|
| Language     | Java 21 |
| Platform     | Jakarta EE 10 (Servlets, JSP/JSTL, EJB, JPA) |
| Persistence  | JPA / Hibernate over an **Oracle** database (JTA datasource) |
| Web tier     | `@WebServlet` controllers + JSP views (`WEB-INF/*.jsp`) |
| Business tier| `@Singleton` / EJB services injected via `@EJB` |
| Build        | Maven (`war` packaging) + Maven Wrapper (`mvnw`) |
| App server   | WildFly / JBoss EAP (context root `/gestion-agences`) |
| Front-end    | Server-rendered JSP, custom CSS, [ApexCharts](https://apexcharts.com/) dashboard charts |
| Analytics    | Oracle SQL views designed for **Power BI** reporting |

---

## Architecture

The project follows a classic layered Jakarta EE design:

```
Browser ──► Servlet (controller) ──► EJB Service ──► JPA EntityManager ──► Oracle DB
                     │
                     └──► forwards to JSP view (WEB-INF/*.jsp)
```

- **Controllers** (`src/main/java/controller`) — one `HttpServlet` per feature,
  mapped with `@WebServlet`. They read request params, call services, set request
  attributes, and forward to a JSP.
- **Services** (`src/main/java/service`) — EJBs holding business logic and JPQL
  queries via an injected `EntityManager`.
- **Entities** (`src/main/java/entity`) — JPA `@Entity` classes mapped to the
  bank's existing Oracle tables (`B_UTILISATEURS`, `AGENCE`, `CLIENT_BTK`,
  `B_OBJECTIF`, …).
- **Filter** (`src/main/java/filter/NotificationFilter`) — a `@WebFilter("/*")`
  that injects pending-request counts (notification badges) into every request
  based on the logged-in user's role.
- **Views** (`src/main/webapp`) — `index.jsp` (login) plus role-aware pages
  under `WEB-INF/` rendered through a shared `sidebar.jsp` / `top-bar.jsp`.

### Authentication & roles

Authentication is handled by `SecurityService` against a dedicated
`SECURITY_USERS` table. Three roles drive the UI and the approval workflow:

| Role                  | Capabilities |
|-----------------------|--------------|
| `ADMIN`               | Manages branches, employees, clients; approves client/employee creation requests. |
| `DIRECTEUR_COMMERCIAL`| Submits creation requests; approves employee data-modification requests. |
| `USER`                | Standard access; can submit modification requests for their own data. |

On login, a `SecurityUser` is linked to a business `Utilisateur`
(`B_UTILISATEURS`) to keep the workflow consistent.

### Request / approval workflows

The app models several asynchronous approval flows, each with an
`EN_ATTENTE → EN_COURS → EFFECTUE / REFUSE` lifecycle:

- **Client creation** — `DemandeClient` (`/demandes-agence`, `/demandes-admin`)
- **Employee creation** — `DemandeEmploye`
- **Employee data modification** — `DemandeModification` (`/gestion-demandes`)
- **Branch requests** — `DemandeAgence`

A `JournalAction` audit log records recent activity, and `Notification` /
`NotificationFilter` surface pending counts to the right role.

---

## Project structure

```
gestion-agences/
├── pom.xml                       # Maven build (Java 21, Jakarta EE 10, WAR)
├── mvnw, mvnw.cmd, .mvn/         # Maven Wrapper
├── sql/                          # Oracle schema + Power BI views (see below)
├── TestDB.java                   # Standalone JDBC connectivity smoke-test
└── src/main/
    ├── java/
    │   ├── controller/           # @WebServlet front controllers
    │   ├── service/              # EJB business services
    │   ├── entity/               # JPA entities
    │   └── filter/               # NotificationFilter
    ├── resources/META-INF/
    │   ├── persistence.xml        # JPA persistence unit (Oracle, JTA)
    │   └── beans.xml              # CDI
    └── webapp/
        ├── index.jsp              # Login page
        ├── forgot-password.jsp
        ├── css/style.css
        └── WEB-INF/               # Protected JSP views + web.xml + jboss-web.xml
```

---

## Database setup

The application expects an **Oracle** database (developed against Oracle XE /
`FREEPDB1`). The bank's core tables (`AGENCE`, `B_UTILISATEURS`, `CLIENT_BTK`,
`B_OBJECTIF`, …) are assumed to pre-exist; the scripts in [`sql/`](sql/) create
the additional tables, sequences, and reporting views this app introduces:

| Script | Purpose |
|--------|---------|
| `setup_security_db.sql`  | `SECURITY_USERS` table + sequence and default login accounts. |
| `setup_demandes.sql`     | `DEMANDE_CLIENT` and `DEMANDE_EMPLOYE` approval tables. |
| `setup_modifications.sql`| `DEMANDES_MODIFICATION` table for the data-change workflow. |
| `v_bi_clients.sql`       | `V_BI_CLIENTS` — client portfolio view for Power BI. |
| `v_bi_employes.sql`      | `V_BI_EMPLOYES` — workforce view for Power BI. |
| `v_bi_objectifs.sql`     | `V_BI_OBJECTIFS` — production/objectives view for Power BI. |

Run them with SQL*Plus / SQLcl / SQL Developer against your schema, e.g.:

```sql
@sql/setup_security_db.sql
@sql/setup_demandes.sql
@sql/setup_modifications.sql
@sql/v_bi_clients.sql
@sql/v_bi_employes.sql
@sql/v_bi_objectifs.sql
```

### Default login accounts

`setup_security_db.sql` seeds demo users (**plaintext passwords — change before
any real use**):

| Username    | Password    | Role |
|-------------|-------------|------|
| `admin`     | `admin`     | `ADMIN` |
| `directeur` | `directeur` | `DIRECTEUR_COMMERCIAL` |
| `user1`     | `user1`     | `USER` |
| `user2`     | `user2`     | `USER` |

---

## Configuration

Database access is configured in
[`src/main/resources/META-INF/persistence.xml`](src/main/resources/META-INF/persistence.xml).

By default it points the JPA properties directly at:

```
jdbc:oracle:thin:@localhost:1521/FREEPDB1   (user SYSTEM)
```

The persistence unit also declares a JTA datasource `java:/OracleDS`, so on
WildFly/JBoss you should define an `OracleDS` datasource (with the Oracle JDBC
driver / `ojdbc11`) and let the container manage transactions. Adjust the URL,
credentials, and dialect for your environment.

---

## Build & run

Requirements: **JDK 21**, an **Oracle** database, and a **WildFly / JBoss EAP**
server with the Oracle JDBC driver and an `OracleDS` datasource configured.

```bash
# Build the WAR (uses the bundled Maven Wrapper)
./mvnw clean package        # Windows: mvnw.cmd clean package
```

This produces `target/gestion-agences-1.0-SNAPSHOT.war`. Deploy it to WildFly
(e.g. copy into `$JBOSS_HOME/standalone/deployments/`) and open:

```
http://localhost:8080/gestion-agences/
```

> `TestDB.java` is a small standalone `main()` that opens a raw JDBC connection —
> handy for verifying Oracle connectivity outside the container.

---

## Reporting (Power BI)

The `V_BI_*` views flatten the operational schema into report-friendly shapes
(client portfolio, workforce by branch, and production/objectives by period and
branch) so they can be consumed directly from Power BI or any BI tool over the
Oracle connection.

---

## Notes

- The committed tree intentionally excludes build output (`target/`), IDE
  files (`.idea/`, `*.iml`), compiled classes (`*.class`), and IDE-generated
  HTML exports (`exportToHTML/`) — see [`.gitignore`](.gitignore). A stray
  duplicate controller (`AgenceServlet - Copie.java`, byte-identical to
  `AgenceServlet.java`) was also dropped because it broke compilation.
- Credentials in `persistence.xml` and `setup_security_db.sql` are
  development/demo defaults and **must not** be used in production.
