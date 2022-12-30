"""
Created on Thu Oct 27 15:30:39 2022

@author: dylan cai and britney chu
Snotty Slimesters
"""
import code
from flask import Flask, request, jsonify
from datetime import datetime, time, date, timedelta
import requests
import logging


attending = []
patient = []


app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_on():
    """Confirmation that server is functional

    Use Flask Handler to produce message

    Returns:
        string: confirms functionality of flask server
    """
    return "Heart Rate Sentinel Server - Snotty Slimesters"


def add_attending(username, email, phone):
    """Add attening info to list of attendings

    Create dictionary given attending's information
    and adds this to this list of existing
    attendings. This is then logged.

    Args:
        username (string): username of attending
        email (string): email of attending
        phone (string): phone number of attending
    """
    new_attendee = {"username": username,
                    "email": email,
                    "phone": phone
                    }
    attending.append(new_attendee)
    logging.info("new attendee {} has been added with email: {}"
                 .format(username, email))


def add_patient(patient_id, attending_username, patient_age,
                hr=[], time=[], status=[]):
    """Add patient info to list of attendings

    Create dictionary given patient's information
    and adds this to this list of existing
    patients. This is then logged.

    Args:
        patient_id (int or string): patient id
        attending_username (string): attending username
                assigned to this patient
        patient_age (int or string): age of patient
        heart_rate (list): list of hr (int)
        time_stamp (list): list of date and time (str) corresponding
                            to each hr entry
        status (list): list of "tachycardic" or not "tachicardic"
                       corresponding to each hr entry

    """
    new_patient = {"patient_id": patient_id,
                   "attending_username": attending_username,
                   "patient_age": patient_age,
                   "heart_rate": hr,
                   "time_stamp": time,
                   "status": status
                   }
    patient.append(new_patient)
    logging.info("new patient with id {} has been added"
                 .format(patient_id))


def init_server():
    """Initialize db with dummy data

    Creates some attendings and patients in global
    variable db. Initiates Log
    """
    global patient
    global attending
    patient = []
    attending = []
    logging.basicConfig(filename="heart_rate_sentinel.log", level=logging.INFO,
                        filemode='w')
    add_attending("Bocci.P", "pboch@gmail.com", "919-555-1212")
    add_attending("Cai.D", "dcai@gmail.com", "330-906-3268")
    add_attending("Chu.B", "bchu@chucrew.com", "123-456-7890")
    add_patient(1, "Cai.D", 10, [1, 2], [1, 2], ["not tachycardic",
                                                 "not tachycardic"])
    add_patient(2, "Chu.B", 45, [1], [1], ["not tachycardic"])
    add_patient(3, "Bocci.P", 100, [1, 2, 3], [1, 2, 3],
                ["tachycardic", "not tachycardic", "not tachycardic"])
    add_patient(4, "Malfoy.D", 20, [80, 90, 100], ["2022-11-03 06:18:20",
                "2022-11-04 06:18:20", "2022-11-05 06:18:20"])
    add_attending("Line.F", "fline@gmail.com", "123-456-7891")

    # initialize logging in init server function
    # anything u need to do to get server ready to use


def add_new_attending_worker(in_data):
    """
    validates incoming data from post request and adds new attending user to
    database

    uses if statement and dictionaries and lists to create database of
    attending users

    Args:
        in_data: dictionary received from client file

    Returns:
        string and 200 status code if done correctly
    """
    result = validate_new_attending_info(in_data)
    if result is not True:
        return result, 400
    add_attending(in_data["username"],
                  in_data["email"],
                  in_data["phone"])
    return "Attendee successfully added", 200


def add_new_patient_worker(in_data):
    """Validate data, Pass data, return completion

    Validates input data, returns error if there is
    one. Adds the patient, and returns succcess info.

    Args:
        in_data (dict): {"patient_id": <string or int>,
                         "attending_username": <string>,
                         "patient_age": <string or int>}
    Returns:
        str: message describing error or success
        int: error code (400) or success code (200)
    """
    result = validate_new_patient_info(in_data)
    if result is not True:
        return result, 400
    add_patient(in_data["patient_id"],
                in_data["attending_username"],
                in_data["patient_age"])
    return "Patient successfully added", 200


