# db_server.py

from database_definition import User
from datetime import datetime
from flask import Flask, request, jsonify
from pymodm import connect
from pymodm import errors as pymodm_errors
import ssl
from database_definition import User
import json
app = Flask(__name__)

"""
    Database format:
    [{
    "id": <integer>,
    "name": <string>,
    "medical_image_names": [<string1>, <string2>]
    "medical_image_data": [<string1>, <string2>],
    "ECG_data": [<string1>, <string2>, ...],
    "heart_rates": [<int1>, <int2>, ...],
    "record_time": [<string1>, <string2>]
    }]
"""


def init_server():
    """
    initializes server with connect strings which connects server to database

    uses pymodm to connect to mongodb

    Args:
        none

    Returns:
        string and 200 status code if done correctly
    """
    connect("mongodb+srv://dc306:Guiyang021463@bme547.ujkjzrl.mongodb.net"
            "/final_proj?retryWrites=true&w=majority")


def find_patient(patient_id):
    """
    finds the patient from the mongodb based on the id number

    uses pymodm import and specific mongo syntax to find the patients

    Args:
        patient_id: id of the patient you want to find

    Returns:
        the user class with the entered patient id, or returns false if error
        is caught
    """
    from pymodm import errors as pymodm_errors
    try:
        found = User.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return False
    return found


@app.route("/", methods=["GET"])
def server_on():
    """
    confirms that the server is on and working

    uses the default server route and get method

    Args:
        none

    Returns:
        confirmation string that server is on
    """
    return "DB server is on"


@app.route("/new_patient", methods=["POST"])
def add_new_patient_to_server():
    """
    calls add_new_patient_worker which adds or updates the patient based on
    the entered data dictionary

    uses get_json function which receives in data and calls other functions
    that do the adding work

    in_data:
        dictionary format:
        [{
        "name": <string>
        "id": <integer>
        "heart_rate": <int1>
        "medical_image": <string1>
        "ecg_image": <string1>
        "m_i_name": <string1>
        "timestamp": <string1>
        }]

    Args:
        none

    Returns:
        string and 200 status code if done correctly
    """
    in_data = request.get_json()
    print("received in_data")
    message, status_code = add_new_patient_worker(in_data)
    print(message)
    print(status_code)
    return message, status_code


def add_new_patient_worker(in_data):
    """
    calls validation function and if the validation passes, the patient is
    either added or updated in the database by calling the specific function

    uses if statements to sort the flow of the data into the correct path

    Args:
        in_data: dictionary that has patient_name, patinet_id, heart_rate,
        medical_image, ecg_image, medical_image_name, and timestamp
        patient_name is a string
        patient_id is an int
        heart_rate is an int
        medical_image, ecg_image, medical_image_name, and timestamp
        are all strings

    Returns:
        string and 200 status code if done correctly
    """
    result = validate_new_patient_info(in_data)
    if result is not True:
        return result, 400
    pat = find_patient(in_data["id"])
    if pat:
        update_patient(in_data["name"],
                       in_data["id"],
                       in_data["heart_rate"],
                       in_data["ecg_image"],
                       in_data["medical_image"],
                       in_data["m_i_name"],
                       in_data["timestamp"])
        return "Patient successfully updated", 200
    else:
        add_patient(in_data["name"],
                    in_data["id"],
                    in_data["heart_rate"],
                    in_data["ecg_image"],
                    in_data["medical_image"],
                    in_data["m_i_name"],
                    in_data["timestamp"])
        return "Patient successfully added", 200


