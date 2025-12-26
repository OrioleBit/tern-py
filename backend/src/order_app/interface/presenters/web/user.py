from order_app.application.dtos.user.login import LoginUserResponseDto
from order_app.application.dtos.user.register import UserResponse
from order_app.interface.presenters.base.user import LoginPresenter, RegisterPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.user_vm import (
    LoginUserViewModel,
    RegisterUserViewModel,
    UserViewModel,
)


class WebRegisterUserPresenter(RegisterPresenter):
    def present_success(self, user_response: UserResponse) -> RegisterUserViewModel:
        return RegisterUserViewModel(
            id=str(user_response.id),
            name=user_response.name,
            email=user_response.email,
            role=user_response.role,
        )

    def present_error(self, error, code=None) -> ErrorViewModel:
        return ErrorViewModel(error, str(code))


class WebLoginUserPresenter(LoginPresenter):
    def present_success(self, response: LoginUserResponseDto) -> LoginUserViewModel:
        return LoginUserViewModel(
            user=UserViewModel(
                id=str(response.id),
                name=response.name,
                email=response.email,
                role=response.role,
            ),
            access_token=response.access_token,
            expires_in=response.expires_in,
        )

    def present_error(self, error, code=None) -> ErrorViewModel:
        return ErrorViewModel(error, str(code))
