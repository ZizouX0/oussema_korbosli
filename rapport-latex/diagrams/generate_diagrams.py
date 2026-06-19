# -*- coding: utf-8 -*-
"""Generate the gestion-agences UML / architecture / BI diagrams (PlantUML).
All content is grounded in the real project (entities, services, servlets, SQL)."""
import os, subprocess
OUT = os.path.dirname(os.path.abspath(__file__))

STYLE = """
skinparam dpi 150
skinparam shadowing false
skinparam DefaultFontName Arial
skinparam DefaultFontSize 13
skinparam ArrowColor #14507A
skinparam roundCorner 6
"""

D = {}

# 1) USE CASE GLOBAL -------------------------------------------------------
D["uc_global"] = """@startuml
%s
left to right direction
skinparam packageStyle rectangle
skinparam actorStyle awesome
skinparam usecaseBackgroundColor #EAF3FA
skinparam usecaseBorderColor #1B6CA8
skinparam actorBorderColor #14507A
actor "Administrateur" as ADM
actor "Directeur commercial" as DIR
actor "Utilisateur" as USR
rectangle "Application de gestion des agences bancaires" {
  usecase "S'authentifier" as UC0
  usecase "Consulter le\\ntableau de bord" as UC1
  usecase "Gérer les agences" as UC2
  usecase "Gérer les employés" as UC3
  usecase "Gérer les clients" as UC4
  usecase "Consulter les\\nobjectifs" as UC5
  usecase "Soumettre une\\ndemande" as UC6
  usecase "Valider / refuser\\nune demande" as UC7
  usecase "Consulter le\\njournal d'audit" as UC8
  usecase "Recevoir des\\nnotifications" as UC9
}
ADM --> UC1
ADM --> UC2
ADM --> UC3
ADM --> UC4
ADM --> UC7
ADM --> UC8
ADM --> UC9
DIR --> UC1
DIR --> UC5
DIR --> UC6
DIR --> UC9
USR --> UC1
USR --> UC6
USR --> UC9
UC1 ..> UC0 : <<include>>
UC2 ..> UC0 : <<include>>
UC6 ..> UC0 : <<include>>
UC7 ..> UC0 : <<include>>
@enduml
""" % STYLE

# 2) CLASS DIAGRAM (faithful to the real JPA model) -----------------------
D["class"] = """@startuml
%s
skinparam classBackgroundColor #EAF3FA
skinparam classBorderColor #1B6CA8
skinparam classArrowColor #14507A
hide empty members

class Agence {
  -id : Long
  -nom : String
  -adresse : String
  -district : String
}
class Utilisateur {
  -id : Long
  -libelleUtilisateur : String
  -emailUtilisateur : String
  -estGestionnaire : Double
  -estSuspendu : Integer
  +getRoleLabel() : String
}
class Client {
  -id : Long
  -nomClient : String
  -typeClient : String
  -secteurActivite : String
  -statutClient : String
}
class Gestionnaire {
  -id : Long
  -nomComplet : String
  -email : String
}
class Objectif {
  -id : Long
  -anneeMois : String
  -productionCreditsConso : Double
  -souscriptionCompteCheques : Double
}
class SecurityUser {
  -id : Long
  -username : String
  -password : String
  -role : String
}
class DemandeClient {
  -id : Long
  -statut : String
  -dateCreation : Instant
}
class DemandeEmploye {
  -id : Long
  -nom : String
  -statut : String
}
class DemandeModification {
  -id : Long
  -champ : String
  -nouvelleVal : String
  -statut : String
}
class DemandeAgence {
  -id : Long
  -typeDemande : String
  -statut : String
}
class JournalAction {
  -id : Long
  -actionCode : String
  -dateAction : Instant
}
class Notification {
  -id : Long
  -typeNotif : String
  -lue : String
}

Agence "1" -- "0..*" Utilisateur : SK_AGENCE >
Agence "1" -- "0..*" Client : SK_AGENCE >
Agence "1" -- "0..*" Objectif : SK_AGENCE >
Gestionnaire "1" -- "0..*" Client : SK_GESTIONNAIRE >
Utilisateur "1" -- "0..*" Objectif : SK_UTILISATEUR >
DemandeClient "0..*" --> "1" Utilisateur : directeur
DemandeEmploye "0..*" --> "1" Utilisateur : directeur
DemandeModification "0..*" --> "1" Utilisateur : utilisateur
DemandeAgence "0..*" --> "1" Utilisateur : directeur
DemandeAgence "0..*" -- "0..*" Utilisateur : utilisateursDemandes
JournalAction "0..*" --> "1" Utilisateur
Notification "0..*" --> "1" Utilisateur : destinataire
SecurityUser ..> Utilisateur : <<authentifie>>
@enduml
""" % STYLE

