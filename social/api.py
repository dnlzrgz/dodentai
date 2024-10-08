from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from pydantic import ValidationError
from schemas.common import Message
from schemas.social import Count
from schemas.user import UserDetails
from social.models import Follow

router = Router()


@router.post(
    "/{username}/follow",
    auth=JWTAuth(),
    response={
        200: Message,
        400: Message,
        403: Message,
        404: Message,
        409: Message,
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
    response={200: list[UserDetails], 403: Message, 404: Message},
)
def get_followers(request, username: str):
    user = get_object_or_404(User, username=username)

    followers = user.followers.select_related("follower").only("follower__username")
    return [UserDetails.from_orm(follow.follower) for follow in followers]


@router.get(
    "/{username}/followers/count",
    auth=JWTAuth(),
    response={200: Count, 403: Message, 404: Message},
)
def get_followers_count(request, username: str):
    user = get_object_or_404(User, username=username)
    follower_count = user.followers.count()
    return 200, {"count": follower_count}


@router.get(
    "/{username}/following",
    auth=JWTAuth(),
    response={200: list[UserDetails], 403: Message, 404: Message},
)
def get_following(request, username: str):
    user = get_object_or_404(User, username=username)

    following = user.following.select_related("following").only("following__username")
    return [UserDetails.from_orm(follow.following) for follow in following]


@router.get(
    "/{username}/following/count",
    auth=JWTAuth(),
    response={200: Count, 403: Message, 404: Message},
)
def get_following_count(request, username: str):
    user = get_object_or_404(User, username=username)
    following_count = user.following.count()
    return 200, {"count": following_count}
