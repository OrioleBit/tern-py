from abc import ABC, abstractmethod
from uuid import UUID

from order_app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        """
        Save a user to the repository.

        Raises:
            UserAlreadyExistsError: If a user with the same email already exists
        """
        raise NotImplementedError  # pragma: no cover

    def update(self, user: User) -> User:
        """
        Update an existing user in the repository.

        Raises:
            UserNotFoundError: If no user exists with the given ID
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by their unique ID.

        Raises:
            UserNotFoundError: If no user exists with the given ID
        """

        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email.

        Raises:
            UserNotFoundError: If no user exists with the given email
        """

        raise NotImplementedError  # pragma: no cover
