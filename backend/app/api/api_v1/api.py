from fastapi import APIRouter

from app.api.modules.kisiler import endpoints as kisiler_endpoints
from app.api.modules.users import endpoints as users_endpoints
from app.api.routes import login
from app.api.routes import private
from app.api.routes import utils

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(private.router, prefix="/private", tags=["private"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(users_endpoints.router, prefix="/users", tags=["users"])
api_router.include_router(kisiler_endpoints.router, prefix="/kisiler", tags=["kisiler"])
