from typing import Any
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from articles.models import Article
from articles.schemas import Empty, ArticleIn, ArticleOut

router = Router()


@router.post("/", auth=JWTAuth(), response={201: ArticleOut, 409: Any, 422: Any})
def create_article(request, data: ArticleIn):
    try:
        article = Article.objects.create(
            **{k: v for k, v in data.dict().items() if k != "tags"},
            user=request.user,
        )
    except IntegrityError as err:
        return 409, {"detail": err}

    if data.tags != Empty:
        for tag_name in data.tags:
            article.tags.add(tag_name)

        article.save()

    return 201, article


@router.get("/{slug}", response={200: ArticleOut, 404: Any})
def get_article(request, slug: str):
    article = get_object_or_404(Article, slug=slug)
    return article
