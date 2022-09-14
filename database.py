def create_patient_entry(patient_name, patient_id, patient_age):
    new_patient = [patient_name, patient_id, patient_age, []]
    return new_patient

def main():
    db = []
    db.append(create_patient_entry("Ann Ables", 1,30))
    db.append(create_patient_entry("Bob Boyles", 2, 34))
    db.append(create_patient_entry("Chris Chou", 3, 25))
    printdb(addTest(main(), 1, "Herpes", "Positive"))
    room_list = ["Room 1", "Room 2", "Room 3"]
    for i, patient in enumerate(db):
        print("Name = {}, Room = {}".format(patient[0], room_list[i]))
    return db
def printdb(db):
    for x in db:
        print("Name: " + str(x[0]))
        print("ID: " + str(x[1]))
        print("Age: " + str(x[2]))
        print("Tests: " + str(x[3]))
def findPatient(db, ID):
    for patient in db:
        if patient[1] == ID:
            return patient
    return False
def addTest(db, ID, testName, testVal):
    findPatient(db,ID)[3].append((testName, testVal))
    return db

if __name__ == "__main__":
    main()