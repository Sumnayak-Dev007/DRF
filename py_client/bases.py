import requests

endpoint = "https://httpbin.org/status/200"
endpoint = "https://httpbin.org/anything"


get_res = requests.get(endpoint)
print(get_res.text)


{
  "args": {},
  "data": "",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.32.3",
    "X-Amzn-Trace-Id": "Root=1-683d96ca-1a40f28f70fb194f6c370d73"
  },
  "json": null,
  "method": "GET",
  "origin": "103.211.52.137",
  "url": "https://httpbin.org/anything"
}