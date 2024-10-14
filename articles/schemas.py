from datetime import datetime
from ninja import Schema
from pydantic import BaseModel, SerializeAsAny
from profiles.models import Profile
from profiles.schemas import ProfileOut


class Empty(BaseModel):
    pass


class ArticleIn(Schema):
    title: str
    slug: str
    summary: str
    tags: list[str]

    content: str

    meta_description: str


class ArticleOut(Schema):
    user_profile: ProfileOut

    title: str
    slug: str
    summary: str
    tags: SerializeAsAny[list[str]]

    content: str

    meta_description: str

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
