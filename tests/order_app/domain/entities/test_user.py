from order_app.domain.entities.user import User, UserRole


def test_user_initial_roles():
    user = User.new(name="Test User", email="test@example.com")
    assert user.role == UserRole.CUSTOMER


def test_user_is_manager():
    user = User.new(
        name="Manager User", email="manager@example.com", role=UserRole.MANAGER
    )
    assert user.role == UserRole.MANAGER
    assert not user.role == UserRole.CUSTOMER
    assert user.is_customer is False
    assert user.is_manager is True


def test_update_user_role():
    user = User.new(name="Test User", email="test@example.com")
    assert user.role == UserRole.CUSTOMER
    user.update_role(UserRole.MANAGER)
    assert user.role == UserRole.MANAGER
    assert user.is_manager is True
    assert user.is_customer is False
