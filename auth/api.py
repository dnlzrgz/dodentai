from ninja import Router
from ninja_jwt.authentication import JWTAuth
from auth.schemas import UserSchema

router = Router()


@router.get("/user", auth=JWTAuth(), response=UserSchema)
def get_current_user(request):
    return request.user
