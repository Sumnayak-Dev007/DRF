import requests
from getpass import getpass


auth_endpoint = "http://127.0.0.1:8000/api/auth/"
username = input("What is your username?\n")
password = getpass("What is your password?\n")

get_auth = requests.post(auth_endpoint,json={'username':username,'password':password})
print(get_auth.json())
print(get_auth.status_code)

if get_auth.status_code == 200:
    token = get_auth.json()['token']
    headers = {
        "Authorization":f"Bearer {token}"
    }
    endpoint = "http://127.0.0.1:8000/api/product/"
    get_res = requests.get(endpoint,headers = headers)
    print(get_res.json())
    print(get_res.status_code)