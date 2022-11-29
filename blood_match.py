import requests

r = requests.get("http://vcm-7631.vm.duke.edu:5002/get_patients/bnc23")
print(r.status_code)
print(r.text)

r = requests.get("http://vcm-7631.vm.duke.edu:5002/get_blood_type/F2")
print(r.status_code)
print(r.text)

r = requests.get("http://vcm-7631.vm.duke.edu:5002/get_blood_type/M4")
print(r.status_code)
print(r.text)

out_data = {"Name": "bnc23", "Match": "Yes"}
r = requests.post("http://vcm-7631.vm.duke.edu:5002/match_check", json=out_data)
print(r.status_code)
print(r.text)