from order_app.domain.exceptions.base import DomainError


class JwtError(DomainError):
    """Base class for JWT errors in the domain."""

    pass


class TokenExpiredError(JwtError):
    """Raised when a JWT has expired."""

    def __init__():
        super().__init__("Token has expired")


class InvalidTokenError(JwtError):
    """Raised when a JWT is invalid."""

    def __init__():
        super().__init__("Invalid token")
