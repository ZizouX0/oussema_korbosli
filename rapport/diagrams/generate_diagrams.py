# -*- coding: utf-8 -*-
"""Author the gestion-agences UML/BI/Gantt diagrams as PlantUML, then render."""
import os, subprocess
OUT = "/tmp/diagrams"
os.makedirs(OUT, exist_ok=True)

STYLE = """
skinparam shadowing false
skinparam DefaultFontName Arial
skinparam DefaultFontSize 13
skinparam ArrowColor #14507A
skinparam roundCorner 6
skinparam Padding 3
"""

diagrams = {}

# 1) USE CASE -------------------------------------------------------------
diagrams["usecase"] = """@startuml
%s
left to right direction
skinparam packageStyle rectangle
skinparam actorStyle awesome
skinparam usecaseBackgroundColor #EAF3FA
skinparam usecaseBorderColor #1B6CA8
skinparam actorBorderColor #14507A
skinparam actorBackgroundColor #DCEAF5

actor "Administrateur" as ADM
actor "Directeur commercial" as DIR
actor "Utilisateur" as USR

rectangle "Application de gestion des agences bancaires" {
  usecase "S'authentifier" as UC0
  usecase "Consulter le\\ntableau de bord" as UC1
  usecase "Gérer les agences" as UC2
  usecase "Gérer les employés" as UC3
  usecase "Gérer les clients" as UC4
  usecase "Gérer les objectifs" as UC5
  usecase "Soumettre une\\ndemande" as UC6
  usecase "Valider / refuser\\nune demande" as UC7
  usecase "Consulter le\\njournal d'audit" as UC8
}

ADM --> UC1
ADM --> UC2
ADM --> UC3
ADM --> UC4
ADM --> UC7
ADM --> UC8
DIR --> UC1
DIR --> UC5
DIR --> UC6
DIR --> UC7
USR --> UC1
USR --> UC6

UC1 ..> UC0 : <<include>>
UC2 ..> UC0 : <<include>>
UC6 ..> UC0 : <<include>>
UC7 ..> UC0 : <<include>>
@enduml
""" % STYLE

# 2) ARCHITECTURE (layered) ----------------------------------------------
diagrams["architecture"] = """@startuml
%s
skinparam componentStyle rectangle
skinparam rectangle {
  BorderColor #1B6CA8
  BackgroundColor #EAF3FA
}
skinparam databaseBackgroundColor #DCEAF5
skinparam databaseBorderColor #14507A

actor "Navigateur\\n(Client web)" as USER

rectangle "Couche Présentation" as L1 {
  [Pages JSP / JSTL]
  [Feuilles de style CSS]
  [Tableau de bord ApexCharts]
}
rectangle "Couche Contrôle" as L2 {
  [Servlets @WebServlet]
  [NotificationFilter]
}
rectangle "Couche Métier (EJB)" as L3 {
  [Services métier\\n(@Singleton / EJB)]
}
rectangle "Couche Persistance" as L4 {
  [Entités JPA]
  [Hibernate]
}
database "Base de données\\nOracle" as DB
[Microsoft Power BI] as PBI #FFF3DC

USER --> L1 : HTTP
L1 --> L2 : requêtes
L2 --> L3 : appels de services
L3 --> L4 : EntityManager
L4 --> DB : JDBC / JTA
PBI ..> DB : vues V_BI_*
@enduml
""" % STYLE

# 3) CLASS DIAGRAM --------------------------------------------------------
diagrams["classes"] = """@startuml
%s
skinparam classBackgroundColor #EAF3FA
skinparam classBorderColor #1B6CA8
skinparam classArrowColor #14507A

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
class Gestionnaire {
  -id : Long
  -nom : String
}
class Client {
  -id : Long
  -nomClient : String
  -typeClient : String
  -secteurActivite : String
  -statutClient : String
}
class Objectif {
  -idObjectif : Long
  -anneeMois : String
  -productionCredits : Double
  -souscriptionComptes : Double
}
class Banque {
  -id : Long
  -libelle : String
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
  -dateCreation : Date
}
class DemandeEmploye {
  -id : Long
  -statut : String
}
class DemandeModification {
  -id : Long
  -champ : String
  -ancienneVal : String
  -nouvelleVal : String
  -statut : String
}
class JournalAction {
  -id : Long
  -action : String
  -dateAction : Date
}
class Notification {
  -id : Long
  -message : String
}

Agence "1" -- "*" Utilisateur : rattache >
Agence "1" -- "*" Client : gère >
Agence "1" -- "*" Objectif : suit >
Gestionnaire "1" -- "*" Client : encadre >
Utilisateur "1" -- "*" Objectif : réalise >
Utilisateur "1" -- "*" DemandeClient : soumet >
Utilisateur "1" -- "*" DemandeEmploye : soumet >
Utilisateur "1" -- "*" DemandeModification : soumet >
Utilisateur "1" -- "*" JournalAction : génère >
Banque "1" -- "*" Agence : possède >
SecurityUser ..> Utilisateur : authentifie
@enduml
""" % STYLE

