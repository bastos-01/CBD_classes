import redis.clients.jedis.Jedis;

import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class Main {

    private static Jedis jedis = new Jedis("localhost");

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("Bem Vindo!");
        System.out.println("Introduza o seu username:");
        String username = sc.nextLine();
        System.out.println("Introduza o primeiro e último nome:");
        String name = sc.nextLine();

        Person p = new Person(username, name);

        jedis.hset("users:" + p.getUsername(),  "name", p.getName());

        int op = 0;

        while (op != 6){
            Scanner sc2 = new Scanner(System.in);
            System.out.println("Opções:\n    1) Mandar mensagem\n    2) Ver caixa de entrada\n    3) Seguir alguém\n    4) Deixar de seguir alguém\n    5) Apagar caixa de entrada\n    6) Sair");
            String option = sc2.nextLine();
            op = Integer.parseInt(option);

            switch (op){
                case 1:
                    System.out.println("Mensagem a mandar:");
                    String mensagem = sc2.nextLine();
                    jedis.lpush("mensagens:" + p.getUsername(), mensagem);
                    break;

                case 2:
                    Set<String> following = jedis.smembers("following:" + p.getUsername());
                    if (following.size() == 0)
                        System.out.println("Não segue ninguém!");
                    else{
                        for (String user: following){
                            String u = user.split(":")[1];
                            List<String> msgs = jedis.lrange("mensagens:" + u, 0, -1);
                            if(msgs.size() != 0){
                                System.out.println("Mensagem de " + jedis.hget(user, "name") + ":");
                                for(String m: msgs)
                                    System.out.println(m);
                            }
                        }
                    }
                    break;

                case 3:
                    System.out.println("Lista de users:");
                    Set<String> users = jedis.keys("users:*");
                    users.remove("users:" + p.getUsername());
                    for (String u: users)
                        System.out.println(u.split(":")[1]);

                    System.out.println("introduza o utilizador que pretende seguir:");
                    String user_follow = "users:" + sc2.nextLine();

                    if(!users.contains(user_follow)){
                        System.out.println("O utilizador não existe!");
                    }
                    else{
                        jedis.sadd("following:" + p.getUsername(), user_follow);
                    }
                    break;

                case 4:
                    Set<String> following_users = jedis.smembers("following:" + p.getUsername());

                    if(following_users.size() == 0)
                        System.out.println("Não segue ninguém!");
                    else{
                        System.out.println("following users:");
                        for(String followU: following_users)
                            System.out.println(followU.split(":")[1]);

                        System.out.println("Escolha o utilizador que pretende deixar de seguir:");
                        String user_unfollow = "users:" + sc.nextLine();
                        if(!following_users.contains(user_unfollow))
                            System.out.println("Já não segue este utilizador!");
                        else
                            jedis.srem("following:" + p.getUsername(), user_unfollow);
                    }
                    break;

                case 5:
                    Set<String> following_u = jedis.smembers("following:" + p.getUsername());
                    if (following_u.size() == 0)
                        System.out.println("Não segue ninguém!");
                    else{
                        for (String user: following_u){
                            String u = user.split(":")[1];
                            jedis.del("mensagens:" + u);
                        }
                    }
                    break;

                case 6:
                    System.out.println("Bye!");
                    break;



            }
        }

        sc.close();


    }




}
