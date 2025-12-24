from order_app.application.dtos.user.login import LoginUserResponseDto
from order_app.application.dtos.user.register import UserResponse
from order_app.interface.presenters.base.user import RegisterPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.user_vm import UserViewModel


class WebRegisterUserPresenter(RegisterPresenter):
    def present_success(self, user_response: UserResponse) -> UserViewModel:
        return UserViewModel(
            id=str(user_response.id),
            name=user_response.name,
            email=user_response.email,
            role=user_response.role,
        )

    def present_error(self, error, code=None) -> ErrorViewModel:
        return ErrorViewModel(error, str(code))


class WebLoginUserPresenter(RegisterPresenter):
    def present_success(self, user_response: LoginUserResponseDto) -> UserViewModel:
        return UserViewModel(
            id=str(user_response.id),
            name=user_response.name,
            email=user_response.email,
            role=user_response.role,
        )

    def present_error(self, error, code=None) -> ErrorViewModel:
        return ErrorViewModel(error, str(code))
