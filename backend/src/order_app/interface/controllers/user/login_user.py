from dataclasses import dataclass

from order_app.application.dtos.user.login import LoginUserRequestDto
from order_app.application.use_cases.user.login import LoginUserUseCase
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.presenters.base.user import LoginPresenter
from order_app.interface.view_models.user_vm import LoginUserViewModel


@dataclass
class LoginUserInputDto:
    email: str
    password: str


@dataclass
class LoginUserController:
    login_user_use_case: LoginUserUseCase
    presenter: LoginPresenter

    def handle(self, input: LoginUserInputDto) -> OperationResult[LoginUserViewModel]:
        request_dto = LoginUserRequestDto(email=input.email, password=input.password)
        result = self.login_user_use_case.execute(request_dto)

        if result.is_success:
            return OperationResult.succeed(self.presenter.present_success(result.value))
        else:
            error_vm = self.presenter.present_error(
                result.error.message, result.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
