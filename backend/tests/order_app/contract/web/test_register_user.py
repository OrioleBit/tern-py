from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.dependencies import get_composition_root
from order_app.infrastructure.web.fastapi.fastapi_app_factory import create_web_app
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.controllers.user.register_user import RegisterUserInputDto
from order_app.interface.view_models.user_vm import RegisterUserViewModel


@pytest.fixture
def composition_root(user_repository, register_user_controller) -> CompositionRoot:
    composition_root = CompositionRoot(
        order_repository=None,
        product_repository=None,
        user_repository=user_repository,
        order_presenter=None,
        register_presenter=None,
        login_presenter=None,
        password_hasher=None,
    )
    composition_root.register_controller = register_user_controller

    return composition_root


@pytest.fixture
def test_client(composition_root) -> TestClient:
    app = create_web_app(testing=True)
    app.dependency_overrides[get_composition_root] = lambda: composition_root
    return TestClient(app)


@pytest.fixture
def composition_root_instance(test_client):
    return test_client.app.dependency_overrides[get_composition_root]()


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


def test_register_user_success(test_client, composition_root_instance):
    payload = {"email": "test@example.com", "password": "password", "name": "Test User"}
    controller_input = RegisterUserInputDto(
        name="Test User", email="test@example.com", password="password"
    )
    success_vm = RegisterUserViewModel(
        id="123e4567-e89b-12d3-a456-426614174000",
        name="Test User",
        email="test@example.com",
        role="customer",
    )
    composition_root_instance.register_controller.handle = Mock(
        return_value=OperationResult.succeed(success_vm)
    )

    response = test_client.post("/users/register", json=payload)

    composition_root_instance.register_controller.handle.assert_called_with(
        controller_input
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": "123e4567-e89b-12d3-a456-426614174000"}


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
