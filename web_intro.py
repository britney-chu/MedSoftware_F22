import requests


# r = requests.get("https://api.github.com/repos/dward2/BME547/branches")
# print(r)
# print(type(r))
# print(r.text)
# answer = r.json()
# print(type(answer))
# if r.status_code == 200:
#     answer = r.json()
#     print(type(answer))
#     for branch in answer:
#         print(branch["name"])
# else:
#     print("Bad requests: {}".format(r.text))

output_info = {"name": "Britney Chu",
               "net_id": "bnc23",
               "e-mail": "britney.chu@duke.edu"}

output_messaging = {"user": "scoutmeister",
                    "message": "FIRE IN WILKINSON"}
output_dylan = {"user": "dc306",
                    "message": "you have a booger hanging out of your nose"}

output_daw74 = {"user": "daw74",
                    "message": "Good Morning dr.ward! "}
r = requests.post("http://vcm-21170.vm.duke.edu:5001/add_message",
                        json = output_daw74)
print(r)
print(r.text)


# r = requests.get("http://vcm-21170.vm.duke.edu:5000/list")
# print(r.text)

#r = requests.get("http://vcm-21170.vm.duke.edu:5001/get_messages/britney")
#print(r.text)
