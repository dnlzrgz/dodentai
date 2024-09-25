from typing import Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from profiles.models import Profile
from profiles.schemas import ProfileOut, ProfileUpdateIn

router = Router()


@router.get("/{username}", response={200: ProfileOut, 404: Any})
def get_profile(request, username: str):
    # TODO: handle if user == request.user
    # TODO: handle if user not authenticated
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    return profile


@router.put("/", auth=JWTAuth(), response={200: ProfileOut, 401: Any})
def update_user_profile(request, data: ProfileUpdateIn):
    profile = get_object_or_404(Profile, user=request.user)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(profile, attr, value)

    profile.save()
    return 200, profile
