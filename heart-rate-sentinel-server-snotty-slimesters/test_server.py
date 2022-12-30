import pytest
from server import attending, patient
from datetime import datetime, time, date, timedelta
import logging
from testfixtures import LogCapture


@pytest.mark.parametrize("input, expected",
                         [({"patient_id": 1,
                            "attending_username": "Billy.B",
                            "patient_age": 10}, True),
                          (["patient_id", 1,
                            "attending_username", "Billy.B",
                            "patient_age", 10],
                           "POST data was not a dictionary"),
                          ({"wrong_key": 1,
                            "attending_username": "Billy.B",
                            "patient_age": 10},
                           "Key patient_id is missing from POST data"),
                          ({"patient_id": 1,
                            "attending_username": 1,
                            "patient_age": 10},
                           "Key attending_username's" +
                           " value has the wrong data type"),
                          ({"patient_id": "hello",
                            "attending_username": "Billy.B",
                            "patient_age": 10},
                           "The patient_id input is not numeric"),
                          ({"patient_id": 1,
                            "attending_username": "Billy.B",
                            "patient_age": "1a1"},
                           "The patient_age input is not numeric")])
def test_validate_new_patient_info(input, expected):
    from server import validate_new_patient_info
    answer = validate_new_patient_info(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"patient_id": 1,
                            "attending_username": "Billy.B",
                            "patient_age": 10},
                           ("Patient successfully added", 200)),
                          ({"patient_id": "AAA",
                            "attending_username": "Billy.B",
                            "patient_age": 10},
                           ("The patient_id input is not numeric", 400)),
                          ({"patient_id": 2,
                            "attending_username": "Chu.B",
                            "patient_age": 45},
                           ("Patient successfully added", 200))])
def test_add_new_patient_worker(input, expected):
    from server import add_new_patient_worker
    answer = add_new_patient_worker(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"username": "1.2",
                            "email": "Billy.B@gmail.com",
                            "phone": "1003002000"}, True),
                          (["username", 1,
                            "email", "Billy.B@gmail.com",
                            "phone", "1003002000"],
                           "POST data was not a dictionary"),
                          ({"wrong_key": 1,
                            "email": "Billy.B",
                            "phone": 10},
                           "Key username is missing from POST data"),
                          ({"username": 1,
                            "email": "2@2.com",
                            "phone": "1000000000"},
                           "Key username's" +
                           " value has the wrong data type"),
                          ({"username": 1,
                            "email": 2,
                            "phone": "1000000000"},
                           "Key username's" +
                           " value has the wrong data type")
                          ])
def test_validate_new_attending_info(input, expected):
    from server import validate_new_attending_info
    answer = validate_new_attending_info(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"username": "cai.d",
                            "email": "dcai@gmail.com",
                            "phone": "1001001000"},
                           ("Attendee successfully added", 200)),
                          ({"username": "a.d",
                            "email": "ad@gmail.com"
                            },
                           ("Key phone is missing from POST data", 400))
                          ])
def test_add_new_attending_worker(input, expected):
    from server import add_new_attending_worker
    answer = add_new_attending_worker(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [(1, {"patient_id": 1,
                               "attending_username": "Cai.D",
                               "patient_age": 10,
                               "heart_rate": [1, 2],
                               "time_stamp": [1, 2],
                               "status": ["not tachycardic",
                                          "not tachycardic"]}),
                          (2, {"patient_id": 2,
                               "attending_username": "Chu.B",
                               "patient_age": 45,
                               "heart_rate": [1],
                               "time_stamp": [1],
                               "status": ["not tachycardic"]})
                          ])
def test_find_patient(input, expected):
    from server import find_patient, init_server
    init_server()
    answer = find_patient(input)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected",
                         [({"patient_id": 1,
                            "attending_username": "Cai.D",
                            "patient_age": 10,
                            "heart_rate": [],
                            "status": [],
                            "time_stamp": []}, 80,
                           {"patient_id": 1,
                            "attending_username": "Cai.D",
                            "patient_age": 10,
                            "heart_rate": [80],
                            "status": ["not tachycardic"],
                            "time_stamp":
                            [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]})])
