from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from schemas.common import Message
from schemas.user import (
    UserIn,
    UserOut,
    UserUpdateIn,
)

router = Router()


@router.post("/users", response={201: UserOut, 409: Message})
def account_registration(request, data: UserIn):
    try:
        user = User(username=data.username, email=data.email)
        user.set_password(data.password)
        user.save()
    except IntegrityError:
        return 409, {"detail": "User already exists"}

    return 201, user


@router.get("/user", auth=JWTAuth(), response={200: UserOut, 401: Message})
def get_user(request):
    return UserOut.from_orm(request.user)


@router.put("/user", auth=JWTAuth(), response={200: UserOut, 401: Message})
def update_user(request, data: UserUpdateIn):
    user = request.user
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(user, attr, value)

    user.save()
    return 200, user
