import requests


def upload_patient_info(patient_name, patient_id, patient_blood_type):
    out_data = {"name": patient_name, "id": patient_id,
                "blood_type": patient_blood_type}
    r = requests.post("http://127.0.0.1:5000/new_patient", json=out_data)
    return r.text, r.status_code

# r = requests.post("http://127.0.0.1:5000/test", json = out_data)

# test_data = {"id": 2, "test_name": "HDL", "test_result": 100}
# r = requests.post("http://127.0.0.1:5000/add_test", json=test_data)
# print(r.status_code)
# print(r.text)

#test_data = {"id": 2, "test_name": "HDL", "test_result": 100}
# r = requests.get("http://127.0.0.1:5000/")
# print(r.status_code)
# print(r.text)