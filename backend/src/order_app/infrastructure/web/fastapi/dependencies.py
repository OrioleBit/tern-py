from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.persistence.sqlite.db import get_connection
from order_app.infrastructure.persistence.sqlite.user_repository import (
    SqliteUserRepository,
)
from order_app.infrastructure.security.argon2_hasher import Argon2PasswordHasher
from order_app.interface.presenters.web.user import (
    WebLoginUserPresenter,
    WebRegisterUserPresenter,
)


def get_composition_root() -> CompositionRoot:
    return CompositionRoot(
        order_repository=None,
        product_repository=None,
        user_repository=SqliteUserRepository(connection=get_connection()),
        password_hasher=Argon2PasswordHasher(),
        register_presenter=WebRegisterUserPresenter(),
        login_presenter=WebLoginUserPresenter(),
        order_presenter=None,
    )
