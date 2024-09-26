from ninja import Schema
from pydantic import EmailStr


class BaseUser(Schema):
    email: EmailStr
    username: str
    password: str


class UserDetails(Schema):
    username: str


class UserIn(BaseUser):
    pass


class UserOut(Schema):
    email: EmailStr
    username: str


class UserUpdateIn(BaseUser):
    email: EmailStr | None = None  # type: ignore
    username: str | None = None  # type: ignore
    password: str | None = None  # type: ignore


class UserLogin(BaseUser):
    email: str | None = None  # type: ignore
