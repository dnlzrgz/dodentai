from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from accounts.api import router as accounts_router
from profiles.api import router as profiles_router

api = NinjaAPI()

api.add_router("/token/", router=obtain_pair_router, tags=["Auth"])
api.add_router("/", router=accounts_router, tags=["Auth"])
api.add_router("/profiles", router=profiles_router, tags=["Profile"])
