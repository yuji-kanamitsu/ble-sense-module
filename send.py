import urllib.request
import json

url = ""
method = "POST"
# headers = {}

'''
get data from a database
'''
obj = []


jsonData = json.dumps(obj) # convert python object to json

# POST
request = urllib.request.Request(
    url=url,
    data=jsonData.encode(),
    method=method
)
with urllib.request.urlopen(request) as response:
    response_body = response.read()


'''
エラー対応処理
'''
try:
    with urllib.request.urlopen(request) as response:
        body = response.read()
except urllib.error.HTTPError as err:
    print(err.code)
    pass
except urllib.error.URLError as err:
    print(err.reason)
    pass