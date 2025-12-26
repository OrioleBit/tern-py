from order_app.domain.entities.user import UserRole


def test_user_initial_roles(user_customer):
    assert user_customer.role == UserRole.CUSTOMER
    assert user_customer.is_customer is True
    assert user_customer.is_manager is False
    assert user_customer.is_admin is False


def test_user_is_customer(user_customer):
    assert user_customer.role == UserRole.CUSTOMER
    assert user_customer.is_customer is True
    assert user_customer.is_manager is False
    assert user_customer.is_admin is False


def test_user_is_manager(user_manager):
    assert user_manager.role == UserRole.MANAGER
    assert user_manager.is_customer is False
    assert user_manager.is_manager is True
    assert user_manager.is_admin is False


def test_user_is_admin(user_admin):
    assert user_admin.role == UserRole.ADMIN
    assert user_admin.is_customer is False
    assert user_admin.is_manager is False
    assert user_admin.is_admin is True


def test_update_user_role(user_customer):
    assert user_customer.role == UserRole.CUSTOMER
    user_customer.update_role(UserRole.MANAGER)
    assert user_customer.role == UserRole.MANAGER

    user_customer.update_role(UserRole.ADMIN)
    assert user_customer.role == UserRole.ADMIN