# 3) SEQUENCE - AUTHENTIFICATION -----------------------------------------
D["seq_auth"] = """@startuml
%s
skinparam sequence {
  ArrowColor #14507A
  LifeLineBorderColor #1B6CA8
  ParticipantBorderColor #1B6CA8
  ParticipantBackgroundColor #EAF3FA
  ActorBorderColor #14507A
}
actor "Utilisateur" as U
participant "Navigateur" as NAV
participant "LoginServlet" as SRV
participant "SecurityService\\n(EJB)" as SEC
participant "UtilisateurService\\n(EJB)" as US
participant "EntityManager" as EM
database "Oracle" as DB
U -> NAV : saisir identifiant / mot de passe
NAV -> SRV : POST /login
activate SRV
SRV -> SEC : authenticate(username, password)
activate SEC
SEC -> EM : query SECURITY_USERS
EM -> DB : SELECT
DB --> EM : SecurityUser | null
SEC --> SRV : SecurityUser
deactivate SEC
alt authentification réussie
  SRV -> US : findOrCreate(username, role)
  US -> EM : find / persist Utilisateur
  EM -> DB : SELECT / INSERT
  SRV -> NAV : créer session + redirection /home
  NAV --> U : tableau de bord
else échec
  SRV -> NAV : message d'erreur
  NAV --> U : page de connexion
end
deactivate SRV
@enduml
""" % STYLE

# 4) SEQUENCE - VALIDATION D'UNE DEMANDE ----------------------------------
D["seq_demande"] = """@startuml
%s
skinparam sequence {
  ArrowColor #14507A
  LifeLineBorderColor #1B6CA8
  ParticipantBorderColor #1B6CA8
  ParticipantBackgroundColor #EAF3FA
  ActorBorderColor #14507A
}
actor "Administrateur" as ADM
participant "Navigateur" as NAV
participant "GestionModifications\\nServlet" as SRV
participant "DemandeModification\\nService (EJB)" as SVC
participant "JournalService\\n(EJB)" as JRN
participant "EntityManager" as EM
database "Oracle" as DB
ADM -> NAV : valider / refuser la demande
NAV -> SRV : POST /gestion-demandes (id, décision)
activate SRV
SRV -> SVC : traiter(id, décision, commentaire)
activate SVC
SVC -> EM : find(DemandeModification, id)
EM -> DB : SELECT
SVC -> SVC : statut = EFFECTUE / REFUSE
SVC -> EM : merge(demande)
EM -> DB : UPDATE
SVC -> JRN : journaliser(action)
JRN -> EM : persist(JournalAction)
EM -> DB : INSERT
SVC --> SRV : succès
deactivate SVC
SRV -> NAV : redirection + notification
deactivate SRV
NAV --> ADM : confirmation
@enduml
""" % STYLE

# 5) ETAT-TRANSITION - CYCLE DE VIE D'UNE DEMANDE -------------------------
D["state_demande"] = """@startuml
%s
skinparam state {
  BackgroundColor #EAF3FA
  BorderColor #1B6CA8
}
[*] --> EN_ATTENTE : création (directeur)
EN_ATTENTE --> EN_COURS : prise en charge (admin)
EN_ATTENTE --> REFUSE : refus
EN_COURS --> EFFECTUE : validation
EN_COURS --> REFUSE : refus
EFFECTUE --> [*]
REFUSE --> [*]
note right of EN_ATTENTE : statut initial\\n(table DEMANDES_*)
note right of EFFECTUE : action appliquée\\n+ journalisée
@enduml
""" % STYLE

