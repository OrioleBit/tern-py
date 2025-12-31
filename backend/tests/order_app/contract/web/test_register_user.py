from unittest.mock import Mock
from uuid import UUID

import pytest
from fastapi import status
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.controllers.user.register_user import RegisterUserInputDto
from order_app.interface.view_models.user_vm import (
    RegisterUserViewModel,
    TokensViewModel,
    UserViewModel,
)


@pytest.mark.parametrize(
    "payload, expected_status, expected_loc, expected_msg_substring",
    [
        (
            {"email": "email", "password": "password", "name": "name"},
            422,
            ["body", "email"],
            "must have an @-sign",
        ),
        (
            {"email": "test@email.com", "password": "password"},
            422,
            ["body", "name"],
            "Field required",
        ),
    ],
    ids=[
        "invalid_email",
        "missing_name",
    ],
)
def test_register_user_invalid_data(
    test_client, payload, expected_status, expected_loc, expected_msg_substring
):
    response = test_client.post("/users/register", json=payload)
    assert response.status_code == expected_status

    detail = response.json()["detail"][0]
    assert detail["loc"] == expected_loc
    assert expected_msg_substring in detail["msg"]


def test_register_user_failure(test_client, composition_root_instance):
    payload = {"email": "test@example.com", "password": "password", "name": "Test User"}
    controller_input = RegisterUserInputDto(
        name="Test User", email="test@example.com", password="password"
    )
    composition_root_instance.register_controller.handle = Mock(
        return_value=OperationResult.fail(
            "User with this email already exists", "USER_ALREADY_EXISTS"
        )
    )
    response = test_client.post("/users/register", json=payload)
    composition_root_instance.register_controller.handle.assert_called_with(
        controller_input
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User with this email already exists"}


def test_register_user_success(test_client, composition_root_instance):
    payload = {"email": "test@example.com", "password": "password", "name": "Test User"}
    controller_input = RegisterUserInputDto(
        name="Test User", email="test@example.com", password="password"
    )
    success_vm = RegisterUserViewModel(
        user=UserViewModel(
            id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            name="Test User",
            email="test@example.com",
            role="customer",
        ),
        tokens=TokensViewModel(
            access_token="access_token", refresh_token="refresh_token"
        ),
    )
    composition_root_instance.register_controller.handle = Mock(
        return_value=OperationResult.succeed(success_vm)
    )

    response = test_client.post("/users/register", json=payload)

    composition_root_instance.register_controller.handle.assert_called_with(
        controller_input
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] == "access_token"
    assert response.cookies["refresh_token"] == "refresh_token"
    assert response.json() == {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "refresh_token": "refresh_token",
        "access_token": "access_token",
    }
