from typing import Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from pydantic import ValidationError
from social.models import Follow

router = Router()


@router.post(
    "/{username}/follow",
    auth=JWTAuth(),
    response={
        200: Any,
        400: Any,
        403: Any,
        404: Any,
        409: Any,
    },
)
def follow(request, username: str):
    follower_user = request.user
    following_user = get_object_or_404(User, username=username)

    if following_user == follower_user:
        return 403, {"detail": "You cannot follow yourself"}

    try:
        follow_in_db = Follow.objects.get(
            follower=follower_user, following=following_user
        )
        follow_in_db.delete()
        return 200, {"detail": f"You have unfollowed {following_user.username}"}
    except Follow.DoesNotExist:
        Follow.objects.create(follower=follower_user, following=following_user)
        return 200, {"detail": f"You are now following {following_user.username}"}
    except ValidationError as e:
        return 400, {"detail": f"{e}"}
    except Exception as e:
        return 409, {"detail": f"An error occurred: {e}"}


@router.get(
    "/{username}/followers",
    auth=JWTAuth(),
    response={200: list[str], 403: Any, 404: Any},
)
def get_followers(request, username: str):
    user = get_object_or_404(User, username=username)

    followers = user.followers.select_related("follower").only("follower__username")
    return [follow.follower.username for follow in followers]


@router.get(
    "/{username}/following",
    auth=JWTAuth(),
    response={200: list[str], 403: Any, 404: Any},
)
def get_following(request, username: str):
    user = get_object_or_404(User, username=username)

    following = user.following.select_related("following").only("following__username")
    return [follow.following.username for follow in following]