def validate_new_patient_info(in_data):
    """
    validates the information in the in_data dictionary by checking
    if each key is present and has the correct type

    uses for loops and if statements to loop through the dictionary and
    return the necessary validation messages

    Args:
        in_data: dictionary that has patient_name, patinet_id, heart_rate,
        medical_image, ecg_image, medical_image_name, and timestamp
        patient_name is a string
        patient_id is an int
        heart_rate is an int
        medical_image, ecg_image, medical_image_name, and timestamp
        are all strings

    Returns:
        returns a validation error message if something is caught but otherwise
        returns True
    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    expected_keys = ["name", "id", "heart_rate", "medical_image", "ecg_image",
                     "m_i_name", "timestamp"]
    for key in expected_keys:
        if key not in in_data:
            return "Key {} is missing from POST data".format(key)
    expected_types = [str, int, int, str, str, str, str]
    for key, ex_type in zip(expected_keys, expected_types):
        if type(in_data[key]) is not ex_type:
            return "Key {}'s value has the wrong data type".format(key)
    print("validated")
    return True


def add_patient(patient_name, patient_id, heart_rate, ecg_image, medical_image,
                medical_image_name, timestamp):
    """
    calls a function to add the patient id, and based on the entries of the
    function, can also call functions that add name, ecg info, and medical
    image info based on if the information is provided in the gui.

    uses if statements to check if data is present for certain variables, and
    if they are present, then it is added to the database

    Args:
        patient_name is a string of name entered
        patient_id is an int of the medical record number
        heart_rate is an int of the calculated heart rate of the ecg image
        medical_image is a b64 string of the entered image
        ecg_image is a b64 string of the entered ecg image
        medical_image_name is the filename of the entered medical image
        timestamp is a string of the time at upload

    Returns:
        string and 200 status code if done correctly
    """
    add_patient_id(patient_id)
    if patient_name:
        add_patient_name(patient_name, patient_id)
    if len(ecg_image) > 0:
        add_patient_heart_rate(heart_rate, patient_id, ecg_image, timestamp)
    if len(medical_image) > 0:
        add_patient_medical_image(medical_image,
                                  medical_image_name, patient_id)
    return "Successfully added new patient", 200


def update_patient(patient_name, patient_id, heart_rate, ecg_image,
                   medical_image, medical_image_name, timestamp):
    """
    calls a function to add the patient id, and based on the entries of the
    function, can also call functions that add name, ecg info, and medical
    image info based on if the information is provided in the gui.

    uses if statements to check if data is present for certain variables, and
    if they are present, then it is added to the database

    Args:
        patient_name is a string of name entered
        patient_id is an int of the medical record number
        heart_rate is an int of the calculated heart rate of the ecg image
        medical_image is a b64 string of the entered image
        ecg_image is a b64 string of the entered ecg image
        medical_image_name is the filename of the entered medical image
        timestamp is a string of the time at upload

    Returns:
        string and 200 status code if done correctly
    """
    if patient_name:
        add_patient_name(patient_name, patient_id)
    if len(ecg_image) > 0:
        add_patient_heart_rate(heart_rate, patient_id, ecg_image, timestamp)
    if len(medical_image) > 0:
        add_patient_medical_image(medical_image,
                                  medical_image_name, patient_id)
    return "Successfully updated patient", 200


def add_patient_id(patient_id):
    """
    adds a new patient with the provided id number to the database

    uses mongomodel functions to add a new user and save it in the database
    this is only done if the patient id entered is not already in the database

    Args:
        patient_id: medical record number

    Returns:
        added_patient: the user class that was just added
    """
    patient = find_patient(patient_id)
    if patient:
        return "Patient ID {} already exists".format(patient.id), 400
    u = User(id=patient_id)
    added_patient = u.save()
    print("Successfully added new patient {}".format(added_patient))
    return added_patient


def add_patient_name(patient_name, patient_id):
    """
    adds a name of patient based on the id provided to the database

    uses mongomodel functions to add or replace the name of the user in the db

    Args:
        patient_id: medical record number
        patient_name: the name entered in the gui

    Returns:
        patient.name: name of the patient which was just changed from the
        function
    """
    patient = find_patient(patient_id)
    if patient is False:
        return "Patient ID {} not found in database".format(patient_id), 400
    patient.name = patient_name
    patient.save()
    print("Successfully added patient name with id {}".format(patient.id))
    return patient.name


def add_patient_heart_rate(heart_rate, patient_id, ecg_image, timestamp):
    """
    appends an ecg image string, the calculated heart rate, and timestamp
    to their respective lists in the database based on patient id

    uses mongomodel functions to access the lists of heart rates, ecg_data,
    and record_time and append function adds the inputted data to the lists

    Args:
        patient_id: medical record number
        heart_rate: calculated heart rate from the ecg image, calculated by the
        ecg_analysis code
        ecg_image: string of the ecg image converted to b64
        timestamp: is the time but in a string form to be successfully uploaded

    Returns:
        patient.heart_rates[-1] is the last added heart rate which was entered
        by the function
    """
    patient = find_patient(patient_id)
    if patient is False:
        return "Patient ID {} not found in database".format(patient_id), 400
    patient.heart_rates.append(heart_rate)
    patient.ECG_data.append(ecg_image)
    patient.record_time.append(timestamp)
    patient.save()
    print("Successfully added patient heartrate, ecg_data, "
          "and timestamp with id {}".format(patient_id))
    return patient.heart_rates[-1]


def add_patient_medical_image(medical_image, medical_image_name, patient_id):
    """
    appends a medical image string and medical image filename
    to their respective lists in the database based on patient id

    uses mongomodel functions to access the lists of medical_image_data, and
    medical_image_name and append function adds the inputted data to the lists

    Args:
        patient_id: medical record number
        medical_image: b64 string of medical image
        medical_image_name: filename of medical image entered for the monitor
        gui to access

    Returns:
        patient.medical_image_names[-1]: returns the last filename added to the
        medical image name list in the database
    """
    patient = find_patient(patient_id)
    if patient is False:
        return "Patient ID {} not found in database".format(patient_id), 400
    patient.medical_image_data.append(medical_image)
    patient.medical_image_names.append(medical_image_name)
    patient.save()
    print("Successfully added patient medical"
          " image with id {}".format(patient.id))
    return patient.medical_image_names[-1]


@app.route("/get_name_by_id/<patient_id>", methods=["GET"])
def get_patient_by_id_name_handler(patient_id):
    """Get patient name from db using patient id

    Calls worker function to get name or error message. Returns this
    with status code as int.

    Args:
        patient_id: id of the patient whose name will be retrieved
    Returns:
        str: message with name or error message
        int: status code of request
    """
    message, status_code = get_patient_by_id_name_worker(patient_id)
    return message, status_code


def get_patient_by_id_name_worker(patient_id):
    """Get patient name if it exists in DB

    First validate that the patient ID is numeric, then that this
    record is available in the database. If it is not then return
    error message with status code 400. If the patient ID is a
    valid input then retrieve the patient record from the database
    and get the name field of it. Return this with the status code
    200.

    Args:
        patient_id: id of the patient whose name will be retrieved
    Returns:
        str: message with name or error message
        int: status code of request
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    find_user = get_patient_by_id(patient_id)
    return find_user.name, 200


