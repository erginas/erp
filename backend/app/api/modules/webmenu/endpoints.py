# app/api/modules/webmenu/endpoints.py
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import SessionDep
from app.api.modules.webmenu import crud
from app.api.modules.webmenu.models import WebMenu
from app.api.modules.webmenu.schemas import WebMenuRead

router = APIRouter(
    prefix="/menu",
    tags=["WebMenu"],
    responses={404: {"description": "Menu not found"}},
)


@router.get("/", response_model=List[WebMenuRead])
def get_menu_list(role: str = Query(...), session: Session = Depends(SessionDep)) -> List[WebMenu]:
    """
    Belirli role sahip kullanıcılara göre menü listesini döner.
    """
    menus = crud.get_menus_by_role(session=session, role=role)
    return menus