def validate_new_patient_info(in_data):
    """Validate patient input infor

    Confirms that input is a dictionary, has the
    necessary keys, and that the values of these
    keys have the right types associated with them.

    Args:
        in_data (dict): {"patient_id": <string or int>,
                         "attending_username": <string>,
                         "patient_age": <string or int>}
    Returns:
        str: message describing error
        or
        boolean: True inidcating valid info
    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["patient_id", "attending_username", "patient_age"]
    for ex_key in expected_keys:
        if ex_key not in in_data:
            return "Key {} is missing from POST data".format(ex_key)
    expected_types = [[int, str], [str], [int, str]]
    for ex_key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[ex_key]) not in ex_type:
            return "Key {}'s value has the wrong data type".format(ex_key)
    try:
        int(in_data["patient_id"])
    except ValueError:
        return "The patient_id input is not numeric"
    try:
        int(in_data["patient_age"])
    except ValueError:
        return "The patient_age input is not numeric"
    return True


def validate_new_attending_info(in_data):
    """
    validates incoming data from post request

    uses if statements and zip function to verify the validity of incoming json

    Args:
        in_data: json data from client file

    Returns:
        returns true if data is all valid, raises errors if common error is
        caught
    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["username", "email", "phone"]
    for key in expected_keys:
        if key not in in_data:
            return "Key {} is missing from POST data".format(key)
    expected_types = [str, str, str]
    for key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[key]) is not ex_type:
            return "Key {}'s value has the wrong data type".format(key)
    return True


@app.route("/api/new_attending", methods=["POST"])
def add_new_attending_to_server():
    """
    calls new_attending worker which completes the addition of the new
    attending user

    uses requests.get_json to complete the task

    Returns:
        returns status message and a status code
    """
    in_data = request.get_json()
    message, status_code = add_new_attending_worker(in_data)
    return message, status_code


@app.route("/api/new_patient", methods=["POST"])
def add_new_patient_to_server():
    """Add new patient to server

    Makes a post request to the server. Gets
    client dictionary of patient info and creates
    new patient in list.

    Returns:
        str: message describing error or success
        int: status code of request
    """
    in_data = request.get_json()
    message, status_code = add_new_patient_worker(in_data)
    return message, status_code


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_status(patient_id):
    """
    calls make_status_dict which creates the dictionary with the status of
    given patient
    uses if statements and try except blocks to catch errors and uses jsonify
    to provide the appropriate value to return

    args: patient id

    Returns:
        returns a dictionary with the status of the patients if successful,
        if not successful, returns appropriate error message
    """
    try:
        int(patient_id)
    except ValueError:
        return "The patient_id input is not numeric"
    status_dict = make_status_dict(patient_id)
    if status_dict == "patient not found":
        return "patient with id {} was not found".format(patient_id)
    return jsonify(status_dict)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def avg_heart_rate(patient_id):
    """
    prints the average heart rate for a given patient to the server

    uses try except block to catch errors and uses jsonify to convert the
    returned value to the proper format

    Args: patient_id: id of the patient which is specified in the url

    Returns:
        returns the jsonified string containing the average heart rate
    """
    try:
        int(patient_id)
    except ValueError:
        return "The patient_id input is not numeric"
    avg = get_avg_hr(patient_id)
    if avg == "patient not found":
        return "patient with id {} not found".format(patient_id)
    return jsonify("average heart rate of patient {} is {} bpm"
                   .format(patient_id, avg))


@app.route("/api/patients/<attending_username>", methods=["GET"])
def get_patients_attending(attending_username):
    """
    prints the list of patients that are being attended to by a certain
    attending user

    uses if statement to catch errors and uses jsonify to convert to
    proper format

    Args: attending_username is the username of the attending user that
    you want the list of patients for

    Returns:
        returns the jsonified string containing
        the correct list of patient dicts
    """
    if find_attending(attending_username) is False:
        return "attending username does not exist in database"
    list = find_patients_for_attending_worker(attending_username)
    return jsonify(list)


