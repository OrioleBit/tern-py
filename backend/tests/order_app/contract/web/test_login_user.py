from unittest.mock import Mock
from uuid import UUID

import pytest
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.controllers.user.login_user import LoginUserInputDto
from order_app.interface.view_models.user_vm import LoginUserViewModel, UserViewModel
from starlette import status


@pytest.mark.parametrize(
    "payload, expected_status, expected_loc, expected_msg_substring",
    [
        (
            {"email": "email", "password": "password"},
            422,
            ["body", "email"],
            "must have an @-sign",
        ),
        (
            {"email": "test@email.com"},
            422,
            ["body", "password"],
            "Field required",
        ),
        (
            {"password": "password"},
            422,
            ["body", "email"],
            "Field required",
        ),
        (
            {"email": "test@email.com", "password": ""},
            422,
            ["body", "password"],
            "String should have at least 8 characters",
        ),
    ],
    ids=[
        "invalid_email",
        "missing_password",
        "missing_email",
        "min_length_password",
    ],
)
def test_login_user_invalid_data(
    test_client, payload, expected_status, expected_loc, expected_msg_substring
):
    response = test_client.post("/users/login", json=payload)
    assert response.status_code == expected_status

    detail = response.json()["detail"][0]
    assert detail["loc"] == expected_loc
    assert expected_msg_substring in detail["msg"]


def test_register_user_failure(test_client, composition_root_instance):
    payload = {"email": "test@example.com", "password": "password", "name": "Test User"}
    controller_input = LoginUserInputDto(email="test@example.com", password="password")
    composition_root_instance.login_controller.handle = Mock(
        return_value=OperationResult.fail("Invalid credentials", "INVALID_CREDENTIALS")
    )
    response = test_client.post("/users/login", json=payload)
    composition_root_instance.login_controller.handle.assert_called_with(
        controller_input
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Invalid credentials"}


def test_register_user_success(test_client, composition_root_instance):
    payload = {"email": "test@example.com", "password": "password", "name": "Test User"}
    controller_input = LoginUserInputDto(email="test@example.com", password="password")
    success_vm = LoginUserViewModel(
        user=UserViewModel(
            id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            name="Test User",
            email="test@example.com",
            role="customer",
        ),
        access_token="access_token",
        refresh_token="refresh_token",
    )
    composition_root_instance.login_controller.handle = Mock(
        return_value=OperationResult.succeed(success_vm)
    )

    response = test_client.post("/users/login", json=payload)

    composition_root_instance.login_controller.handle.assert_called_with(
        controller_input
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies["access_token"] == "access_token"
    assert response.cookies["refresh_token"] == "refresh_token"
    assert response.json() == {
        "refresh_token": "refresh_token",
        "access_token": "access_token",
    }
