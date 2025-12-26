import pytest

from order_app.application.common.result import Result


def test_only_value_or_error_is_allowed():
    with pytest.raises(ValueError) as exc_info:
        Result()
    assert (
        str(exc_info.value)
        == "Either value or error must be provided, but not both or neither"
    )

    with pytest.raises(ValueError) as exc_info:
        Result(_value="value", _error="error")
    assert (
        str(exc_info.value)
        == "Either value or error must be provided, but not both or neither"
    )


def test_access_value_on_error_result():
    result = Result(_error="Some error")
    with pytest.raises(ValueError) as exc_info:
        _ = result.value
    assert str(exc_info.value) == "Cannot access value on error result"


def test_access_error_on_success_result():
    result = Result(_value="Some value")
    with pytest.raises(ValueError) as exc_info:
        _ = result.error
    assert str(exc_info.value) == "Cannot access error on success result"
