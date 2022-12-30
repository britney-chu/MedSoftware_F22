import pytest


@pytest.mark.parametrize("input, expected",
                         [("TACHYCARDIC", True),
                          ("tachycardic", True),
                          ("blah blah", False),
                          (" tachycardic ", True),
                          (".tachycardic.", True),
                          ("-tachycardic-", True),
                          ("atachycardica", True),
                          ("123tachycardica123", True),
                          ("cidracyhcat", False)])
def test_is_tachycardia(input, expected):
    from tachycardia import is_tachycardic
    answer = is_tachycardic(input)
    assert answer == expected
