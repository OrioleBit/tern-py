from abc import ABC, abstractmethod

from order_app.application.dtos.user.login import LoginUserResponseDto
from order_app.application.dtos.user.register import UserResponse
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.user_vm import UserViewModel


class RegisterPresenter(ABC):
    @abstractmethod
    def present_success(self, user_response: UserResponse) -> UserViewModel:
        pass

    @abstractmethod
    def present_error(self, error: str, code: str | None = None) -> ErrorViewModel:
        pass


class LoginPresenter(ABC):
    @abstractmethod
    def present_success(self, user: LoginUserResponseDto) -> str:
        pass

    @abstractmethod
    def present_error(self, error: str, code: str | None = None) -> ErrorViewModel:
        pass
