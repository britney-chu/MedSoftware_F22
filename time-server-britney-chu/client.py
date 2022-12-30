import requests

out_data = {"date": "07/06/2001",
            "units": "years"}


r = requests.get("http://127.0.0.1:5000/until_next_meal/breakfast")
print(r.status_code)
print(r.text)
