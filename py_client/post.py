import requests

endpoint = "http://127.0.0.1:8000/api/product/"

data = {
    "title":"Generic Mixins"
}

get_res = requests.post(endpoint,json=data)


print(get_res.json())
print(get_res.status_code)