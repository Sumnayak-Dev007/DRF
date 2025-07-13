import requests

endpoint = "http://127.0.0.1:8000/api/product/1/update/"

data = {
    "title":"Hello World my old friend",
    "price": 122.75
}

get_res = requests.put(endpoint,json=data)


print(get_res.json())
print(get_res.status_code)