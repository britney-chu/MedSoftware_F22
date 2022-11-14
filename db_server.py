# db_server.py

from flask import Flask, request, jsonify
import logging

"""
    Database format:  A list of patient dictionaries

    [{
    "name": <string>,
    "id": <integer>,
    "blood_type": <string>,
    "test_name": [<string1>, <string2>, ...],
    "test_result": [<string>, <string2>, ...]
    }]
"""

# Create a global variable to hold the database
db = []

# Create an instance of the Flask server
app = Flask(__name__)


@app.route("/", methods=["GET"])
def server_on():
    """GET route to indicate that server is turned on
    """
    return "DB server is on"


def add_patient(patient_name, patient_id, blood_type):
    """ Appends a new patient dictionary to the database list

    This function receives basic information on a new patient, creates a
    dictionary containing that information, as well as empty lists to hold
    test names and results to be added in the future, and appends this
    dictionary to the database list.

    The database is being stored in an internal global variable.  As this
    variable is a list that has already been created, and a list is a
    mutable data type, the use of the "global" keyword is not required.

    Args:
        patient_name (str): Full name of patient
        patient_id (int): The medical record number of the patient
        blood_type (str): Blood type of the patient

    Returns:
        None

    """
    new_patient = {"name": patient_name,
                   "id": patient_id,
                   "blood_type": blood_type,
                   "test_name": [],
                   "test_result": []}
    db.append(new_patient)
    print_database()  # Print so I can see what changes made


def print_database():
    """Print the database to the console in order to visual changes to the
    database during server operation.
    """
    print("\n** Database Output **")
    for i, patient in enumerate(db):
        print("{}: {}".format(i, patient))
    print("\n")


def init_server():
    """Initializes server and database upon program start

    This function will contain any code that should be executed upon the
    initial start of the server.  This could include any connections to an
    external database, initial database entries, logging set-up, etc.  As this
    version of the program is using an internal variable for the database, it
    is simply adding some initial patients to the database for testing
    purposes.

    Returns:
        None
    """
    add_patient("Ann Ables", 1, "A+")
    add_patient("Bob Boyles", 2, "B+")
    # initialization of logging could be added here
    logging.basicConfig(filename="server.log", filemode='w')


@app.route("/new_patient", methods=["POST"])
def add_new_patient_to_server():
    """POST route to receive information about a new patient and add the
       patient to the database

    This "Flask handler" function receives a POST request to add a new patient
    to the database.  The POST request should receive a dictionary encoded as
    a JSON string in the following format:

        {"name": str,
         "id": int,
         "blood_type": str}

    The value for "name" is a string that should contain the full name of the
    patient.  The value of "id" is an integer that is the medical record
    number for the patient.  The value of "blood_type" is a string that
    contains the blood type of the patient (O+, O-, A+, A-, B+, B-, AB+, AB-).

    The function first receives the dictionary sent with the POST request.  It
    then calls a worker function to act on the data.  It finally returns the
    resulting message and status code.
    """
    # Receive data from POST request
    in_data = request.get_json()
    # Call other functions to do all the work
    message, status_code = add_new_patient_worker(in_data)
    # Return information
    return message, status_code


def add_new_patient_worker(in_data):
    """Implements the '/new_patient' route

    This function performs the data validation and implementation for the
    `/new_patient` route which adds a new patient to the database.  It first
    calls a function that validates that the necessary keys and value data
    types exist in the input dictionary.  If the necessary information does
    not exist, the function returns an error message and a status code of 400.
    Otherwise, another function is called and sent the necessary information to
    add a new patient to the database.  A success message and a 200 status code
    is then returned.

    Args:
        in_data (dict): Data received from the POST request.  Should be a
        dictionary with the format found in the docstring of the
        "add_new_patient_to_server" function, but that needs to be verified

    Returns:
        str, int: a message with information about the success or failure of
            the operation and a status code

    """
    expected_keys = ["name", "id", "blood_type"]
    expected_types = [str, int, str]
    result = dictionary_validation(in_data, expected_keys, expected_types)
    if result is not True:
        return result, 400
    add_patient(in_data["name"],
                in_data["id"],
                in_data["blood_type"])
    return "Patient successfully added", 200


def dictionary_validation(in_data, expected_keys, expected_types):
    """Validates that input data is a dictionary with correct information

    This function receives a dictionary that was sent with a POST request.  It
    also receives lists of the keys and value data types that are expected to
    be in this dictionary.  The function then verifies that the expected keys
    are found in the dictionary and that the corresponding value data types
    are of the correct type.  An error message is returned if a key
    is missing or there is an invalid data type.  If keys and data types are
    correct, a value of True is returned.

    Args:
        in_data (dict): object received by the POST request
        expected_keys (list): keys that should be found in the POST request
            dictionary
        expected_types (list): the value data types that should be found in the
            POST request dictionary

    Returns:
        str: error message if there is a problem with the input data, or
        bool: True if input data is valid.

    """
    if type(in_data) is not dict:
        return "POST data was not a dictionary"
    for ex_key, ex_type in zip(expected_keys, expected_types):
        if ex_key not in in_data:
            return "Key {} is missing from POST data".format(ex_key)
        if type(in_data[ex_key]) is not ex_type:
            return "Key {}'s value has the wrong data type".format(ex_key)
    return True


