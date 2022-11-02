import requests

# r = requests.get("http://127.0.0.1:5000/info")
# print(r.status_code)
# print(r.text)

# out_data ={"name": "Britney Chu",
#            "hdl_value": 150}
# r = requests.post("http://127.0.0.1:5000/hdl_check", json = out_data)
# print(r.status_code)
# print(r.text)

# out_data ={"a": 2,
#            "b": 3}
# r = requests.post("http://127.0.0.1:5000/add_numbers", json = out_data)
# print(r.status_code)
# print(r.text)

r = requests.get("http://127.0.0.1:5000/add/2/3")
print(r.status_code)
print(r.text)