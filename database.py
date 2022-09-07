print("this is the database.py module.")
print("Python thinks this is called {}".format(__name__))
from cw0905_2 import check_HDL
answer = check_HDL(55)
print("The HDL of 55 is {}".format(answer))