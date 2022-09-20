import pytest

@pytest.mark.parametrize("input, expected", 
    [(85, "Normal"),
    (45, "Borderline Low"),
    (30, "Low")])
def test_check_HDL(input, expected):
    from blood_calculator import check_HDL
    answer = check_HDL(input) #answer and expected are just variable names you can name them other things
    assert answer == expected # python keyword. check boolean if true move on if false create assertion error


@pytest.mark.parametrize("input, expected", 
    [(125, "LDL is normal"),
    (145, "LDL is borderline high"),
    (170, "LDL is high"), 
    (200, "LDL is very high")])
def test_check_LDL(input, expected):
    from blood_calculator import check_LDL
    answer = check_LDL(input) #answer and expected are just variable names you can name them other things
    assert answer == expected # python keyword. check boolean if true move on if false create assertion error


@pytest.mark.parametrize("input, expected", 
    [(135, "Normal"),
    (210, "Borderline High"),
    (250, "High")])
def test_check_chol(input, expected):
    from blood_calculator import check_chol
    answer = check_chol(input) #answer and expected are just variable names you can name them other things
    assert answer == expected # python keyword. check boolean if true move on if false create assertion error
"""
def test_check_HDL_BorderlineLow():
    from blood_calculator import check_HDL
    answer = check_HDL(55)
    expected = "Borderline Low"
    assert answer == expected
"""

