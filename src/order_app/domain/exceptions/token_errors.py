from order_app.domain.exceptions.base import DomainError


class JwtError(DomainError):
    """Base class for JWT errors in the domain."""

    pass


class TokenExpiredError(JwtError):
    """Raised when a JWT has expired."""

    pass


class InvalidTokenError(JwtError):
    """Raised when a JWT is invalid."""

    pass
