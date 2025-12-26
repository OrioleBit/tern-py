from abc import ABC, abstractmethod

from order_app.application.dtos.user.login import LoginUserResponseDto
from order_app.application.dtos.user.register import UserResponse
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.user_vm import (
    LoginUserViewModel,
    RegisterUserViewModel,
)


class RegisterPresenter(ABC):
    @abstractmethod
    def present_success(self, user_response: UserResponse) -> RegisterUserViewModel:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def present_error(self, error: str, code: str | None = None) -> ErrorViewModel:
        raise NotImplementedError  # pragma: no cover


class LoginPresenter(ABC):
    @abstractmethod
    def present_success(self, user: LoginUserResponseDto) -> LoginUserViewModel:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def present_error(self, error: str, code: str | None = None) -> ErrorViewModel:
        raise NotImplementedError  # pragma: no cover
