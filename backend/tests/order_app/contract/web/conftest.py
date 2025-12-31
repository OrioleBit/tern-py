from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.dependencies import get_composition_root
from order_app.infrastructure.web.fastapi.fastapi_app_factory import create_web_app
from order_app.interface.controllers.user.register_user import RegisterUserController
from order_app.interface.presenters.web.user import WebRegisterUserPresenter


@pytest.fixture
def composition_root(
    user_repository, refresh_token_repo, register_user_controller
) -> CompositionRoot:
    composition_root = CompositionRoot(
        order_repository=None,
        product_repository=None,
        user_repository=user_repository,
        refresh_token_repo=refresh_token_repo,
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
def composition_root_instance(test_client) -> CompositionRoot:
    return test_client.app.dependency_overrides[get_composition_root]()


@pytest.fixture
def register_user_presenter():
    class MockRegisterPresenter(WebRegisterUserPresenter):
        def present_success(self, user_response):
            """Mock implementation of present_success"""
            pass

        def present_error(self, message: str, code: int):
            """Mock implementation of present_error"""
            pass

    mock = MockRegisterPresenter()
    mock.present_success = Mock()
    mock.present_error = Mock()
    return mock


@pytest.fixture
def register_user_controller(register_user_use_case, register_user_presenter):
    class MockRegisterUserController(RegisterUserController):
        def __init__(self):
            self.handle = Mock()
            self.register_user_use_case = register_user_use_case
            self.presenter = register_user_presenter

    return MockRegisterUserController()
