from ninja import NinjaAPI
from ninja_jwt.routers.obtain import obtain_pair_router
from accounts.api import router as accounts_router

api = NinjaAPI()

api.add_router("/token/", router=obtain_pair_router, tags=["Auth"])
api.add_router("/", router=accounts_router, tags=["Auth"])
