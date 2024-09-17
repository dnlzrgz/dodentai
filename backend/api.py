from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from auth.api import router as auth_router

api = NinjaAPI()

api.add_router("/token/", router=obtain_pair_router, tags=["Auth"])
api.add_router("/auth/", auth_router, tags=["Auth"])
