# app/api/modules/webmenu/crud.py
from typing import List

from sqlmodel import Session, select

from app.api.modules.webmenu.models import WebMenu


def get_menus_by_role(*, session: Session, role: str) -> List[WebMenu]:
    statement = select(WebMenu).where(
        (WebMenu.roles == None) | (WebMenu.roles.contains(role))
    )
    result = session.exec(statement).all()
    return result
