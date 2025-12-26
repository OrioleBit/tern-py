import pytest

from order_app.domain.exceptions import InvalidUserRoleError
from order_app.domain.value_objects.user_role import UserRole


@pytest.mark.parametrize(
    "input_role, expected",
    [
        ("MANAGER", UserRole.MANAGER),
        ("manager", UserRole.MANAGER),
        ("CUSTOMER", UserRole.CUSTOMER),
        ("customer", UserRole.CUSTOMER),
        ("Admin", UserRole.ADMIN),
        ("admin", UserRole.ADMIN),
    ],
)
def test_from_str_valid_roles(input_role, expected):
    assert UserRole.from_str(input_role) == expected


@pytest.mark.parametrize(
    "input_role",
    ["", "unknown", "123", None],
)
def test_from_str_invalid_roles(input_role):
    with pytest.raises(InvalidUserRoleError, match=f"Invalid user role: {input_role}"):
        UserRole.from_str(input_role)
