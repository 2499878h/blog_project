import requests

headers = {
    "X-CSRFToken": "3KHiFnDLJHacqb7AXwMZlCH2Pul4T79zV1SnpMnBKz3hFr6jcCpcfOmLWhsFomVl",
    "Cookie" : 'username-localhost-8888="2|1:0|10:1627739555|23:username-localhost-8888|44:MzJlMzNkYjhmMzUzNDdlZDljN2ZmZDg5ZmMzMDc1N2Q=|716fc9f5110e3574c61f4e373527c416b82b7723ee5b0e3e26dd282f9a8b3c58"; _xsrf=2|42392a09|298e77fab079f1b1711d9a48e8c113db|1627739555; csrftoken=3KHiFnDLJHacqb7AXwMZlCH2Pul4T79zV1SnpMnBKz3hFr6jcCpcfOmLWhsFomVl; sessionid=r5nsc8lxaazo6x9nhuh239agbdyz0au6'
}

# login test

base_url = "http://localhost:8888/usercontrol/login"
data = {
    'username': '123',
    'password': '123'
}

resp = requests.post(base_url)
print(resp.content)
print(resp.status_code == 200)

