from passlib.context import CryptContext

from order_app.application.ports.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self):
        super().__init__()
        self._context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, plain_password: str) -> str:
        return self._context.hash(plain_password)

    def verify(self, plain_password, hashed_password):
        return self._context.verify(plain_password, hashed_password)