def test_heart_rate(input1, input2, expected):
    from server import heart_rate
    answer = heart_rate(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [(1, 1.5),
                          (2, 1)])
def test_get_avg_hr(input, expected):
    from server import get_avg_hr
    answer = get_avg_hr(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [("one", "The patient_age input is not numeric"),
                          ("1", True),
                          (100, "The patient with id 100 was not found")])
def test_validate_patient_id(input, expected):
    from server import validate_patient_id, init_server
    init_server()
    answer = validate_patient_id(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected, expected2",
                         [(1, [1, 2], 200),
                          (8, "The patient with id 8 was not found", 400)])
def test_get_heart_rates_worker(input, expected, expected2):
    from server import get_heart_rates_worker, init_server
    init_server()
    answer, code = get_heart_rates_worker(input)
    assert answer == expected and code == expected2


@pytest.mark.parametrize("input, expected",
                         [("Cai.D", {"username": "Cai.D",
                                     "email": "dcai@gmail.com",
                                     "phone": "330-906-3268"}),
                          ("time.w", False)
                          ])
def test_find_attending(input, expected):
    from server import find_attending, init_server
    init_server()
    answer = find_attending(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [("Chu.B", [{"patient_id": 2,
                                      'last_heart_rate': 1,
                                      'last_time': 1,
                                      'status': "not tachycardic"}]),
                          ("time.w", [])
                          ])
def test_find_patients_for_attending_worker(input, expected):
    from server import find_patients_for_attending_worker
    from server import patient, attending, init_server
    init_server()
    answer = find_patients_for_attending_worker(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [([{"patient_id": 2,
                             "attending_username": "Chu.B",
                             "patient_age": 45,
                             'heart_rate': [1],
                             'time_stamp': [1],
                             'status': ["not tachycardic"]}],
                          [{"patient_id": 2,
                            'last_heart_rate': 1,
                            'last_time': 1,
                            'status': "not tachycardic"}])
                          ])
def test_create_dict_for_attending_patients(input, expected):
    from server import create_dict_for_attending_patients
    from server import patient, attending, init_server
    init_server()
    answer = create_dict_for_attending_patients(input)
    assert answer == expected


@pytest.mark.parametrize("input, input1, expected",
                         [(151, 1, "not tachycardic"),
                          (152, 1, "tachycardic"),
                          (151, 2, "not tachycardic"),
                          (152, 2, "tachycardic"),
                          (137, 3, "not tachycardic"),
                          (138, 4, "tachycardic"),
                          (137, 4, "not tachycardic"),
                          (138, 3, "tachycardic"),
                          (133, 5, "not tachycardic"),
                          (134, 5, "tachycardic"),
                          (133, 7, "not tachycardic"),
                          (134, 7, "tachycardic"),
                          (130, 8, "not tachycardic"),
                          (131, 8, "tachycardic"),
                          (130, 11, "not tachycardic"),
                          (131, 11, "tachycardic"),
                          (119, 12, "not tachycardic"),
                          (120, 12, "tachycardic"),
                          (119, 15, "not tachycardic"),
                          (120, 15, "tachycardic"),
                          (100, 16, "not tachycardic"),
                          (101, 16, "tachycardic"),
                          ])
def test_diagnosis(input, input1, expected):
    from server import diagnosis
    answer = diagnosis(input, input1)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"patient_id": 1,
                            "heart_rate_average_since":
                            "2022-11-03 06:18:20"}, True),
                          ({"patient_id": "1",
                            "heart_rate_average_since":
                            "2022-11-03 06:18:20"}, True),
                          ({"blah": 1,
                            "heart_rate_average_since":
                            "2022-11-03 06:18:20"},
                           "Key patient_id is missing from POST data"),
                          ({"patient_id": [1, 2, 3],
                            "heart_rate_average_since":
                            "2022-11-03 06:18:20"},
                           "Key patient_id's value has the wrong data type"),
                          ({"patient_id": "one",
                            "heart_rate_average_since":
                            "2022-11-03 06:18:20"},
                           "The patient_id input is not numeric")])
