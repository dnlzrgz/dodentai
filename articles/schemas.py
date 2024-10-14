from datetime import datetime
from ninja import Schema
from pydantic import BaseModel, SerializeAsAny, field_validator
from profiles.models import Profile
from profiles.schemas import ProfileOut


class Empty(BaseModel):
    pass


class ArticleBase(Schema):
    title: str
    slug: str
    summary: str
    tags: list[str]
    meta_description: str
    content: str


class ArticleIn(ArticleBase):
    pass

    @field_validator("slug")
    def ensure_slug_is_lowercase(cls, value):
        return value.lower() if isinstance(value, str) else value


class ArticleOut(ArticleBase):
    user_profile: ProfileOut
    tags: SerializeAsAny[list[str]]
    created_at: datetime

    @staticmethod
    def resolve_user_profile(obj):
        user = obj.user
        return Profile.objects.get(user=user)

    @staticmethod
    def resolve_tags(obj):
        return (
            obj.tags if isinstance(obj.tags, list) else [t.name for t in obj.tags.all()]
        )


class ArticleUpdate(ArticleBase):
    title: str | None = None  # type: ignore
    slug: str | None = None  # type: ignore
    summary: str | None = None  # type: ignore
    tags: list[str] | None = None  # type: ignore
    meta_description: str | None = None  # type: ignore
    content: str | None = None  # type: ignore

    @field_validator("slug")
    def ensure_slug_is_lowercase(cls, value):
        return value.lower() if isinstance(value, str) else value
