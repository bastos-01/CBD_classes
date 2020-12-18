import com.datastax.oss.driver.api.core.CqlSession;
import com.datastax.oss.driver.api.core.cql.*;
import com.datastax.oss.driver.api.core.cql.Row;
import org.apache.spark.sql.*;

public class queries {

    public static void main(String[] args) {

        try (CqlSession session = CqlSession.builder().withKeyspace("videos").build()) {

            System.out.println("Os últimos 3 comentários introduzidos para um vídeo: ");
            querie1(session);

            System.out.println("\n\nTodos os vídeos com a tag 'work': ");
            querie2(session);

            System.out.println("\n\nVídeos partilhados por determinado utilizador (maria1987, por exemplo) num determinado período de tempo (Agosto de 2017, por exemplo): ");
            querie3(session);

            System.out.println("\n\nTodos os seguidores (followers) de determinado vídeo: ");
            querie4(session);

        }
    }

    private static void querie1(CqlSession session) {
        ResultSet rs = session.execute(SimpleStatement.builder("select * from comment_by_video where videoId=1 limit 3").build());

        for (Row row: rs)
            System.out.format("%3s | %30s | %15s | %30s\n", row.getInt("videoid"), row.getObject("comment_date"), row.getString("author"), row.getString("comment"));
    }

    private static void querie2(CqlSession session) {
        ResultSet rs = session.execute(SimpleStatement.builder("select * from video where tag contains 'work' allow filtering").build());

        for (Row row: rs)
            System.out.format("%3s | %15s | %60s | %50s | %30s | %30s\n", row.getInt("id"), row.getString("author"),
                                                    row.getString("description"), row.getString("name"),
                                                    row.getSet("tag", String.class) ,row.getObject("upload_date"));
    }

    private static void querie3(CqlSession session) {
        ResultSet rs = session.execute(SimpleStatement.builder("select * from video where author='bastitos' and upload_date > '2010-06-03' and upload_date < '2015-12-12'  allow filtering").build());

        for (Row row: rs)
            System.out.format("%3s | %15s | %60s | %50s | %30s | %30s\n", row.getInt("id"), row.getString("author"),
                    row.getString("description"), row.getString("name"),
                    row.getSet("tag", String.class) ,row.getObject("upload_date"));
    }

    private static void querie4(CqlSession session) {
        ResultSet rs = session.execute(SimpleStatement.builder("select * from follower where video_id=7").build());

        for (Row row: rs)
            System.out.format("%3s | %15s\n", row.getInt("video_id"), row.getSet("user", String.class));
    }
}
