package redis;

import redis.clients.jedis.Jedis;

import java.util.*;


public class App {

    public static void main(String[] args) {

        //with list
        ListPost redisList = new ListPost();

        List<String> lista = new ArrayList<>();
        lista.add("Antonio");
        lista.add("Pedro");
        lista.add("Jose");
        lista.add("Carolina");

        for (String u : lista)
            redisList.saveUser(u);

        System.out.println("\n------------ USANDO LIST ------------");
        System.out.println("\nLista de keys:");
        redisList.getAllKeys().stream().forEach(System.out::println);

        System.out.println("\nLista de users:");
        redisList.getUser().stream().forEach(System.out::println);

        //apagar a base de dados
        redisList.flushAll();

        //with Hashmap
        HashMapPost redisHashMap = new HashMapPost();

        Map<String, String> hashmap = new HashMap<>();
        hashmap.put("User1", "Ana");
        hashmap.put("User2", "Pedro");
        hashmap.put("User3", "Maria");
        hashmap.put("User4", "Luis");

        redisHashMap.saveUser(hashmap);

        System.out.println("\n------------ USANDO HASHMAP ------------");
        System.out.println("\nLista de keys:");
        redisHashMap.getAllKeys().stream().forEach(System.out::println);

        System.out.println("\nLista de users:");
        Map<String, String> map_users = redisHashMap.getUser();
        for(String key: map_users.keySet())
            System.out.println(map_users.get(key));
        System.out.println();

        //apagar a base de dados
        redisHashMap.flushAll();


    }
}

    class ListPost{
        private Jedis jedis;
        public static String USERS = "users"; // Key set for users' name

        public ListPost() {
            this.jedis = new Jedis("localhost");
        }
        public void saveUser(String username) {
            jedis.lpush(USERS, username);
        }
        public List<String> getUser() {
            return jedis.lrange(USERS, 0, -1);
        }
        public Set<String> getAllKeys() {
            return jedis.keys("*");
        }
        public void flushAll(){
            jedis.flushAll();
        }
    }

    class HashMapPost{
        private Jedis jedis;
        public static String USERS = "users_hash"; // Key set for users' name

        public HashMapPost() {
            this.jedis = new Jedis("localhost");
        }
        public void saveUser(Map<String,String> mapa) {
            jedis.hmset(USERS, mapa);
        }
        public Map<String,String> getUser() {
            return jedis.hgetAll(USERS);
        }
        public Set<String> getAllKeys() {
            return jedis.keys("*");
        }
        public void flushAll(){
            jedis.flushAll();
        }


    }

