from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from accounts.api import router as accounts_router
from profiles.api import router as profiles_router
from social.api import router as social_router

api = NinjaAPI()

api.add_router("/token/", router=obtain_pair_router, tags=["Auth"])
api.add_router("/", router=accounts_router, tags=["Auth"])
api.add_router("/profile/", router=profiles_router, tags=["Profile"])
api.add_router("/profile/", router=social_router, tags=["Profile", "Social"])
