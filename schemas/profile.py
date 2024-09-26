from datetime import date, datetime
from ninja import Schema
from schemas.user import UserDetails


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
