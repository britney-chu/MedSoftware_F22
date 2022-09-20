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
    print("1 - analyze HDL")
    print("2 - analyze LDL")
    print("3 - analyze Total Cholesterol")
    print("9 - Quit")
    
    keep_running = True
    while keep_running:
        choice = input("Enter your choice: ")
        if choice == "9":
            return
        elif choice == "1":
            HDL_driver()
        elif choice == "2":
            LDL_driver()
        elif choice == "3":
            cholesterol_driver()

def user_input():
    user_in = input("Enter value: ")
    return int(user_in)
def check_HDL(HDLNum):
    if HDLNum >= 60:
        return "Normal"
    elif HDLNum >= 40:
        return "Borderline Low"
    else:
        return "Low"
#driver function: calls other funtions and moves variables in between them
def HDL_driver():
    hdl_value = user_input()
    answer = check_HDL(hdl_value)
    output_HDL_result(hdl_value, answer)
def LDL_driver():
    ldl_value = user_input()
    answer = check_LDL(ldl_value)
    output_LDL_result(ldl_value, answer)
def cholesterol_driver():
    chol_value = user_input()
    answer = check_chol(chol_value)
    output_chol_results(chol_value, answer)

def check_chol(cholNum):
    if cholNum < 200:
        return "Normal"
    elif 200 <= cholNum <= 239:
        return "Borderline High"
    elif cholNum >= 240:
        return "High"

def check_LDL(LDLNum):
    if LDLNum < 130:
        return "LDL is normal"
    elif 130 <= LDLNum <160:
        return "LDL is borderline high"
    elif 160 <= LDLNum <190:
        return "LDL is high"
    else:
        return "LDL is very high"

def output_HDL_result(HDL_value, charac):
    print("The results for an HDL value of {} is {}".format(HDL_value, charac))
def output_LDL_result(LDL_value, charac):
    print("The results for an LDL value of {} is {}".format(LDL_value, charac))
def output_chol_results(chol_value, charac):
    print("The results for an cholesterol value of {} is {}".format(chol_value, charac))
if __name__ == "__main__":
    interface()
