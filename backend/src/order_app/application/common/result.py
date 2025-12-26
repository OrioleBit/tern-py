from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Generic, Self, TypeVar

T = TypeVar("T")  # Success type


class ErrorCode(Enum):
    """Enumeration of possible error codes in the application layer."""

    NOT_FOUND = auto()
    FORBIDDEN = auto()
    VALIDATION = auto()
    ALREADY_EXISTS = auto()
    DOMAIN = auto()


@dataclass(frozen=True)
class Error:
    """Represents an error that occurred during use case execution."""

    code: ErrorCode
    message: str
    details: dict[str, Any] | None = None

    @classmethod
    def not_found(cls, entity: str, attr_name: str, attr_value: str) -> Self:
        """Create a NOT_FOUND error for a specific entity."""
        return cls(
            message=f"{entity} not found",
            code=ErrorCode.NOT_FOUND,
            details={"attr_name": attr_name, "attr_value": attr_value}
            if attr_name
            else None,
        )

    @classmethod
    def already_exists(cls, entity: str, attr_name: str, attr_value: str) -> Self:
        """Create an ALREADY_EXISTS error."""
        return cls(
            message=f"{entity} already exists",
            code=ErrorCode.ALREADY_EXISTS,
            details={"attr_name": attr_name, "attr_value": attr_value}
            if attr_name
            else None,
        )

    @classmethod
    def forbidden(
        cls,
        *,
        entity: str,
        action: str | None = None,
        entity_id: str | None = None,
    ) -> Self:
        """Create a FORBIDDEN error."""
        return cls(
            code=ErrorCode.FORBIDDEN,
            message="You do not have permission to perform this action",
            details={
                "entity": entity,
                "action": action,
                "entity_id": entity_id,
            }
            if entity
            else None,
        )

    @classmethod
    def domain(cls, message: str | None = None) -> Self:
        return cls(code=ErrorCode.DOMAIN, message=message)


@dataclass(frozen=True)
class Result(Generic[T]):
    """Represents the outcome of a use case execution as an Either type."""

    _value: T | None = None
    _error: Error | None = None

    def __post_init__(self):
        if (self._value is None and self._error is None) or (
            self._value is not None and self._error is not None
        ):
            raise ValueError(
                "Either value or error must be provided, but not both or neither"
            )

    @property
    def is_success(self) -> bool:
        """Check if the result represents a successful operation."""
        return self._value is not None

    @property
    def value(self) -> T:
        """Get the success value. Raises ValueError if result is an error."""
        if self._value is None:
            raise ValueError("Cannot access value on error result")
        return self._value

    @property
    def error(self) -> Error:
        """Get the error value. Raises ValueError if result is successful."""
        if self._error is None:
            raise ValueError("Cannot access error on success result")
        return self._error

    @classmethod
    def success(cls, value: T) -> Result[T]:
        """Create a successful result with the given value."""
        return cls(_value=value)

    @classmethod
    def failure(cls, error: Error) -> Result[T]:
        """Create a failed result with the given error."""
        return cls(_error=error)
