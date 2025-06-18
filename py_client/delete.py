import requests


product_id=input("Enter id of Product: ")
try:
    product_id=int(product_id)
except:
    product_id=None
    print(f'{product_id} is not a valid id')

if product_id:
    endpoint = f"http://127.0.0.1:8000/api/product/{product_id}/delete/"


get_res = requests.delete(endpoint)

print(get_res.status_code,get_res.status_code==204)