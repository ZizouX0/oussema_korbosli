import java.sql.*;

public class TestDB {
    public static void main(String[] args) {
        String url = "jdbc:oracle:thin:@localhost:1521/FREEPDB1";
        String user = "SYSTEM";
        String password = "root";

        try (Connection conn = DriverManager.getConnection(url, user, password);
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT SK_AGENCE, COUNT(*) as cnt FROM B_UTILISATEURS GROUP BY SK_AGENCE")) {
            System.out.println("Connected.");
            while (rs.next()) {
                System.out.println("SK_AGENCE: " + rs.getString("SK_AGENCE") + ", Count: " + rs.getInt("cnt"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
