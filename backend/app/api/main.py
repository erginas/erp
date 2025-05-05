from fastapi import APIRouter

from app.api.modules.kisiler.endpoints import router as kisiler_router
from app.api.modules.users.endpoints import router as user_router
from app.api.modules.webmenu import endpoints as webmenu_endpoints
from app.api.routes import login, private, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(user_router)

api_router.include_router(webmenu_endpoints.router)
api_router.include_router(utils.router)

api_router.include_router(kisiler_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
