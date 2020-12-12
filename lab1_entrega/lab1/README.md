# Lab 1

        Cada pasta contém a resolução e os ficheiros de cada exercício.
        Tudo o que é suposto indexar algum tipo de explicação e/ou comandos usados, está presente neste documento.
    

## 1.2

        $cd src
        $./redis-server

    New terminal window:
        $python3 script.py
        $sudo cat initials4redis.txt | ./../redis-6.0.8/src/redis-cli --pipe
    
    Verificar a inserção:
        $KEYS *
        $GET A

## 1.5

    Criei um sistema de mensagens pub/sub com as funcionalidades:
        Login;
        Seguir alguém;
        Deixar de seguir alguém;
        Mandar mensagem;
        Verificar as mensagens recebidas;
        Apagar a caixa de entrada;

    A cada utilizador é lhe associado um username e um nome, criadas com a classe Person.

    Para guardar os utilizadores criados, usei um hash, em que a key é "users:<username>" e tem uma field "name" com o nome colocado.

    Para as mensagens, utilizei uma lista, com a key "mensagens:<username>" e valor a própria mensagem.

    Utilizei também um Set para as pessoas que são seguidas, com a key "following:<username>" e as pessoas como membros.

    

    
