import requests


headers = {
    'Authorization':'Bearer d5adb68b73812119b2524c00b16486f16759fcd9'
}
endpoint = "http://127.0.0.1:8000/api/product/"

data = {
    "title":"Token Authentication"
}

get_res = requests.post(endpoint,json=data,headers = headers)

print(get_res.json())
print(get_res.status_code)