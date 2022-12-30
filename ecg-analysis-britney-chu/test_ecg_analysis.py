import pytest
import numpy as np
import math
import logging
from testfixtures import LogCapture


@pytest.mark.parametrize("input, expected1, expected2",
                         [([['0', '-0.145'],
                            ['0.003', '0.309'],
                            ['0.006', '0.244']],
                           [0, 0.003, 0.006], [-0.145, 0.309, 0.244]),
                          ([['0', 'NaN'],
                            ['0.003', '0.309'],
                            ['0.006', '0.244']],
                           [0.003, 0.006], [0.309, 0.244]),
                          ([['0', 'hello'],
                            ['hello', '0.309'],
                            ['0.006', '0.244']],
                           [0.006], [0.244]),
                          ([['0', '--'],
                            ['0.006', '0.244']],
                           [0.006], [0.244]),
                          ([['0', '++'],
                            ['one', '0.309'],
                            ['0.006', '0.244']],
                           [0.006], [0.244])])
def test_parse_data(input, expected1, expected2):
    from ecg_analysis import parse_data
    with LogCapture() as log_c:
        answer = parse_data(input)
    assert answer[0] == expected1 and answer[1] == expected2


@pytest.mark.parametrize("input, expected1, expected2",
                         [([['0', 'NaN'],
                            ['0.003', '0.309'],
                            ['0.006', '0.244']],
                           [0.003, 0.006], [0.309, 0.244]),
                          ([['0', 'hello'],
                            ['0.0', '0.309'],
                            ['0.006', '0.244']],
                           [0.0, 0.006], [0.309, 0.244]),
                          ([['0', '--'],
                            ['0.006', '0.244']],
                           [0.006], [0.244]),
                          ([['0', 'one'],
                            ['0.0', '0.309'],
                            ['0.006', '0.244']],
                           [0.0, 0.006], [0.309, 0.244])])
def test_parse_data_reports_error(input, expected1, expected2):
    logging.basicConfig(filename="test.log", filemode="w", level=logging.INFO)
    from ecg_analysis import parse_data
    with LogCapture() as log_c:
        answer = parse_data(input)
    log_c.check(("root", "ERROR",
                 "data entry contains at least one value that is NaN"))


@pytest.mark.parametrize("input, expected1, expected2",
                         [([['0', '-0.145'],
                            ['0.003', '0.309'],
                            ['0.006', '0.244']],
                           [0, 0.003, 0.006], [-0.145, 0.309, 0.244]),
                          ([['0', '1.1'],
                            ['0.003', '0.309'],
                            ['0.006', '0.244']],
                           [0, 0.003, 0.006], [1.1, 0.309, 0.244])])
def test_parse_data_reports_no_error(input, expected1, expected2):
    logging.basicConfig(filename="test.log", filemode="w", level=logging.INFO)
    from ecg_analysis import parse_data
    with LogCapture() as log_c:
        answer = parse_data(input)
    log_c.check()


@pytest.mark.parametrize("input, expected",
                         [([0.0, 1.1, 2.2, 3.3, 4.4, 5.5], 5.5),
                          ([10.1, 20.1, 30.1, 40.1, 50.1], 40),
                          ([-5.0, 5.0], 10)])
def test_find_duration(input, expected):
    from ecg_analysis import find_duration
    answer = find_duration(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [([0.0, 1.1, 2.2, 3.3, 4.4, 5.5], (0.0, 5.5)),
                          ([10.1, 20.1, 30.1, 40.1, 50.1], (10.1, 50.1)),
                          ([-5.0, 0, 1, 2, 5.0], (-5.0, 5.0)),
                          ([1, 1, 1, 1], (1, 1)),
                          ([1], (1, 1))])
def test_voltage_extremes(input, expected):
    from ecg_analysis import voltage_extremes
    answer = voltage_extremes(input)
    assert answer == expected


@pytest.mark.parametrize("input, input2, expected",
                         [(60, [1, 2, 3, 4, 5, 6, 7], 7),
                          (120.1, [1, 2, 3, 4], 2)])
def test_heart_rate(input, input2, expected):
    from ecg_analysis import heart_rate
    answer = heart_rate(input, input2)
    assert answer == expected


@pytest.mark.parametrize("input, input2, expected",
                         [([1, 2, 3, 4, 5, 6, 7], np.array([0, 1]), [1, 2])])
def test_beat_time(input, input2, expected):
    from ecg_analysis import beat_time
    answer = beat_time(input, input2)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [([0.0, 1.1, 2.2, 3.3, 4.4, 5.5], 1.1),
                          ([10.1, 20.1, 30.1, 40.1, 50.1], 10),
                          ([-5.0, 0, 1, 2, 5.0], 5),
                          ([1, 1, 1, 1], 0)])
def test_find_delta(input, expected):
    from ecg_analysis import find_delta
    answer = find_delta(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected",
                         [([1, 2, 3, 4, 5, 6], 3.89)])
def test_calc_RMS(input, expected):
    from ecg_analysis import calc_RMS
    answer = calc_RMS(input)
    assert answer == expected


@pytest.mark.parametrize("input, input2, expected, expected2",
                         [(.004, np.sin(np.arange(0, 2 * math.pi, .004)),
                           np.sin(np.arange(0, 2 * math.pi, .004)), False),
                          (.004,
                           np.sin(np.arange(0, 2 * math.pi, .004)*10000000),
                           np.sin(np.arange(0, 2 * math.pi, .004)*10000000),
                           True)])
def test_low_filter(input, input2, expected, expected2):
    from ecg_analysis import low_filter
    answer1, answer2 = low_filter(input, input2)
    assert answer2 == expected2


@pytest.mark.parametrize("input, input2, expected, expected2",
                         [(.004, np.sin(np.arange(0, 2 * math.pi, .004)),
                           np.sin(np.arange(0, 2 * math.pi, .004)), True),
                          (.004,
                           np.sin(np.arange(0, 2 * math.pi, .004)*10000000),
                           np.sin(np.arange(0, 2 * math.pi, .004)*10000000),
                           False)])
def test_high_filter(input, input2, expected, expected2):
    from ecg_analysis import high_filter
    answer1, answer2 = high_filter(input, input2)
    assert answer2 == expected2


@pytest.mark.parametrize("input, expected",
                         [("./test_data/test_data1.csv", 'test_data1.json'),
                          ("./test_data/test_data35.csv", 'test_data35.json')])
def test_get_filenumber(input, expected):
    from ecg_analysis import get_filenumber
    answer = get_filenumber(input)
    assert answer == expected


@pytest.mark.parametrize("input, input2",
                         [(-400, 400),
                          (-400.1, 400.1)])
def test_check_extremes_error(input, input2):
    logging.basicConfig(filename="test.log", filemode="w", level=logging.INFO)
    from ecg_analysis import check_extremes
    with LogCapture() as log_c:
        answer = check_extremes(input, input2)
    log_c.check(("root", "WARNING",
                 "contains voltages beyond +/- 300mV"))


@pytest.mark.parametrize("input, input2",
                         [(-300, 300),
                          (-100, 100)])
def test_check_extremes_no_error(input, input2):
    logging.basicConfig(filename="test.log", filemode="w", level=logging.INFO)
    from ecg_analysis import check_extremes
    with LogCapture() as log_c:
        answer = check_extremes(input, input2)
    log_c.check()
