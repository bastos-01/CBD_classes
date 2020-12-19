import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.*;
import java.sql.Timestamp;

public class teste {

    public static void main(String[] args) {

        try (CqlSession session = CqlSession.builder().withKeyspace("videos").build()) {

            System.out.println("Search for users: ");
            getUsers(session);

            System.out.println("\nInserting a value in user.");
            setUser(session, "JavaInsert", "Java", "javainsert@ua.pt");
            System.out.println("Checking if new user exists: ");
            getUser(session, "JavaInsert");

            System.out.println("\nEditing name of user \"JavaInsert\".");
            updateUser(session, "JavaInsert", "AnotherName");
            System.out.println("Checking if the name changed: ");
            getUser(session, "JavaInsert");

            System.out.println("\nDeleting user \"JavaInsert\".");
            deleteUser(session, "JavaInsert");
            System.out.println("Checking if user was deleted: ");
            getUser(session, "JavaInsert");

        }
    }

    // get all users
    private static void getUsers(CqlSession session) {
        ResultSet rs = session.execute(SimpleStatement.builder("SELECT * FROM user").build());

        for (Row row: rs)
            System.out.format("%s - %s - %s\n", row.getString("username"), row.getString("name"), row.getString("email"));
    }

    // get specific user
    private static void getUser(CqlSession session, String username) {
        try {
            ResultSet rs = session.execute(SimpleStatement.builder("SELECT * FROM user WHERE username=?").addPositionalValue(username).build());

            Row row = rs.one();
            System.out.format("%s - %s - %s\n", row.getString("username"), row.getString("name"), row.getString("email"));
        }
        catch (Exception QueryExecutionException){
            System.out.println("User not found!");
        }
    }

    // insert user
    private static void setUser(CqlSession session, String username,  String name, String email) {
        session.execute(SimpleStatement.builder( "insert into user (username, name, email) values (?,?,?)").addPositionalValues(username, name, email).build());
    }

    // update name of user
    private static void updateUser(CqlSession session, String username, String name) {
        session.execute(SimpleStatement.builder("UPDATE user SET name=?  WHERE username=?").addPositionalValues(name, username).build());
    }

    // delete user
    private static void deleteUser(CqlSession session, String username) {
        session.execute(SimpleStatement.builder("DELETE FROM user WHERE username=?").addPositionalValue(username).build());

    }



}
