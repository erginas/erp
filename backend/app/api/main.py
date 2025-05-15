from fastapi import APIRouter

from app.api.modules.kisiler.dashboard.enpoints import router as kisiler_dashboard_router
from app.api.modules.kisiler.endpoints import router as kisiler_router
from app.api.modules.kisiler.izin.izin_dashboard import router as kisi_izin_router
# personel routers
# from app.api.modules.personel.dashboard_endpoints import router as personel_dashboard_router
# from app.api.modules.personel.endpoints import router as personel_router
# from app.api.modules.personel.izin.endpoints import router as personel_izin_router
# users
from app.api.modules.users.endpoints import router as user_router
from app.api.modules.webmenu.endpoints import router as webmenu_endpoints
from app.api.routes import login, private, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(user_router)

api_router.include_router(webmenu_endpoints)
api_router.include_router(utils.router)

# api_router.include_router(personel_dashboard_router)
# api_router.include_router(personel_router)
# api_router.include_router(personel_izin_router)

api_router.include_router(kisiler_router)
api_router.include_router(kisiler_dashboard_router)
api_router.include_router(kisi_izin_router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