def test_validate_time_input(input, expected):
    from server import validate_time_input
    answer = validate_time_input(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected, expected2",
                         [({"patient_id": 4,
                            "heart_rate_average_since": "2022-11-03 06:18:20"},
                           90.0, 200),
                          ({"patient_id": "four",
                            "heart_rate_average_since": "2022-11-03 06:18:20"},
                           "The patient_id input is not numeric", 400)])
def test_get_interval_average_worker(input, expected, expected2):
    from server import get_interval_average_worker, init_server
    init_server()
    answer, answer2 = get_interval_average_worker(input)
    assert answer == expected and answer2 == expected2


@pytest.mark.parametrize("input, input2, expected",
                         [(4, "2022-11-03 06:18:20", [80, 90, 100]),
                          (4, "2022-11-04 06:18:20", [90, 100])])
def test_get_hr_interval(input, input2, expected):
    from server import get_hr_interval, init_server, find_patient
    init_server()
    patient = find_patient(input)
    answer = get_hr_interval(patient, input2)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [([1, 2, 3], 2),
                          ([10, 20], 15.0)])
def test_average_list(input, expected):
    from server import average_list
    answer = average_list(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected1, expected2",
                         [({"patient_id": 1,
                            "attending_username": "Bocci.P",
                            "patient_age": 45,
                            "heart_rate": [152],
                            "time_stamp": ["10/10"],
                            "status": ["tachycardic"]},
                           "Email from hospital_alerts@hospital.com"
                           " to pboch@gmail.com", 200),
                          ({"patient_id": "hello",
                            "attending_username": "pboch@gmail.com",
                            "patient_age": 45,
                            "heart_rate": [152],
                            "time_stamp": ["10/10"],
                            "status": ["tachycardic"]},
                           "The patient_age input is not numeric", 400)])
def test_send_email(input, expected1, expected2):
    from server import send_email, init_server
    init_server()
    answer, answer2 = send_email(input)
    assert answer == expected1 and answer2 == expected2


@pytest.mark.parametrize("input, expected",
                         [({"patient_id": "1",
                            "patient_age": 25,
                            "heart_rate": [10]},
                           "The patient number 1 is 25 years old and"
                           " recorded a heart rate of 10 which is considered"
                           " tachycardic")])
def test_create_email(input, expected):
    from server import create_email
    answer = create_email(input)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected",
                         [("hello@hello.com", "hello",
                           {"from_email": "hospital_alerts@hospital.com",
                            "to_email": "hello@hello.com",
                            "subject": "Tachycardic HR ALERT",
                            "content": "hello"})])
def test_create_out_data(input1, input2, expected):
    from server import create_out_data
    answer = create_out_data(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input, input1, input2, expected", [
    ("username",
     "email@email.com",
     "123-456-7890",
     "new attendee username has been added with email: email@email.com")
    ])
def test_log_add_attending(input, input1, input2, expected):
    from server import add_attending
    with LogCapture() as log_c:
        add_attending(input, input1, input2)
    log_c.check(("root", "INFO", expected))


@pytest.mark.parametrize("input, input1, input2, expected", [
    (5, "username", 40,
     "new patient with id 5 has been added")
    ])
def test_log_add_patient(input, input1, input2, expected):
    from server import add_patient
    with LogCapture() as log_c:
        add_patient(input, input1, input2)
    log_c.check(("root", "INFO", expected))


@pytest.mark.parametrize("input, input1, expected", [
    ({"patient_id": 1,
      "attending_username": "Bocci.P",
      "patient_age": 45,
      "heart_rate": [152],
      "time_stamp": [1],
      "status": ["tachycardic"]}, 160,
     "patient with patient id:1, last heart rate:160, "
     "and attending physician e-mail:pboch@gmail.com was tachycardic")
    ])
def test_heart_rate_logging(input, input1, expected):
    from server import heart_rate, find_attending
    with LogCapture() as log_c:
        heart_rate(input, input1)
    log_c.check(("root", "WARNING", expected))
