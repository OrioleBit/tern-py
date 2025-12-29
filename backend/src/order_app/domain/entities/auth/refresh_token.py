import datetime
from dataclasses import dataclass
from uuid import UUID

from order_app.domain.entities.entity import Entity


@dataclass
class RefreshToken(Entity):
    user_id: UUID
    token: str
    expires_at: int  # Unix timestamp
    is_revoked: bool = False

    def is_valid(self) -> bool:
        return not self.is_revoked and self.expires_at > int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        )
