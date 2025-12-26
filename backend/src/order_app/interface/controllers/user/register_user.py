from dataclasses import dataclass

from order_app.application.dtos.user.register import RegisterUserRequestDto
from order_app.application.use_cases.user.register import RegisterUserUseCase
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.presenters.base.user import RegisterPresenter
from order_app.interface.view_models.user_vm import RegisterUserViewModel


@dataclass
class RegisterUserInputDto:
    name: str
    email: str
    password: str


@dataclass
class RegisterUserController:
    register_user_use_case: RegisterUserUseCase
    presenter: RegisterPresenter

    def handle(
        self, input: RegisterUserInputDto
    ) -> OperationResult[RegisterUserViewModel]:
        request_dto = RegisterUserRequestDto(
            name=input.name, email=input.email, password=input.password
        )

        result = self.register_user_use_case.execute(request_dto)

        if result.is_success:
            user_response = result.value
            user_view_model = self.presenter.present_success(user_response)
            return OperationResult.succeed(user_view_model)
        else:
            error_vm = self.presenter.present_error(
                result.error.message, result.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
