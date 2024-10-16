from typing import Any
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import PageNumberPagination, paginate
from ninja_jwt.authentication import JWTAuth
from articles.models import Article
from articles.schemas import Empty, ArticleIn, ArticleOut, ArticleUpdate

router = Router()


@router.post(
    "/",
    auth=JWTAuth(),
    response={
        201: ArticleOut,
        409: Any,
        422: Any,
    },
)
def create_article(request, data: ArticleIn):
    if Article.objects.filter(slug=data.slug).exists():
        return 409, {"detail": "This slug already exists."}

    try:
        article = Article.objects.create(
            **{k: v for k, v in data.dict().items() if k != "tags"},
            user=request.user,
        )
    except IntegrityError as err:
        return 422, {"detail": f"{err}"}

    if data.tags != Empty:
        for tag_name in data.tags:
            article.tags.add(tag_name)

        article.save()

    return 201, article


@router.get("/{slug}", response={200: ArticleOut, 404: Any})
def get_article(request, slug: str):
    return get_object_or_404(Article, slug=slug)


@router.get("/", response={200: list[ArticleOut]})
@paginate(PageNumberPagination, page_size=10)
def list_articles(request):
    # TODO: sort by publication date
    return Article.objects.all()


@router.put("/{slug}", auth=JWTAuth(), response={200: ArticleOut, 401: Any, 404: Any})
def update_article(request, slug: str, data: ArticleUpdate):
    article = get_object_or_404(Article, slug=slug)
    if request.user != article.user:
        return 403, None

    updated_fields = []
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(article, attr, value)
        updated_fields.extend(["title", "slug"] if attr == "title" else [attr])

    article.save(update_fields=updated_fields)

    return 200, article


@router.delete(
    "/{slug}", auth=JWTAuth(), response={204: Any, 401: Any, 403: Any, 404: Any}
)
def delete_article(request, slug: str):
    article = get_object_or_404(Article, slug=slug)
    if request.user != article.user:
        return 403, None

    article.delete()
    return 204, None
