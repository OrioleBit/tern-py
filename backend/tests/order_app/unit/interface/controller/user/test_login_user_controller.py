from unittest.mock import MagicMock

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.login import (
    LoginUserRequestDto,
    LoginUserResponseDto,
)
from order_app.interface.controllers.user.login_user import (
    LoginUserController,
    LoginUserInputDto,
)
from order_app.interface.presenters.base.user import LoginPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel


def test_login_user_failure(login_user_use_case):
    login_user_use_case.execute.return_value = Result.failure(
        Error(code="code", message="error")
    )
    mock_presenter = MagicMock(spec=LoginPresenter)
    mock_presenter.present_error.return_value = ErrorViewModel("errordata", "codedata")
    login_controller = LoginUserController(
        login_user_use_case=login_user_use_case,
        presenter=mock_presenter,
    )

    operation_result = login_controller.handle(
        LoginUserInputDto(email="test@email.com", password="password")
    )

    login_user_use_case.execute.assert_called_once_with(
        LoginUserRequestDto(email="test@email.com", password="password")
    )
    mock_presenter.present_error.assert_called_once_with("error", "code")
    mock_presenter.present_success.assert_not_called()
    assert not operation_result.is_success
    assert operation_result.error.message == "errordata"
    assert operation_result.error.code == "codedata"


def test_login_user_success(login_user_use_case):
    use_case_response = LoginUserResponseDto(
        id="user_id",
        name="Name",
        email="test@email.com",
        role="user",
        access_token="access_token",
        expires_in=3600,
    )
    login_user_use_case.execute.return_value = Result.success(use_case_response)
    mock_presenter = MagicMock(spec=LoginPresenter)
    expected_view_model = MagicMock()
    mock_presenter.present_success.return_value = expected_view_model

    login_controller = LoginUserController(
        login_user_use_case=login_user_use_case,
        presenter=mock_presenter,
    )

    operation_result = login_controller.handle(
        LoginUserInputDto(email="test@email.com", password="password")
    )

    login_user_use_case.execute.assert_called_once_with(
        LoginUserRequestDto(email="test@email.com", password="password")
    )
    mock_presenter.present_success.assert_called_once_with(use_case_response)
    mock_presenter.present_error.assert_not_called()
    assert operation_result.is_success
    assert operation_result.success == expected_view_model
