from unittest.mock import MagicMock

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.register import RegisterUserRequestDto
from order_app.interface.controllers.user.register_user import (
    RegisterUserController,
    RegisterUserInputDto,
)
from order_app.interface.presenters.base.user import RegisterPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel


def test_register_user_handler_failure(register_user_use_case):
    register_user_use_case.execute.return_value = Result.failure(Error("error", "code"))
    mock_presenter = MagicMock(spec=RegisterPresenter)
    mock_presenter.present_error.return_value = ErrorViewModel("errordata", "codedata")

    user_controller = RegisterUserController(
        register_user_use_case=register_user_use_case,
        presenter=mock_presenter,
    )
    request_data = RegisterUserInputDto(
        name="name",
        email="email",
        password="password",
    )

    operation_result = user_controller.handle(input=request_data)

    register_user_use_case.execute.assert_called_once_with(
        RegisterUserRequestDto(name="name", email="email", password="password")
    )
    mock_presenter.present_error.assert_called_once_with("code", "error")
    assert not operation_result.is_success
    assert operation_result.error.message == "errordata"
    assert operation_result.error.code == "codedata"


def test_register_user_handler_success(register_user_use_case):
    user_response = MagicMock()
    register_user_use_case.execute.return_value = Result.success(user_response)
    mock_presenter = MagicMock(spec=RegisterPresenter)
    user_view_model = MagicMock()
    mock_presenter.present_success.return_value = user_view_model

    user_controller = RegisterUserController(
        register_user_use_case=register_user_use_case,
        presenter=mock_presenter,
    )
    request_data = RegisterUserInputDto(
        name="name",
        email="email",
        password="password",
    )

    operation_result = user_controller.handle(input=request_data)

    register_user_use_case.execute.assert_called_once_with(
        RegisterUserRequestDto(name="name", email="email", password="password")
    )
    mock_presenter.present_success.assert_called_once_with(user_response)
    assert operation_result.is_success
    assert operation_result.success == user_view_model
