from ninja import Schema
from pydantic import EmailStr


class UserIn(Schema):
    email: EmailStr
    username: str
    password: str


class UserOut(Schema):
    email: EmailStr
    username: str


class UserUpdateIn(Schema):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserLogin(UserIn):
    email: str | None = None  # type: ignore


class Token(Schema):
    token: str


class Message(Schema):
    message: str
