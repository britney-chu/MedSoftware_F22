# def increment_by_five(x):
#     a = x + 5
#     if a>= 18:
#         adult = True
#     else:
#         adult = False
#     return a, adult

# answer, is_adult = increment_by_five(11)
# print("The answer is {}".format(answer))
# print("True or false, the person is an adult: {}".format(is_adult))

def interface():
    print("Blood Calculator")
    print("Options: ")
    print("9 - Quit")
    
    keep_running = True
    while keep_running:
        choice = input("Enter your choice: ")
        if choice=='9':
            return
def user_input():
    user_in = input("Enter HDL: ")
    return int(user_in)
def check_HDL(HDLNum):
    if HDLNum >= 60:
        return "Normal"
    elif HDLNum >= 40:
        return "Borderline Low"
    else:
        return "Low"
# take input from keyboard as a number then return that number 
interface()