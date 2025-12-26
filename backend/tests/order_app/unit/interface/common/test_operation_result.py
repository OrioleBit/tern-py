import pytest

from order_app.interface.common.operation_result import OperationResult


def test_only_success_or_error_is_allowed():
    with pytest.raises(ValueError) as exc_info:
        OperationResult()
    assert (
        str(exc_info.value)
        == "Either success or error must be provided, but not both or neither"
    )

    with pytest.raises(ValueError) as exc_info:
        OperationResult(success="value", error="error")
    assert (
        str(exc_info.value)
        == "Either success or error must be provided, but not both or neither"
    )


def test_access_success_on_error_result():
    result = OperationResult(error="Some error")
    with pytest.raises(ValueError) as exc_info:
        _ = result.success
    assert str(exc_info.value) == "Cannot access success value on error result"


def test_access_error_on_success_result():
    result = OperationResult(success="Some value")
    with pytest.raises(ValueError) as exc_info:
        _ = result.error
    assert str(exc_info.value) == "Cannot access error value on success result"
