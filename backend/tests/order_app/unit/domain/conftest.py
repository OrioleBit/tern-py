import pytest

from order_app.domain.entities.user import User
from order_app.domain.value_objects.user_role import UserRole


@pytest.fixture
def user_customer():
    return User.new(
        name="Test User", password_hash="password", email="test@example.com"
    )


@pytest.fixture
def user_manager():
    return User.new(
        name="Test User",
        password_hash="password",
        email="test@example.com",
        role=UserRole.MANAGER,
    )


@pytest.fixture
def user_admin():
    return User.new(
        name="Test User",
        password_hash="password",
        email="test@example.com",
        role=UserRole.ADMIN,
    )
