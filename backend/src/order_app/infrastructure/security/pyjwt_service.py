import datetime
from dataclasses import dataclass

import jwt
from order_app.application.ports.auth_token_service import AuthTokenService
from order_app.domain.exceptions.token_errors import (
    InvalidTokenError,
    TokenExpiredError,
)


@dataclass
class PyJWTService(AuthTokenService):
    secret_key: str
    algorithm: str = "HS256"

    def generate_token(self, payload: dict, expires_in: int = None) -> str:
        payload_copy = payload.copy()
        now = datetime.datetime.now(datetime.timezone.utc)
        payload_copy["iat"] = now
        payload_copy["exp"] = now + datetime.timedelta(seconds=expires_in)
        token = jwt.encode(payload_copy, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> dict:
        try:
            decoded_payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
