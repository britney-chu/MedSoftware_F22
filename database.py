def create_patient_entry(patient_name, patient_id, patient_age):
    new_patient = {"First Name" : patient_name.split()[0], "Last Name" : patient_name.split()[1], 
                    "Id": patient_id, "Age": patient_age, "Tests": [] }
    return new_patient

def main():
    db = []
    db.append(create_patient_entry("Ann Ables", 1,30))
    db.append(create_patient_entry("Bob Boyles", 2, 34))
    db.append(create_patient_entry("Chris Chou", 3, 25))

    printdb(db)
    addTest(db,3,"HDL", 100)
    printdb(db)
    print("Patient {} is a {}".format(get_full_name(db[2]), adult_or_minor(db[2])))
    '''
    room_list = ["Room 1", "Room 2", "Room 3"]
    for i, patient in enumerate(db):
        print("Name = {}, Room = {}".format(patient[0], room_list[i]))
    return db
    '''
def printdb(db):
    for x in db:
        print(x)
        print("Name: {}, id: {}, age: {}".format(get_full_name(x),x["Id"], x["Age"]))
def get_full_name(patient):
    full_name = "{} {}".format(patient["First Name"], patient["Last Name"])
    return full_name

def findPatient(db, ID):
    for patient in db:
        if patient["Id"] == ID:
            return patient
    return False
def addTest(db, ID, testName, testVal):
    findPatient(db,ID)["Tests"].append((testName, testVal))
    return db
def adult_or_minor(patient):
    if patient["Age"]>=18:
        return "adult"
    else:
        return "minor"

if __name__ == "__main__":
    main()
    