def validate_patient_id(patient_id):
    """Validate that patient id is numeric and in database

    Checks if patient id is numeric. If it is then it checks if the
    patient ID is found in the database. If it is then return True,
    if not return the error message.

    Args:
        patient_id: id of the patient whose name will be retrieved
    Returns:
        str: message error message
        OR
        bool: True if patient found
    """
    try:
        int(patient_id)
    except ValueError:
        return "The patient_id input is not numeric"
    if not (get_patient_by_id(int(patient_id))):
        return "The patient with id {} was not found".format(patient_id)
    else:
        return True


def get_patient_by_id(patient_id):
    """Get patient user object from db using patient id

    Creates mongo query for patient record with matching patient
    ID as the input. Then returns this user. If no matching record
    is found, then error is captured and returns False.

    Args:
        patient_id: id User object to be retrieved
    Returns:
        User: User object of patient record from database
        OR
        bool: False if no matching record.
    """
    try:
        user = User.objects.raw({"_id": patient_id}).first()
        return user
    except pymodm_errors.DoesNotExist:
        return False


@app.route("/get_all_ids", methods=["GET"])
def get_all_ids_handler():
    """Get all medical record ids from database

    Receive request from monitor.
    Use worker function to get all IDs and return
    these with paired status code.

    Returns:
        str: json string of list of IDs or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_all_ids_worker()
    return jsonify(message), status_code


def get_all_ids_worker():
    """Get all IDs from database and return in list

    Make mongo query to get all users. If there are no records,
    return False and 400 status code. If there are users, it gets
    their id and append this to a list, sorts this list. Then
    returns this list with status code 200.

    Returns:
        str: sorted list of IDs OR bool: False if none found
        int: status code (200 is OK, 400 is Bad Request)
    """
    ids_list = []
    try:
        user_list = User.objects.raw({})
        for user in user_list:
            ids_list.append(user.id)
        ids_list = sorted(ids_list)
        return ids_list, 200
    except pymodm_errors.DoesNotExist:
        return False, 400


@app.route("/get_hr/<patient_id>", methods=["GET"])
def get_hr_by_id_handler(patient_id):
    """Get all heart rate records from patient record

    Receive request from monitor.
    Use worker function to get all heart rates and return
    these with paired status code.

    Args:
        patient_id: id of heart rates to be retrieved

    Returns:
        str: json string of list of heart rates or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_hr_by_id_worker(patient_id)
    return jsonify(message), status_code


def get_hr_by_id_worker(patient_id):
    """Get all heart rates from database and return in list

    Validate that the patient ID is numeric and in database.
    If not return error message and 400 status code. If it is
    then call function to get the patient user object associated
    with input ID, then get the heart rates attribute. Return this
    as a list of integers.

    Args:
        patient_id: id of heart rates to be retrieved

    Returns:
        list: list of integers of heart rates from patient record
        OR
        str: error message

        int: status code (200 is OK, 400 is Bad Request)
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    patient = get_patient_by_id(patient_id)
    hr = patient.heart_rates
    return hr, 200


@app.route("/get_ecg/<patient_id>", methods=["GET"])
def get_ecg_by_id(patient_id):
    """Get ECG image strings for patient ID

    Receive request from monitor.
    Use worker function to get all ECG images in base 64
    encoding and return these with paired status code.

    Args:
        patient_id: id of ECG strings to be retrieved

    Returns:
        str: json string of list of ECG strings or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_ecg_by_id_worker(patient_id)
    return json.dumps(message), status_code


