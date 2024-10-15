from datetime import date, datetime
from ninja import Schema

from social.models import Follow


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
    last_active_at: datetime

    @staticmethod
    def resolve_username(obj):
        return obj.user.username

    @staticmethod
    def resolve_followers_count(obj):
        return Follow.objects.filter(following=obj.user).count()

    @staticmethod
    def resolve_following_count(obj):
        return Follow.objects.filter(follower=obj.user).count()


class ProfileUpdateIn(BaseProfile):
    public_name: str | None = None  # type: ignore
    biography: str | None = None  # type: ignore
