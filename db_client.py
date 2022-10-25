import requests

out_data = {"name": "Charlie",
            "id": 3,
            "blood_type": "AB-"}


r = requests.post("http://127.0.0.1:5000/new_patient", json = out_data)
print(r.status_code)
print(r.text)