import pytest
from fastapi.testclient import TestClient

from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.fastapi.fastapi_app_factory import create_web_app


@pytest.fixture
def composition_root():
    return CompositionRoot(
        order_repository=None,
        product_repository=None,
        user_repository=None,
        order_presenter=None,
        user_presenter=None,
        password_hasher=None,
    )


@pytest.fixture
def client(composition_root):
    app = create_web_app(testing=True)
    return TestClient(app)


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
    client, payload, expected_status, expected_loc, expected_msg_substring
):
    response = client.post("/users/register", json=payload)
    assert response.status_code == expected_status

    detail = response.json()["detail"][0]
    assert detail["loc"] == expected_loc
    assert expected_msg_substring in detail["msg"]
