import java.sql.*;

/**
 * Vérification rapide de la connexion Oracle, hors conteneur.
 *
 * Aucun identifiant n'est écrit dans le fichier : ils sont lus dans les
 * variables d'environnement, les mêmes que celles des outils Python
 * (etl/test_connexion_oracle.py, etl/etl_agences.py).
 *
 *   BTK_DB_USER   défaut BTK_BI
 *   BTK_DB_DSN    défaut localhost:1521/FREEPDB1
 *   BTK_DB_PWD    obligatoire
 *
 * Utilisation :
 *   set BTK_DB_PWD=votre_mot_de_passe        (Windows)
 *   export BTK_DB_PWD=votre_mot_de_passe     (macOS / Linux)
 *   java -cp ojdbc11.jar TestDB
 *
 * Note : ceci teste Oracle seul. Si ce test passe mais que l'application
 * renvoie « IJ000453 », le problème est la datasource WildFly, pas la base —
 * voir tools/DEPANNAGE_ORACLE_WILDFLY.md.
 */
public class TestDB {

    private static String env(String nom, String defaut) {
        String v = System.getenv(nom);
        return (v == null || v.isBlank()) ? defaut : v;
    }

    public static void main(String[] args) {
        String user = env("BTK_DB_USER", "BTK_BI");
        String dsn = env("BTK_DB_DSN", "localhost:1521/FREEPDB1");
        String password = System.getenv("BTK_DB_PWD");
        if (password == null || password.isBlank()) {
            System.err.println("Definissez BTK_DB_PWD avec le mot de passe Oracle.");
            System.exit(1);
        }
        String url = "jdbc:oracle:thin:@" + dsn;

        System.out.println("Connexion a " + user + "@" + dsn + " ...");
        try (Connection conn = DriverManager.getConnection(url, user, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(
                     "SELECT SK_AGENCE, COUNT(*) AS CNT FROM B_UTILISATEURS GROUP BY SK_AGENCE")) {

            System.out.println("Connecte. " + conn.getMetaData().getDatabaseProductVersion());
            int agences = 0;
            while (rs.next()) {
                agences++;
                System.out.println("  SK_AGENCE " + rs.getString("SK_AGENCE")
                        + " : " + rs.getInt("CNT") + " employes");
            }
            System.out.println(agences + " agences lues.");

        } catch (SQLException e) {
            System.err.println("ECHEC : " + e.getMessage());
            String m = String.valueOf(e.getMessage());
            if (m.contains("ORA-01017")) {
                System.err.println("  -> identifiant ou mot de passe incorrect.");
            } else if (m.contains("ORA-12541") || m.contains("Connection refused")) {
                System.err.println("  -> Oracle n'est pas demarre, ou l'hote/le port sont faux.");
            } else if (m.contains("ORA-12514")) {
                System.err.println("  -> nom de service inconnu : essayez XEPDB1 ou ORCLPDB1.");
            } else if (m.contains("ORA-00942")) {
                System.err.println("  -> les tables ne sont pas visibles depuis le schema " + user
                        + " : GRANT SELECT, ou connectez-vous au schema proprietaire.");
            }
            System.exit(1);
        }
    }
}