# 4) SEQUENCE -------------------------------------------------------------
diagrams["sequence"] = """@startuml
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
participant "EntityManager\\n(JPA)" as EM
database "Oracle" as DB
participant "JournalService" as JRN

ADM -> NAV : clic « Valider la demande »
NAV -> SRV : POST /gestion-demandes (id, décision)
activate SRV
SRV -> SVC : traiter(id, décision, commentaire)
activate SVC
SVC -> EM : find(DemandeModification, id)
EM -> DB : SELECT
DB --> EM : demande
SVC -> SVC : statut = EFFECTUÉ / REFUSÉ
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

# 5) ER / RELATIONAL SCHEMA ----------------------------------------------
diagrams["er"] = """@startuml
%s
skinparam linetype ortho
skinparam class {
  BackgroundColor #EAF3FA
  BorderColor #1B6CA8
}
hide circle
hide methods

entity "AGENCE" as AGENCE {
  *SK_AGENCE : NUMBER <<PK>>
  --
  LIBELLE_AGENCE
  ADRESSE_AGENCE
  DISTRICT
}
entity "B_UTILISATEURS" as USR {
  *SK_UTILISATEUR : NUMBER <<PK>>
  --
  LIBELLE_UTILISATEUR
  EMAIL_UTILISATEUR
  EST_GESTIONNAIRE
  EST_SUSPENDU
  #SK_AGENCE <<FK>>
}
entity "CLIENT_BTK" as CLI {
  *SK_CLIENT : NUMBER <<PK>>
  --
  NOM_CLIENT
  TYPE_CLIENT
  SECTEUR_ACTIVITE
  STATUT_CLIENT
  #SK_AGENCE <<FK>>
}
entity "B_OBJECTIF" as OBJ {
  *ID_OBJECTIF : NUMBER <<PK>>
  --
  ANNEE_MOIS
  #SK_AGENCE <<FK>>
  #SK_UTILISATEUR <<FK>>
}
entity "SECURITY_USERS" as SEC {
  *ID : NUMBER <<PK>>
  --
  USERNAME
  PASSWORD
  ROLE
}
entity "DEMANDE_CLIENT" as DC {
  *ID_DEMANDE : NUMBER <<PK>>
  --
  NOM_CLIENT
  STATUT
  #ID_DIRECTEUR <<FK>>
}
entity "DEMANDE_EMPLOYE" as DE {
  *ID_DEMANDE : NUMBER <<PK>>
  --
  NOM
  STATUT
  #ID_DIRECTEUR <<FK>>
}
entity "DEMANDES_MODIFICATION" as DM {
  *ID : NUMBER <<PK>>
  --
  CHAMP
  NOUVELLE_VAL
  STATUT
  #ID_USER <<FK>>
}

AGENCE ||--o{ USR
AGENCE ||--o{ CLI
AGENCE ||--o{ OBJ
USR ||--o{ OBJ
USR ||--o{ DC
USR ||--o{ DE
USR ||--o{ DM
@enduml
""" % STYLE

# 6) BI STAR MODEL --------------------------------------------------------
diagrams["bi"] = """@startuml
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
entity "DIM_CLIENT" as DC #EAF3FA {
  TYPE_CLIENT
  STATUT
}

entity "V_BI_OBJECTIFS\\n(faits production)" as F1 {
  TOTAL_OUVERTURE_COMPTES
  CREDITS_CONSO / IMMO / INVEST
  CARTES_COMMANDES
  COLLECTE_EPARGNE
}
entity "V_BI_EMPLOYES\\n(faits effectifs)" as F2 {
  ROLE_LABEL
  STATUT
}
entity "V_BI_CLIENTS\\n(faits clients)" as F3 {
  NOM_COMPLET
}

DA ||--o{ F1
DG ||--o{ F1
DP ||--o{ F1
DA ||--o{ F2
DA ||--o{ F3
DC ||--o{ F3
@enduml
""" % STYLE

# 7) GANTT ----------------------------------------------------------------
diagrams["gantt"] = """@startgantt
%s
printscale weekly
Project starts 2026-02-02
[Étude de l'existant et analyse] as [E] lasts 3 weeks
[E] is colored in #1B6CA8/#EAF3FA
[Spécification des besoins] as [S] lasts 2 weeks
[S] starts at [E]'s end
[Conception] as [C] lasts 3 weeks
[C] starts at [S]'s end
[C] is colored in #1B6CA8/#EAF3FA
[Développement des modules] as [D] lasts 5 weeks
[D] starts at [C]'s end
[D] is colored in #14507A/#DCEAF5
[Volet décisionnel (Power BI)] as [B] lasts 3 weeks
[B] starts at [D]'s end
[B] is colored in #C8861A/#FFF3DC
[Tests et validation] as [T] lasts 2 weeks
[T] starts at [B]'s end
[Rédaction du rapport] as [R] lasts 5 weeks
[R] starts at [C]'s end
@endgantt
""" % STYLE

for name, content in diagrams.items():
    with open(f"{OUT}/{name}.puml", "w", encoding="utf-8") as f:
        f.write(content)
print("wrote", len(diagrams), "puml files")

# render all to PNG
r = subprocess.run(
    ["java", "-jar", "/tmp/plantuml.jar", "-tpng", "-charset", "UTF-8",
     f"{OUT}/usecase.puml", f"{OUT}/architecture.puml", f"{OUT}/classes.puml",
     f"{OUT}/sequence.puml", f"{OUT}/er.puml", f"{OUT}/bi.puml", f"{OUT}/gantt.puml"],
    capture_output=True, text=True)
print("STDOUT:", r.stdout[-1000:])
print("STDERR:", r.stderr[-2000:])
print("\n=== rendered files ===")
for f in sorted(os.listdir(OUT)):
    if f.endswith(".png"):
        print(" ", f, os.path.getsize(f"{OUT}/{f}"), "bytes")
