# « Unable to get managed connection for java:/OracleDS » — que faire

Symptôme, à l'ouverture de <http://localhost:8080/gestion-agences/> :

```
jakarta.ejb.EJBException: org.hibernate.exception.GenericJDBCException:
  Unable to acquire JDBC Connection
  [jakarta.resource.ResourceException: IJ000453: Unable to get managed connection
   for java:/OracleDS]
```

**Ce que cela veut dire.** Le code et le déploiement sont bons : WildFly a bien
trouvé la datasource `java:/OracleDS`, mais son pool n'arrive pas à **ouvrir une
connexion vers Oracle**. Si la datasource était absente, l'erreur serait une
`NameNotFoundException` au déploiement, pas `IJ000453`.

Il y a donc deux familles de causes : **Oracle n'est pas joignable**, ou **la
datasource pointe au mauvais endroit**. L'étape A tranche entre les deux en une
commande.

---

## Étape A — Oracle ou WildFly ?

Depuis le dossier du projet :

```bash
python3 etl/test_connexion_oracle.py
```

Ce test ouvre une connexion Oracle **sans passer par WildFly**, avec les mêmes
paramètres que l'application.

| Résultat | Conclusion | Suite |
|---|---|---|
| le test échoue | Oracle n'est pas joignable | **étape B** |
| le test réussit | Oracle va bien, c'est la datasource | **étape C** |

---

## Étape B — Rendre Oracle joignable

### B1. Les services sont-ils démarrés ?

Windows, `services.msc` — les deux doivent être *En cours d'exécution* :

- `OracleServiceFREE` (ou `OracleServiceXE`) ;
- `OracleOraDB…TNSListener`.

```bash
lsnrctl status
```

La sortie doit lister un service `freepdb1`. Si le nom diffère (`xepdb1`,
`orclpdb1`), c'est celui-là qu'il faudra mettre partout — y compris dans l'URL
de la datasource, à l'étape C.

### B2. La base pluggable est-elle *ouverte* ?

**C'est la cause la plus fréquente après un redémarrage du poste** : le
conteneur démarre, mais la base pluggable reste en `MOUNTED` — donc injoignable,
alors même que le listener répond.

```sql
sqlplus / as sysdba

SELECT name, open_mode FROM v$pdbs;
```

Si `FREEPDB1` est en `MOUNTED` :

```sql
ALTER PLUGGABLE DATABASE FREEPDB1 OPEN;
ALTER PLUGGABLE DATABASE FREEPDB1 SAVE STATE;   -- s'ouvrira seule au prochain démarrage
```

`SAVE STATE` évite d'avoir à refaire la manœuvre à chaque redémarrage.

### B3. Les identifiants

Utilisateur `BTK_BI`, service `localhost:1521/FREEPDB1`. Un compte verrouillé se rouvre avec :

```sql
ALTER USER BTK_BI ACCOUNT UNLOCK;
```

Quand `etl/test_connexion_oracle.py` répond `Connecté`, passer à l'étape C.

---

## Étape C — Réparer la datasource WildFly

### C1. Interroger le pool

```bash
# Linux / macOS
$WILDFLY_HOME/bin/jboss-cli.sh --connect --file=tools/setup-oracle-datasource.cli

# Windows
%WILDFLY_HOME%\bin\jboss-cli.bat --connect --file=tools\setup-oracle-datasource.cli
```

Le script affiche la configuration en place puis teste la connexion. La réponse
utile est celle de `test-connection-in-pool` :

- `"outcome" => "success"` — le pool fonctionne ; s'il reste une erreur dans
  l'application, elle est ailleurs (voir C4) ;
- `"outcome" => "failed"` — le message qui suit donne la cause exacte, dans le
  même vocabulaire qu'à l'étape B (`ORA-01017`, `ORA-12541`, `ORA-12514`…).

### C2. Comparer avec ce qui a marché à l'étape A

Dans la sortie de `read-resource`, vérifier trois attributs :

| Attribut | Valeur attendue |
|---|---|
| `connection-url` | `jdbc:oracle:thin:@localhost:1521/FREEPDB1` |
| `user-name` | `BTK_BI` |
| `password` | le mot de passe de la base |

Le service en fin d'URL doit être **exactement** celui vu dans `lsnrctl status`.

### C3. Corriger, puis recharger

```bash
$WILDFLY_HOME/bin/jboss-cli.sh --connect
```

```
/subsystem=datasources/data-source=OracleDS:write-attribute(name=connection-url,value="jdbc:oracle:thin:@localhost:1521/FREEPDB1")
/subsystem=datasources/data-source=OracleDS:write-attribute(name=user-name,value="BTK_BI")
/subsystem=datasources/data-source=OracleDS:write-attribute(name=password,value="VOTRE_MOT_DE_PASSE")
reload
/subsystem=datasources/data-source=OracleDS:test-connection-in-pool
```

`reload` est indispensable : sans lui, la modification n'est pas appliquée au
pool.

### C4. Oracle était arrêté puis a redémarré

Le pool garde alors des connexions mortes et continue de renvoyer `IJ000453`
même une fois Oracle revenu. Il faut le vider :

```
/subsystem=datasources/data-source=OracleDS:flush-all-connection-in-pool
/subsystem=datasources/data-source=OracleDS:test-connection-in-pool
```

### C5. Si le pilote Oracle manque

Ce n'est pas le cas ici — `IJ000453` prouve que la datasource est déclarée —
mais pour mémoire, la méthode la plus simple est de **déployer le pilote** :
copier `ojdbc11.jar` dans `$WILDFLY_HOME/standalone/deployments/`. WildFly
l'enregistre alors comme pilote sous le nom `ojdbc11.jar`, sans avoir à créer de
module.

---

## Pour que le problème ne revienne pas

Après un redémarrage du poste, dans l'ordre :

1. démarrer Oracle (services Windows) ;
2. vérifier que la PDB est `READ WRITE` — le `SAVE STATE` de l'étape B2 s'en
   charge une fois pour toutes ;
3. démarrer WildFly ;
4. ouvrir <http://localhost:8080/gestion-agences/>.

WildFly démarré **avant** Oracle fonctionne aussi : le pool crée ses connexions
à la demande. Mais si une page a déjà été ouverte pendant qu'Oracle était
absent, vider le pool (C4).

Détail des paramètres de connexion et des codes d'erreur Oracle :
[`etl/CONNEXION_ORACLE.md`](../etl/CONNEXION_ORACLE.md).
