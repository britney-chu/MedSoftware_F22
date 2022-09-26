class Patient:
    def __init__(self, first_name, last_name, patient_id, age):
        self.first_name = ""
        self.last_name = ""
        self.patient_id = ""
        self.age = ""
        self.tests = []
    
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)




def create_patient_entry(patient_name, patient_id, patient_age):
    new_patient = Patient(patient_name.split()[0], patient_name.split()[1], patient_id, patient_age)
    new_patient.tests = []
    return new_patient

def main():
    db = {}
    db[1] = create_patient_entry("Ann Ables", 1,30)
    db[2] = create_patient_entry("Bob Boyles", 2, 34)
    db[3] = create_patient_entry("Chris Chou", 3, 25)

    printdb(db)
    addTest(db,3,"HDL", 100)
    printdb(db)
    print("Patient {} is a {}".format(db[2].full_name(), db[2].adult_or_minor()))
    '''
    room_list = ["Room 1", "Room 2", "Room 3"]
    for i, patient in enumerate(db):
        print("Name = {}, Room = {}".format(patient[0], room_list[i]))
    return db
    '''
def printdb(db):
    for x in db:
        print("Name: {}, id: {}, age: {}, tests: {}".format(get_full_name(db[x]),db[x]["Id"], db[x]["Age"], db[x]["Tests"]))
def get_full_name(patient):
    full_name = "{} {}".format(patient["First Name"], patient["Last Name"])
    return full_name

def findPatient(db, ID):
    patient = db[ID]
    return patient

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
    