import datetime
from uuid import uuid4

from freezegun import freeze_time
from order_app.domain.entities.auth import RefreshToken


@freeze_time("2022-01-01")
def test_is_valid_is_revoked():
    refresh_token = RefreshToken.new(
        user_id=uuid4(),
        token="test_token",
        expires_at=int(datetime.datetime.now(datetime.timezone.utc).timestamp()) + 3600,
        is_revoked=True,
    )
    assert not refresh_token.is_valid()


@freeze_time("2022-01-01")
def test_is_valid_is_expired():
    refresh_token = RefreshToken.new(
        user_id=uuid4(),
        token="test_token",
        expires_at=int(datetime.datetime.now(datetime.timezone.utc).timestamp()) - 3600,
        is_revoked=False,
    )
    assert not refresh_token.is_valid()


@freeze_time("2022-01-01")
def test_is_valid_not_revoked_not_expired():
    refresh_token = RefreshToken.new(
        user_id=uuid4(),
        token="test_token",
        expires_at=int(datetime.datetime.now(datetime.timezone.utc).timestamp()) + 3600,
        is_revoked=False,
    )
    assert refresh_token.is_valid()
