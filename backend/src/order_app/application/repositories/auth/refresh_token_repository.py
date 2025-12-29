from abc import ABC, abstractmethod
from uuid import UUID

from order_app.domain.entities.auth.refresh_token import RefreshToken


class RefreshTokenRepository(ABC):
    @abstractmethod
    def save(self, refresh_token: RefreshToken):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_token(self, token: str) -> RefreshToken:
        """
        Retrieve a refresh token entity by its token string.

        Raises:
            RefreshTokenNotFoundError: If no refresh token exists with the given token
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def revoke_token(self, token_id: UUID):
        """
        Revoke a refresh token.

        Raises:
             RefreshTokenNotFoundError: If no refresh token exists with the given token
        """
        raise NotImplementedError  # pragma: no cover
