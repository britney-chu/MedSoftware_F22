#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 12:31:46 2022

@author: dylancai
"""

import pytest
import ssl
from database_definition import User
from server import init_server
import base64
from datetime import datetime, time, date, timedelta
import logging
from testfixtures import LogCapture
from pymodm import connect, MongoModel, fields
from database_definition import User


@pytest.mark.parametrize("input, input1, expected",
                         [(101, "DYLAN", "DYLAN"),
                          (102, "dylan", "dylan"),
                          (103, "britney", "britney")
                          ])
def test_find_patient(input, input1, expected):
    from server import add_patient_id, add_patient_name
    init_server()
    add_patient_id(input)
    add_patient_name(input1, input)
    pat = User.objects.raw({"_id": input}).first()
    pat.delete()
    answer = pat
    if answer:
        assert answer.name == expected
    else:
        assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"name": "dylan", "id": 1,
                            "heart_rate": 12,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"}, True),
                          (["name", "dylan", "id", 1,
                            "heart_rate", 12,
                            "medical_image", "medical_image_string",
                            "ecg_image", "ecg_image_string",
                            "m_i_name", "medical_image_name",
                            "timestamp", "1:23:45"],
                           "POST data was not a dictionary"),
                          ({"wrong_key": "dylan", "id": 1,
                            "heart_rate": 12,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                           "Key name is missing from POST data"),
                          ({"name": "dylan", "id": 1,
                            "heart_rate": True,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                           "Key heart_rate's" +
                           " value has the wrong data type"),
                          ({"name": "dylan", "id": 1,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                           "Key heart_rate is missing from POST data")])
def test_validate_new_patient_info(input, expected):
    from server import validate_new_patient_info
    answer = validate_new_patient_info(input)
    assert answer == expected


@pytest.mark.parametrize("input, input1, input2, input3, input4,"
                         "input5, input6, expected",
                         [("Dylan", 2, 13, "ecg_string", "mi_string",
                           "medical_image_name", "timestamp",
                          ("Successfully added new patient", 200)),
                          ("Dylan", 3, 13, "", "mi_string",
                           "medical_image_name", "timestamp",
                          ("Successfully added new patient", 200)),
                          ("Dylan", 4, 13, "ecg_string", "",
                           "medical_image_name", "timestamp",
                          ("Successfully added new patient", 200))])
def test_add_patient(input, input1, input2, input3,
                     input4, input5, input6, expected):
    from server import add_patient, find_patient
    answer = add_patient(input, input1, input2, input3,
                         input4, input5, input6)
    pat = find_patient(input1)
    pat.delete()
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [({"name": "dylan", "id": 350,
                            "heart_rate": 12,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                          ("Patient successfully added", 200)),
                          ({"name": "dylan", "id": 300,
                            "heart_rate": 12,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                          ("Patient successfully updated", 200)),
                          ({"name": "dylan",
                            "heart_rate": 12,
                            "medical_image": "medical_image_string",
                            "ecg_image": "ecg_image_string",
                            "m_i_name": "medical_image_name",
                            "timestamp": "1:23:45"},
                          ("Key id is missing from POST data", 400))])
def test_add_new_patient_worker(input, expected):
    from server import add_new_patient_worker
    from server import find_patient
    init_server()
    answer = add_new_patient_worker(input)
    if answer == ("Patient successfully added", 200):
        pat = find_patient(input["id"])
        pat.delete()
    elif answer == ("Patient successfully updated", 200):
        pat = find_patient(input["id"])
        pat.heart_rates = pat.heart_rates[:-1]
        pat.record_time = pat.record_time[:-1]
        pat.ECG_data = pat.ECG_data[:-1]
        pat.medical_image_names = pat.medical_image_names[:-1]
        pat.medical_image_data = pat.medical_image_data[:-1]
        pat.save()
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [(101, 101),
                          (300, ("Patient ID 300 already exists", 400))])
def test_add_patient_id(input, expected):
    from server import add_patient_id
    init_server()
    answer = add_patient_id(input)
    print(answer)
    if type(answer) is tuple:
        assert answer == expected
    else:
        find_pat = User.objects.raw({"_id": input}).first()
        find_pat.delete()
        assert answer.id == expected


@pytest.mark.parametrize("input, input1, expected",
                         [("DYLAN", 300, "DYLAN"),
                          ("Britney CHUCHU", 400, "Britney CHUCHU"),
                          ("Billy bob", 3000,
                           ("Patient ID 3000 not found in database", 400))])
def test_add_patient_name(input, input1, expected):
    from server import add_patient_name
    init_server()
    answer = add_patient_name(input, input1)
    assert answer == expected


@pytest.mark.parametrize("input, input1, input2, input3, expected",
                         [(50, 300, "ecg_string_shouldnotshow", "2:33pm", 50),
                          (50, 10024, "ecg_string_trial", "2:33pm",
                           ("Patient ID 10024 not found in database", 400))])
def test_add_patient_heart_rate(input, input1, input2, input3, expected):
    from server import add_patient_heart_rate, find_patient
    init_server()
    answer = add_patient_heart_rate(input, input1, input2, input3)
    pat = find_patient(input1)
    if pat:
        pat.heart_rates = pat.heart_rates[:-1]
        print(pat.heart_rates)
        pat.record_time = pat.record_time[:-1]
        pat.ECG_data = pat.ECG_data[:-1]
        pat.save()
    assert answer == expected


@pytest.mark.parametrize("input, input1, input2, expected",
                         [("medical_image_string", "medical_image_name",
                           300, "medical_image_name"),
                          ("medical_image_string", "medical_image_name", 1020,
                          ("Patient ID 1020 not found in database", 400))])
def test_add_patient_medical_image(input, input1, input2, expected):
    from server import add_patient_medical_image, find_patient
    init_server()
    answer = add_patient_medical_image(input, input1, input2)
    pat = find_patient(input2)
    if pat:
        pat.medical_image_names = pat.medical_image_names[:-1]
        pat.medical_image_data = pat.medical_image_data[:-1]
        pat.save()
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [("images/acl1.jpg", "/9j/4AAQSkZJRgABAgAA")
                          ])
def test_convert_file_to_b64(input, expected):
    from patient_gui import convert_file_to_b64
    init_server()
    answer = convert_file_to_b64(input)
    with open("images/acl1.jpg", "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    print(b64_string)
    assert answer[0:20] == expected


@pytest.mark.parametrize("input, expected",
                         [("one", "The patient_id input is not numeric"),
                          ("100", True),
                          (101, "The patient with id 101 was not found"),
                          ("101", "The patient with id 101 was not found")])
def test_validate_patient_id(input, expected):
    from server import validate_patient_id
    from database_definition import User
    answer = validate_patient_id(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected1, expected2",
                         [(100, "dylan", 200),
                          (400, "Britney CHUCHU", 200),
                          (2831, "The patient with id 2831 was not found",
                           400)])
def test_get_patient_by_id_name_worker(input, expected1, expected2):
    from server import get_patient_by_id_name_worker
    from database_definition import User
    answer, code = get_patient_by_id_name_worker(input)
    assert answer == expected1 and code == expected2


@pytest.mark.parametrize("input, expected",
                         [(100, "dylan"),
                          (101, False),
                          (400, "Britney CHUCHU")])
def test_get_patient_by_id(input, expected):
    from server import get_patient_by_id
    from database_definition import User
    answer = get_patient_by_id(input)
    if answer:
        answer = answer.name
    assert answer == expected


@pytest.mark.parametrize("expected1, expected2",
                         [([100, 300, 400, 500], 200)])
def test_get_all_ids_worker(expected1, expected2):
    from server import get_all_ids_worker
    from database_definition import User
    answer, code = get_all_ids_worker()
    assert answer == expected1 and code == expected2


@pytest.mark.parametrize("input, expected1, expected2",
                         [(100, [12, 12, 12, 12, 12, 12, 12], 200),
                          (101, "The patient with id 101 was not found",
                           400),
                          ("meep", "The patient_id input is not numeric",
                           400)])
def test_get_hr_by_id_worker(input, expected1, expected2):
    from server import get_hr_by_id_worker
    from database_definition import User
    answer, code = get_hr_by_id_worker(input)
    assert answer == expected1 and code == expected2


def test_b64_string_to_file():
    from monitor import file_to_b64_string
    from monitor import b64_string_to_file
    import filecmp
    import os
    b64str = file_to_b64_string("images/acl2.jpg")
    b64_string_to_file(b64str, "test_image_output.jpg")
    answer = filecmp.cmp("images/acl2.jpg",
                         "test_image_output.jpg")
    os.remove("test_image_output.jpg")
    assert answer


def test_file_to_b64_string():
    from monitor import file_to_b64_string
    b64str = file_to_b64_string("images/acl2.jpg")
    assert b64str[0:20] == "/9j/4AAQSkZJRgABAgAA"


@pytest.mark.parametrize("input, expected",
                         [("(101, 102, 103)", ['101', '102', '103']),
                          ("101, 102, 103", ['101', '102', '103']),
                          ("(((101, 102))), 103", ['101', '102', '103'])])
def test_get_time_list(input, expected):
    from monitor import get_time_list
    answer = get_time_list(input)
    assert answer == expected
