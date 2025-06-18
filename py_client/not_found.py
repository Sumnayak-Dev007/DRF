import requests

endpoint = "http://127.0.0.1:8000/api/product/60000000/"


get_res = requests.get(endpoint)


print(get_res.json())
print(get_res.status_code)