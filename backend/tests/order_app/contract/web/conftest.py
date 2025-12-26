from unittest.mock import Mock

import pytest

from order_app.interface.controllers.user.register_user import RegisterUserController
from order_app.interface.presenters.web.user import WebRegisterUserPresenter


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
