from dataclasses import dataclass
from typing import Generic, TypeVar

from order_app.interface.view_models.error_vm import ErrorViewModel

T = TypeVar("T")


@dataclass
class OperationResult(Generic[T]):
    _success: T | None = None
    _error: ErrorViewModel | None = None

    def __init__(self, success: T | None = None, error: ErrorViewModel | None = None):
        if (success is None and error is None) or (
            success is not None and error is not None
        ):
            raise ValueError(
                "Either success or error must be provided, but not both or neither"
            )
        self._success = success
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._success is not None

    @property
    def success(self) -> T:
        """Returns the success value."""
        if self._success is None:
            raise ValueError("Cannot access success value on error result")
        return self._success

    @property
    def error(self) -> ErrorViewModel:
        """Returns the error details."""
        if self._error is None:
            raise ValueError("Cannot access error value on success result")
        return self._error

    @classmethod
    def succeed(cls, value: T) -> "OperationResult[T]":
        """Creates a successful result with the given value."""
        return cls(success=value)

    @classmethod
    def fail(cls, message: str, code: str | None = None) -> "OperationResult[T]":
        """Creates a failed result with the given error message and optional code."""
        return cls(error=ErrorViewModel(message, code))
