import requests



BASE = "http://127.0.0.1:5000/"

# res = requests.post(BASE+"User/",{"name":"Ayman","email":"ayman2@gmail.com","password":"123456",
#                                 "phone_number":1097348399,"company_name":"Itqan"})
# if res.json()['error'] is None:
#     print("User Added Successfully")
# else:
#     print(res.json()['error'])

res = requests.get(BASE+"User",{"email":"ayman@gmail.com" , "password":"13456"})
print(res.status_code)
if res.json()['error'] is not None:
    print(res.json()['error'])
else:
    print("Login successfully")
