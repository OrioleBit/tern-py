from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorViewModel:
    message: str
    code: str | None = None