# 6) ARCHITECTURE LOGIQUE (couches / composants) --------------------------
D["archi_logique"] = """@startuml
%s
skinparam componentStyle rectangle
skinparam rectangle {
  BorderColor #1B6CA8
  BackgroundColor #EAF3FA
}
skinparam databaseBackgroundColor #DCEAF5
skinparam databaseBorderColor #14507A
actor "Navigateur" as USER
rectangle "Couche Présentation" as L1 {
  [Pages JSP / JSTL]
  [Feuilles CSS]
  [Tableau de bord ApexCharts]
}
rectangle "Couche Contrôle" as L2 {
  [Servlets @WebServlet]
  [NotificationFilter]
}
rectangle "Couche Métier (EJB)" as L3 {
  [Services @Singleton / EJB]
}
rectangle "Couche Persistance" as L4 {
  [Entités JPA]
  [Hibernate]
}
database "Base Oracle" as DB
[Microsoft Power BI] as PBI #FFF3DC
USER --> L1 : HTTP
L1 --> L2 : requêtes
L2 --> L3 : appels de services
L3 --> L4 : EntityManager
L4 --> DB : JDBC / JTA
PBI ..> DB : vues V_BI_*
@enduml
""" % STYLE

# 7) ARCHITECTURE PHYSIQUE (deployment 3-tier) ----------------------------
D["archi_physique"] = """@startuml
%s
skinparam node {
  BorderColor #1B6CA8
  BackgroundColor #EAF3FA
}
skinparam databaseBackgroundColor #DCEAF5
skinparam databaseBorderColor #14507A
node "Poste client" as C {
  [Navigateur web]
}
node "Poste décisionnel" as P {
  [Power BI Desktop]
}
node "Serveur d'applications\\nWildFly / JBoss" as S {
  artifact "gestion-agences.war"
}
node "Serveur de base de données" as DBS {
  database "Oracle\\n(FREEPDB1)" as DB
}
C --> S : HTTP / HTTPS
S --> DBS : JDBC (datasource JTA OracleDS)
P --> DBS : connexion Oracle (vues V_BI_*)
@enduml
""" % STYLE

# 8) SCHEMA RELATIONNEL (ER) ----------------------------------------------
D["er"] = """@startuml
%s
skinparam linetype ortho
skinparam class {
  BackgroundColor #EAF3FA
  BorderColor #1B6CA8
}
hide circle
hide methods
entity "AGENCE" as AGENCE {
  *SK_AGENCE <<PK>>
  --
  LIBELLE_AGENCE
  ADRESSE_AGENCE
  DISTRICT
}
entity "B_UTILISATEURS" as USR {
  *SK_UTILISATEUR <<PK>>
  --
  LIBELLE_UTILISATEUR
  EMAIL_UTILISATEUR
  EST_GESTIONNAIRE
  EST_SUSPENDU
  #SK_AGENCE <<FK>>
}
entity "CLIENT" as CLI {
  *SK_CLIENT <<PK>>
  --
  NOM_CLIENT
  TYPE_CLIENT
  STATUT_CLIENT
  #SK_AGENCE <<FK>>
  #SK_GESTIONNAIRE <<FK>>
}
entity "B_OBJECTIF" as OBJ {
  *ID_OBJECTIF <<PK>>
  --
  ANNEE_MOIS
  #SK_AGENCE <<FK>>
  #SK_UTILISATEUR <<FK>>
}
entity "SECURITY_USERS" as SEC {
  *ID <<PK>>
  --
  USERNAME
  PASSWORD
  ROLE
}
entity "DEMANDE_CLIENT" as DC {
  *ID_DEMANDE <<PK>>
  --
  NOM_CLIENT
  STATUT
  #ID_DIRECTEUR <<FK>>
}
entity "DEMANDE_EMPLOYE" as DE {
  *ID_DEMANDE <<PK>>
  --
  NOM
  STATUT
  #ID_DIRECTEUR <<FK>>
}
entity "DEMANDES_MODIFICATION" as DM {
  *ID <<PK>>
  --
  CHAMP
  NOUVELLE_VAL
  STATUT
  #ID_USER <<FK>>
}
entity "JOURNAL_ACTION" as JA {
  *ID_JOURNAL <<PK>>
  --
  ACTION_CODE
  #ID_UTILISATEUR <<FK>>
}
AGENCE ||--o{ USR
AGENCE ||--o{ CLI
AGENCE ||--o{ OBJ
USR ||--o{ OBJ
USR ||--o{ DC
USR ||--o{ DE
USR ||--o{ DM
USR ||--o{ JA
@enduml
""" % STYLE

