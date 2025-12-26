from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class JwtService(ABC):
    secret_key: str
    algorithm: str = field(default="HS256")
    expires_in: int = field(default=3600)  # in seconds

    @abstractmethod
    def generate_token(self, payload: dict) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """
        Raises:
            InvalidTokenError: If the token is invalid.
            TokenExpiredError: If the token has expired.
        """
        raise NotImplementedError  # pragma: no cover
