from datetime import date, datetime
from ninja import Schema


class UserDetails(Schema):
    username: str
    email: str


class BaseProfile(Schema):
    public_name: str
    biography: str
    birthday: date | None = None
    location: str | None = None


class ProfileIn(BaseProfile):
    pass


class ProfileOut(BaseProfile):
    user: UserDetails
    joined_at: datetime
    last_active: datetime


class ProfileUpdateIn(BaseProfile):
    public_name: str | None = None  # type: ignore
    biography: str | None = None  # type: ignore
