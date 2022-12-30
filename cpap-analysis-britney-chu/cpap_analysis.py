import json


def read_txt(filename):
    """Take in file.text and read each line into a list of strings

    The function opens the file which creates a file object
    then reads each line as a string into a list of strings.
    The file is then closed and the list of strings is returened.

    Args:
        filename (string): name of file with data (expecting .txt)

    Returns:
        list: List of each line in file as a string
    """
    inFile = open(filename, 'r')
    data = inFile.readlines()
    inFile.close()
    return data


def parseData(data):
    """Translate data read from file to list of patient dictionaries

    This function takes in the list of strings describing patient data
    and determines how many patients there will be. Using this is creates
    a list of dictionaries in which data from each patient is stored with
    a descriptive key of the type of information stored. These dictionaries
    are then put into a list which the function returns

    Args:
        data (list): list of strings which are lines from the file input

    Returns:
        list: List of dictionaries, each representing a patient's data
    """
    num_patients = int(len(data) / 5)
    list_patients = []
    for i in range(num_patients):
        data_dict = {}
        data_dict['First Name'] = data[0 + 5 * i].split()[0]
        data_dict['Last Name'] = data[0 + 5 * i].split()[1]
        data_dict['Hours'] = float(data[1 + 5 * i])
        int_seal = to_float_list(data[2 + 5 * i].split(",")[1:])
        data_dict['Seal'] = int_seal
        int_events = to_int_list(data[3 + 5 * i].split(",")[1:])
        data_dict['Events'] = int_events
        int_o2 = to_int_list(data[4 + 5 * i].split(",")[1:])
        data_dict['O2'] = int_o2
        list_patients.append(data_dict)
    return list_patients


def to_int_list(inlist):
    """Change a list of string number to a list of type int

    This function takes in a list of strings which are numbers,
    removes white space from the beginning and end,
    and changes them to python type int.

    Args:
        inList (list): List of numbers as strings with whitespace

    Returns:
        list: List of integers
    """
    return [int(n.strip()) for n in inlist]


def to_float_list(inlist):
    """Change a list of string number to a list of type float

    This function takes in a list of strings which are numbers,
    removes white space from the beginning and end,
    and changes them to python type float.

    Args:
        inList (list): List of numbers as strings with whitespace

    Returns:
        list: List of floats
    """
    return [float(n.strip()) for n in inlist]


def find_avg(field, data_dict):
    """Locates record within dictionary and averages values

    Uses field as key to dictionary. Gets the value at this key
    (list) and takes the average of the values in the list.

    Args:
        field (string): Key of list to be averaged
        data_dict (dictionary): patient dictionary record

    Returns:
        float: Average of values in list at given key
    """
    average = sum(data_dict[field]) / len(data_dict[field])
    round_avg = round(average, 2)
    return round_avg


def add_to_record(field, data_dict, value):
    """Add new recrod to patient dicitonary

    Add key with inputted name to dictionary representing
    one patient with inputted value pair

    Args:
        field (string): Key new dictionary entry
        data_dict (dictionary): patient dictionary record
                                to be updated
        value (any type): value to be added at key 'field'

    Returns:
        dictionary: patient dict with new key value pair
    """
    data_dict[field] = value
    return data_dict


def check_o2(data_dict):
    """Check O2 level of patient for hypoxia

    Look in dictionary at all O2 levels for values
    below 93. If found return string hypoxia. If not
    found return normal. The patient did not experience
    low oxygenation in this case.

    Args:
        data_dict (dictionary): patient dictionary record
                                to be assessed for hypoxia

    Returns:
        string: assessment of whether or not patient
                has experienced hypoxia
    """
    for x in (data_dict['O2']):
        if x < 93:
            return "hypoxia"
    return "normal"


def do_diagnosis(data_dict):
    """Given events/hr and hypoxia status determine diagnosis

    Average values in list at key "Events". Run check_o2
    on O2 values found in dictionary to determine if the patient has
    experienced hypoxia.
    If patient has not experienced hypoxia
    and has an average of 5 or less apnea events per hr
    then the diagnosis is "normal sleep".
    If the patient has not experienced hypoxia and has an average
    of more than 5 apnea events per hr then the diagnosis is "apnea"
    If the patient has experienced hypoxia and has an average of
    5 or less apnea events per hr then the diagnosis is "hypoxia"
    If the patient has experienced hypoxia and has an average of
    more than 5 apnea events per hr then the diagnosis is "hypoxia apnea"


    Args:
        data_dict (dictionary): patient record to be diagnosed

    Returns:
        string: diagnosis of patient given cpap record
    """
    avg_events = find_avg("Events", data_dict)
    o2_level = check_o2(data_dict)
    if (o2_level == "hypoxia" and avg_events <= 5):
        return "hypoxia"
    if (o2_level == "normal" and avg_events <= 5):
        return "normal sleep"
    if (o2_level == "normal" and avg_events > 5):
        return "apnea"
    if (o2_level == "hypoxia" and avg_events > 5):
        return "hypoxia apnea"


def save_json(patient):
    """save patient dictionary as json file

    Save dictionary as json file with name 'FirstName-LastName.json'.
    Then close this file.


    Args:
        data_dict (dictionary): patient dictionary record
                                to be saved as json file
    """
    file_name = ("-".join([patient["First Name"],
                 patient["Last Name"]]) + ".json")
    out_file = open(file_name, 'w')
    json.dump(patient, out_file)
    out_file.close()


if __name__ == "__main__":
    data = read_txt("sample_data.txt")
    list_patients = parseData(data)
    for patient in list_patients:
        seal_avg = find_avg("Seal", patient)
        add_to_record("Seal Average", patient, seal_avg)
        diagnosis = do_diagnosis(patient)
        add_to_record("Diagnosis", patient, diagnosis)
        save_json(patient)