# 9) MODELE DECISIONNEL (star) --------------------------------------------
D["bi"] = """@startuml
%s
skinparam linetype ortho
skinparam class {
  BackgroundColor #FFF3DC
  BorderColor #C8861A
}
hide circle
hide methods
entity "DIM_AGENCE" as DA #EAF3FA {
  LIBELLE_AGENCE
  DISTRICT
}
entity "DIM_GESTIONNAIRE" as DG #EAF3FA {
  NOM_GESTIONNAIRE
}
entity "DIM_PERIODE" as DP #EAF3FA {
  ANNEE_MOIS
}
entity "DIM_CLIENT" as DCx #EAF3FA {
  TYPE_CLIENT
  STATUT
}
entity "V_BI_OBJECTIFS\\n(production)" as F1 {
  TOTAL_OUVERTURE_COMPTES
  CREDITS_CONSO / IMMO / INVEST
  COLLECTE_EPARGNE
}
entity "V_BI_EMPLOYES\\n(effectifs)" as F2 {
  ROLE_LABEL
  STATUT
}
entity "V_BI_CLIENTS\\n(portefeuille)" as F3 {
  NOM_COMPLET
}
DA ||--o{ F1
DG ||--o{ F1
DP ||--o{ F1
DA ||--o{ F2
DA ||--o{ F3
DCx ||--o{ F3
@enduml
""" % STYLE

# 10) GANTT / SPRINTS SCRUM -----------------------------------------------
D["gantt"] = """@startgantt
%s
printscale weekly
Project starts 2026-02-16
[Sprint 0 : cadrage et étude] as [S0] lasts 2 weeks
[S0] is colored in #1B6CA8/#EAF3FA
[Sprint 1 : authentification et sécurité] as [S1] lasts 2 weeks
[S1] starts at [S0]'s end
[Sprint 2 : gestion des agences et employés] as [S2] lasts 3 weeks
[S2] starts at [S1]'s end
[Sprint 3 : clients et objectifs] as [S3] lasts 3 weeks
[S3] starts at [S2]'s end
[Sprint 4 : workflow de demandes] as [S4] lasts 3 weeks
[S4] starts at [S3]'s end
[Sprint 5 : volet décisionnel (Power BI)] as [S5] lasts 2 weeks
[S5] starts at [S4]'s end
[S5] is colored in #C8861A/#FFF3DC
[Tests et rédaction] as [S6] lasts 2 weeks
[S6] starts at [S5]'s end
@endgantt
""" % STYLE

for name, content in D.items():
    open(os.path.join(OUT, name + ".puml"), "w", encoding="utf-8").write(content)
print("wrote", len(D), "puml files")
args = ["java", "-jar", "/tmp/plantuml.jar", "-tpng", "-charset", "UTF-8"] + \
       [os.path.join(OUT, n + ".puml") for n in D]
r = subprocess.run(args, capture_output=True, text=True)
print("STDERR:", r.stderr[-1500:] or "(none)")
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print("  ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