def get_avg_hr(pid):
    """
    calculates average heart rate based on the patient given

    uses if statement to catch errors, and uses sum and len functions to find
    average

    Args: pid: the patient id which is used to find the list of heart rates
    for that patient to find the average

    Returns:
        returns the average of all of the heart rates in the list
    """
    found = find_patient(pid)
    if found is False:
        return "patient not found"
    avg = sum(found["heart_rate"]) / len(found["heart_rate"])
    return avg


def find_patient(pid):
    """Given patient ID, find patient dict

    Searches through existing patients by ID
    to find patient with matching ID to input.

    Args:
        int: patient_id
    Returns:
        boolean: False if patient not found
        or
        dict: patient data from list of patients
    """
    for p in patient:
        if p["patient_id"] == int(pid):
            return p
    return False


def find_attending(username):
    """
    finds the attending user based on the username

    uses if statement and for loop to find a specific username in the
    list

    Args: username: attending username used to find the attender

    Returns:
        returns the found attending or false if nothing was found
    """
    for a in attending:
        if a["username"] == username:
            return a
    return False


def find_patients_for_attending_worker(username):
    """
    worker function to find patients under a specific attender

    uses a for loop and if statement to create list of patients
    then calls create_dict function that creates the dictionary with
    correct format to return

    Args: username: username of the attending worker

    Returns:
        returns the list of dicts needed
    """
    list = []
    for p in patient:
        if p["attending_username"] == username:
            list.append(p)
    list_new = create_dict_for_attending_patients(list)
    return list_new


def create_dict_for_attending_patients(patients):
    """
    creates the dict with necessary fields for all patients in a list

    uses dictionaries and for loop to create multiple dictionaries

    Args: patients: list of patients under one attending

    Returns:
        returns list of dictionaries, each dict corresponding to a patient in
        the initial list
    """
    list = []
    dict = {}
    print(patients)
    for p in patients:
        dict["patient_id"] = p["patient_id"]
        dict["last_heart_rate"] = p["heart_rate"][-1]
        dict["last_time"] = p["time_stamp"][-1]
        dict["status"] = p["status"][-1]
        list.append(dict)
    return list


def make_status_dict(pid):
    """
    makes a dictionary with the proper fields to show the status of the
    most recent heart rate

    uses if statements and negative indexing to create necessary dict

    Args: pid: id of the patient

    Returns:
        returns the dictionary with heart rate, status, and timestamp for a
        specific patient
    """
    found = find_patient(pid)
    if found is False:
        return "patient with id {} was not found".format(pid)
    status_dict = {}
    status_dict["heart_rate"] = found["heart_rate"][-1]
    status_dict["status"] = found["status"][-1]
    status_dict["time_stamp"] = found["time_stamp"][-1]
    return status_dict


def diagnosis(hr, age):
    """
    gives the diagnosis of tachycardic or not tachycardic based on age and HR

    uses if statements to diagnose

    Args: heart rate: most recent heart rate of the patient
    age: age of the patient

    Returns:
        returns the diagnosis in a string
    """
    if 1 <= age <= 2 and hr > 151:
        return "tachycardic"
    elif 3 <= age <= 4 and hr > 137:
        return "tachycardic"
    elif 5 <= age <= 7 and hr > 133:
        return "tachycardic"
    elif 8 <= age <= 11 and hr > 130:
        return "tachycardic"
    elif 12 <= age <= 15 and hr > 119:
        return "tachycardic"
    elif age > 15 and hr > 100:
        return "tachycardic"
    else:
        return "not tachycardic"


@app.route("/api/heart_rate", methods=["POST"])
def add_heart_rate_to_patient():
    """Add a patient's heart rate in db

    Reads post request input data.
    Calls heart_rate_worker. Then returns success
    or Failure

    Returns:
        str: message describing error or success
        int: status code of request
    """
    in_data = request.get_json()
    message, status_code = heart_rate_worker(in_data)
    return message, status_code


