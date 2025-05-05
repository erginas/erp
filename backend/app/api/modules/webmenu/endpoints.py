from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.modules.webmenu.schemas import WebMenuRead
from app.api.modules.webmenu.crud import get_menus_by_role
from app.core.db import get_session

router = APIRouter(
    prefix="/menu",
    tags=["WebMenu"]
)

@router.get("/", response_model=List[WebMenuRead])
def list_menu(
    role: str = Query(..., description="Kullanıcının rolü"),  # ✅ Burada önemli
    session: Session = Depends(get_session),
):
    return get_menus_by_role(session=session, role=role)
