from typing import Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ninja import Router
from profiles.models import Profile
from profiles.schemas import ProfileOut

router = Router()


@router.get(
    "/{username}",
    response={200: ProfileOut, 404: Any},
)
def get_profile(request, username: str):
    # TODO: handle if user == request.user
    # TODO: handle if user not authenticated
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return ProfileOut.from_orm(profile)
