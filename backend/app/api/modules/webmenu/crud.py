# app/api/modules/webmenu/crud.py
from typing import List

from sqlalchemy.orm import Session

from app.api.modules.webmenu.models import WebMenu


def get_menus_by_role(session: Session, role: str) -> List[WebMenu]:
    return session.query(WebMenu).filter(
        (WebMenu.roles == None) | (WebMenu.roles.ilike(f"%{role}%"))
    ).all()
