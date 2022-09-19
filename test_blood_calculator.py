import pytest

@pytest.mark.parametrize("input, expected", 
    [(85, "Normal"),
    (45, "Borderline Low"),
    (30, "Low")])
def test_check_HDL_Normal(input, expected):
    from blood_calculator import check_HDL
    answer = check_HDL(input) #answer and expected are just variable names you can name them other things

    assert answer == expected # python keyword. check boolean if true move on if false create assertion error
    
"""
def test_check_HDL_BorderlineLow():
    from blood_calculator import check_HDL
    answer = check_HDL(55)
    expected = "Borderline Low"
    assert answer == expected
"""

