import requests

endpoint = "http://127.0.0.1:8000/api/product/6/"


get_res = requests.get(endpoint,json={"title":None})


print(get_res.json())
print(get_res.status_code)