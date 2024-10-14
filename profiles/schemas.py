from datetime import date, datetime
from ninja import Schema


class BaseProfile(Schema):
    public_name: str
    biography: str
    birthday: date | None = None
    location: str | None = None


class ProfileIn(BaseProfile):
    pass


class ProfileOut(BaseProfile):
    username: str

    followers_count: int = 0
    following_count: int = 0

    joined_at: datetime
    last_active: datetime

    @staticmethod
    def resolve_username(obj):
        return obj.user.username


class ProfileUpdateIn(BaseProfile):
    public_name: str | None = None  # type: ignore
    biography: str | None = None  # type: ignore
