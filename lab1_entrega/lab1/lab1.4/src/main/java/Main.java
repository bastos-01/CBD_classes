import redis.clients.jedis.Jedis;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.Buffer;
import java.util.*;


public class Main {

    public static void main(String[] args) throws IOException {

        //alinea a)
        FileReader fr = null;

        try{
            fr = new FileReader(new File("female-names.txt"));
        }catch (Exception e){
            e.printStackTrace();
        }

        BufferedReader br = new BufferedReader(fr);
        String line;
        SetPost redisList = new SetPost();

        while((line = br.readLine()) != null){
            redisList.saveUser(line);
        }

        System.out.println("a) -----------------------");
        Scanner sc = new Scanner(System.in);
        while(true) {
            System.out.print("Search for ('Enter') for quit): ");
            String input_name = sc.nextLine();

            if(input_name.length() == 0)
                break;

            Set<String> resposta = redisList.getUser(input_name);
            System.out.println(input_name);
            for (String s : resposta)
                System.out.println(s);
        }

        //alinea b)
        SetPostCsv csvList = new SetPostCsv();
        System.out.println("\nb) -----------------------");
        BufferedReader csvReader = new BufferedReader(new FileReader(new File("nomes-registados-2020.csv")));
        String row;
        while ((row = csvReader.readLine()) != null) {
            String[] data = row.split(";");
            csvList.saveUser(data[0], Integer.parseInt(data[2]));
        }
        csvReader.close();

        while(true) {
            System.out.print("Search for ('Enter') for quit): ");
            String input_name2 = sc.nextLine();

            if(input_name2.length() == 0)
                break;

            Set<String> resposta2 = csvList.getUser();
            for (String s : resposta2)
                if (s.toLowerCase().matches(input_name2 + "(.*)"))
                    System.out.println(s);
        }
        sc.close();

    }
}

class SetPost{
    private Jedis jedis;
    public static String USERS = "femaleNames"; // Key set for users' name

    public SetPost() {
        this.jedis = new Jedis("localhost");
    }
    public void saveUser(String username) {
        jedis.zadd(USERS, 0 , username);
    }
    public Set<String> getUser(String search) {
        return jedis.zrangeByLex(USERS, "[" + search + "*", "[" + search + (char)0xFF);
    }
    public Set<String> getAllKeys() {
        return jedis.keys("*");
    }
    public void flushAll(){
        jedis.flushAll();
    }
}

class SetPostCsv{
    private Jedis jedis;
    public static String USERS = "femaleNames2"; // Key set for users' name

    public SetPostCsv() {
        this.jedis = new Jedis("localhost");
    }
    public void saveUser(String username, int score) {
        jedis.zadd(USERS, score , username);
    }
    public Set<String> getUser() {
        return jedis.zrevrange(USERS,0,-1);
    }
    public Set<String> getAllKeys() {
        return jedis.keys("*");
    }
    public void flushAll(){
        jedis.flushAll();
    }
}