def heart_rate(patient, heart_rate):
    """Add hr to patient log

    Adds heart rate entry to the dictionary of
    the patient info. Then assesses this entry
    for diagnosis and adds this to the status
    entry. The time of this entry is also logged
    in the dictionary. If the diagnosis is tachycardic
    an email is sent to the attending and a warning is
    added to the log.

    Returns:
        dict: updated patient info
    """
    patient["heart_rate"].append(int(heart_rate))
    patient["status"].append(diagnosis(patient["heart_rate"][-1],
                                       patient["patient_age"]))
    attend = find_attending(patient["attending_username"])
    if diagnosis(patient["heart_rate"][-1],
                 patient["patient_age"]) == "tachycardic":
        logging.warning("patient with patient id:{}, last heart rate:{}, "
                        "and attending physician e-mail:{} was tachycardic"
                        .format(patient['patient_id'],
                                patient["heart_rate"][-1],
                                attend["email"]))
    patient["time_stamp"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return patient


def heart_rate_worker(in_data):
    """Add hr to patient and check diagnosis

    Validates the input data. If it is not a
    valid input then it returns the error and
    the error code. It then checks if this patient
    exists in the db. If if it does

    Returns:
        dict: updated patient info
    """
    result = validate_heart_rate_info(in_data)
    result2 = validate_patient_id(in_data["patient_id"])
    if result is not True:
        return result, 400
    if result is not True:
        return result2, 400
    patient = find_patient(in_data["patient_id"])
    heart_rate(patient,
               in_data["heart_rate"])
    if diagnosis(patient["heart_rate"][-1],
                 patient["patient_age"]) == "tachycardic":
        send_email(patient)
    return "Heart Rate successfully added", 200


def validate_heart_rate_info(in_data):
    """Validate heart rate input infor

    Confirms that input is a dictionary, has the
    necessary keys, and that the values of these
    keys have the right types associated with them.

    Args:
        in_data (dict): {"patient_id": <string or int>,
                         "heart_rate": <string or int>}
    Returns:
        str: message describing error
        or
        boolean: True inidcating valid info
    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["patient_id", "heart_rate"]
    for ex_key in expected_keys:
        if ex_key not in in_data:
            return "Key {} is missing from POST data".format(ex_key)
    expected_types = [[int, str], [int, str]]
    for ex_key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[ex_key]) not in ex_type:
            return "Key {}'s value has the wrong data type".format(ex_key)
    try:
        int(in_data["patient_id"])
    except ValueError:
        return "The patient_id input is not numeric"
    try:
        int(in_data["heart_rate"])
    except ValueError:
        return "The patient_age input is not numeric"
    return True


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_patient_record(patient_id):
    """Get request to get patient hr record

    Calls worker and returns message and status code.

    Returns:
        str: message describing error or hr list
        int: status code
    """
    message, status_code = get_heart_rates_worker(patient_id)
    return message, status_code


def get_heart_rates_worker(patient_id):
    """Validate data, Find patient, return hr

    Runs validation test. If valid, finds patient
    using patient id, retreives hr list and successful
    status code.

    Args:
        patient_id (int): patient whose data is being
                          retreived
    Returns:
        list: message describing error or hr list
        int: status code
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient = find_patient(patient_id)
    hr_list = patient["heart_rate"]
    return hr_list, 200


def validate_patient_id(patient_id):
    """Check if patient with ID exists

    Validate that patient exists in the db.
    If not return error describing ID not found.

    Args:
        patient_id (int): queried patient_id in db
    Returns:
        str: message describing error
        or
        boolean: True inidcating patient_found
    """
    try:
        int(patient_id)
    except ValueError:
        return "The patient_age input is not numeric"
    if not (find_patient(int(patient_id))):
        return "The patient with id {} was not found".format(patient_id)
    else:
        return True


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def get_interval_average():
    """handle request to get interval avg

    Receives input post information, passes this data
    to the worker and returns message and status code.

    Returns:
        str: message with interval average or error
        int: status of request
    """
    in_data = request.get_json()
    message, status_code = get_interval_average_worker(in_data)
    return jsonify(message), status_code


def get_interval_average_worker(in_data):
    """Validate input, find average, return answer

    Confirms that input is valid, then finds patient in
    db. gets the interval average, and returns the average
    of this list after input time.

    Args:
        in_data (dict): {"patient_id": <string or int>,
                         "heart_rate_average_since": <string>}
    Returns:
        str: message describing error or interval avg
        or
        int: Status code
    """
    result = validate_time_input(in_data)
    if result is not True:
        return result, 400
    result2 = validate_patient_id(in_data["patient_id"])
    if result is not True:
        return result2, 400
    patient = find_patient(in_data["patient_id"])
    hr_interval = get_hr_interval(patient,
                                  in_data["heart_rate_average_since"])
    hr_interval_avg = average_list(hr_interval)
    return hr_interval_avg, 200


def get_hr_interval(patient, time_in):
    """Get interval range after time

    Get list of hr after time_in from patient
    dictionary.

    Args:
        patient (dict): patient data with hr and times
    Returns:
        list: list of hr after time inputted
    """
    time_in_obj = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
    for i in range(len(patient["time_stamp"])):
        time_entry = patient["time_stamp"][i]
        time_entry_obj = datetime.strptime(time_entry, "%Y-%m-%d %H:%M:%S")
        if ((time_entry_obj - time_in_obj).total_seconds()) >= 0:
            start_index = i
            break
    hr_list = patient["heart_rate"][start_index:]
    return hr_list


def average_list(in_list):
    """Takes average of values in list.

    Sums items in a list and divides this by the number
    of items in the list

    Args:
        in_list (list): list to be averaged
    Returns:
        float: avg of list
    """
    return sum(in_list)/len(in_list)


def validate_time_input(in_data):
    """Validate post request hr interval info

    Confirms that input is a dictionary, has the
    necessary keys, and that the values of these
    keys have the right types associated with them.

    Args:
        in_data (dict): {"patient_id": <string or int>,
                         "heart_rate_average_since":
                         <string or int>}
    Returns:
        str: message describing error
        or
        boolean: True inidcating valid info
    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["patient_id", "heart_rate_average_since"]
    for ex_key in expected_keys:
        if ex_key not in in_data:
            return "Key {} is missing from POST data".format(ex_key)
    expected_types = [[int, str], [str]]
    for ex_key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[ex_key]) not in ex_type:
            return "Key {}'s value has the wrong data type".format(ex_key)
    try:
        int(in_data["patient_id"])
    except ValueError:
        return "The patient_id input is not numeric"
    return True


def send_email(patient):
    """Send email to attending when tachycardic

    Validate patient id exists. Sends email to
    server to alert attending that patient is tachycardic
    then returns the message sent with the status code.

    Args:
        patient (dict): patient data with logged hr
    Returns:
        str: message describing error or message of email
        int: status code
    """
    result1 = validate_patient_id(patient["patient_id"])
    result2 = validate_new_patient_info(patient)
    if result1 is not True:
        return result1, 400
    if result2 is not True:
        return result2, 400
    email_message = create_email(patient)
    to_email = find_attending(patient["attending_username"])["email"]
    out_data = create_out_data(to_email, email_message)
    r = requests.post("http://vcm-7631.vm.duke.edu:5007/hrss/send_email",
                      json=out_data)
    return ("Email from hospital_alerts@hospital.com to {}".format(to_email),
            r.status_code)


def create_email(patient):
    """Write email to be sent to attending

    Uses patient id, age, and most recent heart rate
    to write message to be sent to the attending

    Args:
        in_data (dict): patient data who is tachycardic
    Returns:
        str: message for attending's email
    """
    email_message = "The patient number {} is {} years old and" \
                    " recorded a heart rate of {} which is considered"\
                    " tachycardic".format(patient["patient_id"],
                                          patient["patient_age"],
                                          patient["heart_rate"][-1])
    return email_message


def create_out_data(to_email, email_message):
    """Create dictionary for request to email server

    Uses email address and message inputs to create
    a dictionary to be sent to email server.

    Args:
        to_email (str): str of email address
        email_message (str): str of message to attending
    Returns:
        dictionary: to be sent to email server request.
    """
    out_data = {"from_email": "hospital_alerts@hospital.com",
                "to_email": to_email,
                "subject": "Tachycardic HR ALERT",
                "content": email_message}
    return out_data


if __name__ == '__main__':
    init_server()
    app.run(host="0.0.0.0")
