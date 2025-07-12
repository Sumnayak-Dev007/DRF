import requests


# endpoint = "https://httpbin.org/anything"
endpoint = " http://127.0.0.1:8000/api/demo/"


# get_res = requests.get(endpoint,params = {"abc":1234},json={"queryy":"Echo GET request"})
get_res = requests.get(endpoint,json={"queryy":"Echo GET request"})
# get_res = requests.post(endpoint,json={"title":None})
print(get_res.headers)
print(get_res.status_code)


print(get_res.json())


