from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from ninja import Router
from ninja_jwt.tokens import AccessToken
from ninja_jwt.authentication import JWTAuth
from accounts.schemas import (
    UserIn,
    UserLogin,
    UserOut,
    UserUpdateIn,
    Message,
    Token,
)

router = Router()


@router.post("/users", response={201: UserOut, 409: Message})
def account_registration(request, data: UserIn):
    try:
        user = User(username=data.username, email=data.email)
        user.set_password(data.password)
        user.save()
    except IntegrityError:
        return 409, {"message": "User already exists"}

    return 201, user


@router.post("/users/login", response={200: Token, 401: Message})
def account_login(request, data: UserLogin):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return 401, {"message": "Incorrect credentials"}

    jwt_token = AccessToken.for_user(user)
    return 200, {"token": str(jwt_token)}


@router.get("/user", auth=JWTAuth(), response={200: UserOut, 401: Message})
def get_user(request):
    return UserOut.from_orm(request.user)


@router.put("/user", auth=JWTAuth(), response={200: UserOut, 401: Message})
def update_user(request, data: UserUpdateIn):
    current_user = request.user

    if data.username:
        current_user.username = data.username
    if data.email:
        current_user.email = data.email
    if data.password:
        current_user.password = data.password

    current_user.save()

    return 200, current_user
