from datetime import datetime
from ninja import Schema
from pydantic import BaseModel, SerializeAsAny


class Empty(BaseModel):
    pass


class ArticleIn(Schema):
    title: str
    slug: str
    summary: str
    tags: list[str]

    content: str

    meta_description: str
    meta_keywords: str


class ArticleOut(Schema):
    # username: str | None = None
    # public_name: str | None = None

    title: str
    slug: str
    summary: str
    tags: SerializeAsAny[list[str]]

    content: str

    meta_description: str
    meta_keywords: str

    created_at: datetime

    @staticmethod
    def resolve_tags(obj):
        return (
            obj.tags if isinstance(obj.tags, list) else [t.name for t in obj.tags.all()]
        )
