import pytest


@pytest.mark.parametrize("input, expected",
                         [(['Anne Boynton\n', '7.25\n',
                            'Seal,11.0,23.6,15.2,2.3,4.0,19.7,3.7\n',
                            'Events,5,0,2,3,9,1,2\n',
                            'O2,95,93,98,97,96,97,100\n'],
                           [{'First Name': 'Anne', 'Last Name': 'Boynton',
                             'Hours': 7.25,
                             'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                             'Events': [5, 0, 2, 3, 9, 1, 2],
                             'O2': [95, 93, 98, 97, 96, 97, 100]}])])
def test_parse_data(input, expected):
    from cpap_analysis import parseData
    answer = parseData(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [('Events,5,0,2,3,9,1,2\n'.split(",")[1:],
                           [5, 0, 2, 3, 9, 1, 2]),
                          ('Events,5,0,2,3,9,1,2'.split(",")[1:],
                           [5, 0, 2, 3, 9, 1, 2]),
                          ('Events,5,0,2,3,9,1,2,3,4,423\n'.split(",")[1:],
                           [5, 0, 2, 3, 9, 1, 2, 3, 4, 423])])
def test_to_int_list(input, expected):
    from cpap_analysis import to_int_list
    answer = to_int_list(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [('Seal,15.2,2.3,4.0,19.7,3.7\n'.split(",")[1:],
                           [15.2, 2.3, 4.0, 19.7, 3.7]),
                          ('Seal,15.2,2.3,4.0,19.7,3.7'.split(",")[1:],
                           [15.2, 2.3, 4.0, 19.7, 3.7]),
                          ('Seal,15.2,2.3,4.0,19.7,3.7,400.0\n'.split(",")[1:],
                           [15.2, 2.3, 4.0, 19.7, 3.7, 400.0])])
def test_to_float_list(input, expected):
    from cpap_analysis import to_float_list
    answer = to_float_list(input)
    assert answer == expected


@pytest.mark.parametrize("field, data_dict, expected",
                         [("Seal",
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           11.36),
                          ("Events",
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           3.14)])
def test_find_avg(field, data_dict, expected):
    from cpap_analysis import find_avg
    answer = find_avg(field, data_dict)
    assert answer == expected


@pytest.mark.parametrize("field, data_dict, value, expected",
                         [("Seal Average",
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           11.36,
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100],
                            'Seal Average': 11.36}),
                          ("Diagnosis",
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           'test diagnosis',
                           {'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100],
                            'Diagnosis': 'test diagnosis'})])
def test_add_to_record(field, data_dict, value, expected):
    from cpap_analysis import add_to_record
    answer = add_to_record(field, data_dict, value)
    assert answer == expected


@pytest.mark.parametrize("data_dict, expected",
                         [({'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           "normal"),
                          ({'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100, 5]},
                           "hypoxia"),
                          ({'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100, -2]},
                           "hypoxia")])
def test_check_o2(data_dict, expected):
    from cpap_analysis import check_o2
    answer = check_o2(data_dict)
    assert answer == expected


@pytest.mark.parametrize("data_dict, expected",
                         [({'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 0, 2, 3, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           "normal sleep"),
                          ({'First Name': 'Kamal', 'Last Name': 'Solaiman',
                            'Hours': 6.5,
                            'Seal': [27.9, 13.3, 15.5, 7.5, 6.1, 15.8],
                            'Events': [5, 6, 7, 1, 6, 0],
                            'O2': [99, 91, 98, 92, 98, 95]},
                           "hypoxia"),
                          ({'First Name': 'Kyaw', 'Last Name': 'Win',
                            'Hours': 8.2,
                            'Seal': [12.8, 23.4, 23.4, 22.4, 16.3],
                            'Events': [10, 7, 4, 2, 7, 7, 100, 2],
                            'O2': [94, 94, 94, 96, 96, 93, 98, 92]},
                           "hypoxia apnea"),
                          ({'First Name': 'Anne', 'Last Name': 'Boynton',
                            'Hours': 7.25,
                            'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 100, 2, 100, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           "apnea"),
                          ({'Seal': [11.0, 23.6, 15.2, 2.3, 4.0, 19.7, 3.7],
                            'Events': [5, 100, 2, 100, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           "apnea"),
                          ({'Events': [5, 100, 2, 100, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, 100]},
                           "apnea"),
                          ({'Events': [5, 100, 2, 100, 9, 1, 2],
                            'O2': [95, 93, 98, 97, 96, 97, -100]},
                           "hypoxia apnea")])
def test_do_diagnosis(data_dict, expected):
    from cpap_analysis import do_diagnosis
    answer = do_diagnosis(data_dict)
    assert answer == expected