def get_ecg_by_id_worker(patient_id):
    """Get all ECG strings from database and return in list

    Validate that the patient ID is numeric and in database.
    If not return error message and 400 status code. If it is
    then call function to get the patient user object associated
    with input ID, then get the ECG data attribute. Return this
    as a list of base64 encoded strings of ECG images.

    Args:
        patient_id: id of ECG strings to be retrieved

    Returns:
        list: list of integers of ECG strings from patient record
        OR
        str: error message

        int: status code (200 is OK, 400 is Bad Request)
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    patient = get_patient_by_id(patient_id)
    ecg = patient.ECG_data
    return ecg, 200


@app.route("/get_ecg_times/<patient_id>", methods=["GET"])
def get_ecg_times_by_id(patient_id):
    """Get ECG time strings for patient ID

    Receive request from monitor.
    Use worker function to get all ECG times as
    strings and return these with paired status code.

    Args:
        patient_id: id of ECG upload times to be retrieved

    Returns:
        str: json string of list of ECG time strings or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_ecg_times_by_id_worker(patient_id)
    return json.dumps(message), status_code


def get_ecg_times_by_id_worker(patient_id):
    """Get all ECG time strings from database and return in list

    Validate that the patient ID is numeric and in database.
    If not return error message and 400 status code. If it is
    then call function to get the patient user object associated
    with input ID, then get the record time attribute. Return this
    as a list of strings of recorded ECG upload times.

    Args:
        patient_id: id of ECG upload time strings to be retrieved

    Returns:
        list: list of strings of times ECGs uploaded to patient record
        OR
        str: error message

        int: status code (200 is OK, 400 is Bad Request)
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    patient = get_patient_by_id(patient_id)
    ecg_times = patient.record_time
    return ecg_times, 200


@app.route("/get_med_img_names/<patient_id>", methods=["GET"])
def get_med_img_names_by_id(patient_id):
    """Get medical image names from patient record

    Receive request from monitor.
    Use worker function to get all medical image names from
    patient record with matching patient ID.
    Return these as strings with paired status code.

    Args:
        patient_id: id of medical image names to be retrieved

    Returns:
        str: json string of list of medical image names (strings)
             or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_med_img_names_by_id_worker(patient_id)
    return json.dumps(message), status_code


def get_med_img_names_by_id_worker(patient_id):
    """Get all ECG time strings from database and return in list

    Validate that the patient ID is numeric and in database.
    If not return error message and 400 status code. If it is
    then call function to get the patient user object associated
    with input ID, then get the medical_image_names attribute.
    Return this as a list of strings of uploaded medical image
    names with integer status code.

    Args:
        patient_id: id of medical image names to be retrieved

    Returns:
        list: list of strings of medical image names uploaded to patient record
        OR
        str: error message

        int: status code (200 is OK, 400 is Bad Request)
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    patient = get_patient_by_id(patient_id)
    med_img_names = patient.medical_image_names
    return med_img_names, 200


@app.route("/get_med_img/<patient_id>", methods=["GET"])
def get_med_img(patient_id):
    """Get medical images from patient record

    Receive request from monitor.
    Use worker function to get all medical images from
    patient record with matching patient ID. These are
    encoded as a base64 string.
    Return these as strings with paired status code.

    Args:
        patient_id: id of medical images to be retrieved

    Returns:
        str: json string of list of medical image data (strings)
             or error message
        int: status code (200 is OK, 400 is Bad Request)
    """
    message, status_code = get_med_img_worker(patient_id)
    return json.dumps(message), status_code


def get_med_img_worker(patient_id):
    """Get all medical image strings from database and return in list

    Validate that the patient ID is numeric and in database.
    If not return error message and 400 status code. If it is
    then call function to get the patient user object associated
    with input ID, then get the medical_image_data attribute.
    Return this as a list of strings of uploaded medical images
    with integer status code. These strings are a base64 encoding
    of the image.

    Args:
        patient_id: id of medical image names to be retrieved

    Returns:
        list: list of strings of medical images (base64) uploaded
              to patient record
        OR
        str: error message

        int: status code (200 is OK, 400 is Bad Request)
    """
    result = validate_patient_id(patient_id)
    if result is not True:
        return result, 400
    patient_id = int(patient_id)
    patient = get_patient_by_id(patient_id)
    med_img = patient.medical_image_data
    return med_img, 200


if __name__ == '__main__':
    init_server()
    app.run(host="0.0.0.0")
