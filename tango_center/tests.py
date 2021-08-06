import requests

headers = {
    "X-CSRFToken": "V38ghhesrWjdltnt1F0uNVTCpI8RQJeXl9fDNu3fhwvnQzfWQVddVna791xsEOQF",
    "Cookie" : 'username-localhost-8888="2|1:0|10:1627739555|23:username-localhost-8888|44:MzJlMzNkYjhmMzUzNDdlZDljN2ZmZDg5ZmMzMDc1N2Q=|716fc9f5110e3574c61f4e373527c416b82b7723ee5b0e3e26dd282f9a8b3c58"; _xsrf=2|42392a09|298e77fab079f1b1711d9a48e8c113db|1627739555; csrftoken=V38ghhesrWjdltnt1F0uNVTCpI8RQJeXl9fDNu3fhwvnQzfWQVddVna791xsEOQF; sessionid=opv0sbt5oxq3n388f0d9wxjjqq39grv5'
}

# all info test

base_url = "http://localhost:8888/all/"
resp = requests.get(base_url)
print(resp.status_code == 200)

# category query test

# test 1

base_url = "http://localhost:8888/all/"
data = {
    'val': 'python',
    'sort': 'comment',
    'start': 0,
    'end': 5,
}
resp = requests.post(url=base_url, data=data, headers=headers)
# print(resp.content)
print(resp.status_code == 200)

# test 2

base_url = "http://localhost:8888/all/"
data = {
    'val': 'web',
    'sort': 'comment',
    'start': 0,
    'end': 5,
}
resp = requests.post(url=base_url, data=data, headers=headers)
# print(resp.content)
print(resp.status_code == 200)