@app.route("/add_test", methods=["POST"])
def add_test_flask_handler():
    """POST route to receive information about a test data to add to a patient
    record in the database.

    This "Flask handler" function receives a POST request to add a test result
    to a patient record in the database.  The POST request should receive a
    dictionary encoded as a JSON string in the following format:

        {"id": int,
         "test_name": str,
         "test_result": int}

    The value of "id" is an integer that is the medical record number for the
    patient.  The value of "test_name" is a string containing the name of the
    test.  The value of "test_result" is an integer containing the numeric
    result of the test.

    The function first receives the dictionary sent with the POST request.  It
    then calls a worker function to act on the data.  It finally returns the
    resulting message and status code.
    """

    in_data = request.get_json()
    msg, status_code = add_test_worker(in_data)
    return msg, status_code


def add_test_worker(in_data):
    """Implements the '/add_test' route

    This function performs the data validation and implementation for the
    `/add_test` route which adds a new test result to the database entry
    for a specific patient.  It first calls a function that validates that
    the necessary keys and value data types exist in the input dictionary.
    If the necessary information does not exist, the function returns an
    error message and a status code of 400.  Otherwise, another function is
    called and sent the necessary information to add the test results to
    the correct patient.  A success message and a 200 status code is then
    returned.

    Args:
        in_data (dict): Data received from the POST request.  Should be a
        dictionary with the format found in the docstring of the
        "add_test_flask_handler" function, but that needs to be verified

    Returns:
        str, int: a message with information about the success or failure of
            the operation and a status code
        """
    expected_keys = ["id", "test_name", "test_result"]
    expected_types = [int, str, int]
    msg = dictionary_validation(in_data, expected_keys, expected_types)
    if msg is not True:
        return msg, 400
    add_test_to_patient(in_data)
    return "Test added", 200


def find_patient(patient_id):
    """Finds a patient in the database with a given id.

    This function iterates through the database list and compares the patient
    id of each patient in the list against a target id.  When the target id is
    found, that patient is returned to the calling function.  If the target id
    is not found, a value of False is returned.

    Args:
        patient_id (int): the patient id of interest

    Returns:
        dict: patient information of patient with id that matches parameter id,
                or
        bool: False if no patient record with the parameter id is found.
    """
    for patient in db:
        if patient["id"] == patient_id:
            return patient
    return False


def add_test_to_patient(in_data):
    """Adds test result to target patient record

    A call to the "find_patient" function returns the patient dictionary of
    the patient with the "id" found in the "in_data" dictionary.  The
    "test_name" and "test_result" from the "in_data" dictionary are then
    appended to the appropriate list in the patient dictionary.

    Args:
        in_data (dict): Contains the patient id and test results to be added

    Returns:
        None
    """
    patient = find_patient(in_data["id"])
    patient["test_name"].append(in_data["test_name"])
    patient["test_result"].append(in_data["test_result"])
    print_database()


@app.route("/get_results/<patient_id>", methods=["GET"])
def get_results_flask_handler(patient_id):
    """GET route to obtain results for a specific patient

    This function implements a variable URL in which the server returns
    patient information.  The variable URL will contain the medical record
    number, or id, of the patient of interest.  This id is passed to a function
    that will retrieve the data for this function to return.

    Args:
        patient_id (str): the variable portion of the URL which should contain
            the patient medical record number

    Returns:
        str, int: message on result of request and the status code

    """
    result, status_code = get_results_worker(patient_id)
    return jsonify(result), status_code


def get_results_worker(patient_id):
    """Implements the "/get_results/<patient_id>" route

    This function receives, as a string, the portion of the variable URL that
    should contain the id number of the patient to retrieve.  The function
    first calls a validation function to ensure that the patient id is valid
    and that the patient exists in the database.  If not, an error message is
    returned with a status code of 400.  If the patient id is valid and there
    is a patient with that id, a call is made to a function to retrieve that
    patient, and the patient dictionary is returned with a status code of 200.

    Args:
        patient_id (str): patient id found in variable URL

    Returns:
        str, int: error message and 400 status code if patient_id parameter is
                    invalid, or
        dict, int: patient dictionary and 200 status code if patient_id matches
                    an entry in database

    """
    msg = validate_patient_id(patient_id)
    if msg is not True:
        return msg, 400
    patient = find_patient(int(patient_id))
    return patient, 200


def validate_patient_id(patient_id_str):
    """Validates that received patient id is an integer and that patient exists

    This function validates the information received by the variable URL
    "/get_results/<patient_id>".  First, it checks that the "patient_id"
    received represents a number.  It then checks that a patient exists in the
    database with that number.  If either of these conditions is not true,
    an error message string is returned.  If both are true, a value of True
    is returned to indicate a valid input.

    Args:
        patient_id_str (str): The portion of the variable URL that should
            contain the patient ID

    Returns:
        str: error message if validation fails, or
        bool: True if validation passes

    """
    try:
        patient_id = int(patient_id_str)
    except ValueError:
        return "Patient id provided was not an integer"
    patient = find_patient(patient_id)
    if patient is False:
        return "No patient with id provided was found"
    return True


if __name__ == '__main__':
    # Call function to initialize server and database
    init_server()
    # Start the server
    app.run()