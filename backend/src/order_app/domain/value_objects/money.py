from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TWO_PLACES = Decimal("0.01")


@dataclass
class Money:
    amount: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < Decimal("0"):
            raise ValueError("Money amount cannot be negative")

        normalized = self.amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", normalized)

    def __add__(self, other: "Money") -> "Money":
        self.assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, value: int | Decimal) -> "Money":
        if isinstance(value, int) or isinstance(value, Decimal):
            if value < 0:
                raise ValueError("Value must be non-negative")
        else:
            raise TypeError(f"Cannot multiply Money by {type(value)}")

        return (
            Money(self.amount * Decimal(value), self.currency)
            if isinstance(value, int)
            else Money(self.amount * value, self.currency)
        )

    __rmul__ = __mul__

    def __imul__(self, other):
        return self * other

    def assert_same_currency(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add Money with different currencies")

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"
