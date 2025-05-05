# app/api/modules/webmenu/schemas.py
from typing import Optional, List

from sqlmodel import SQLModel


class WebMenuBase(SQLModel):
    label: str
    to_path: str
    module_key: Optional[str] = None
    parent_id: Optional[int] = None
    icon_name: Optional[str] = None
    roles: Optional[str] = None


class WebMenuCreate(WebMenuBase):
    pass


class WebMenuRead(WebMenuBase):
    id: int
    # children: Optional[List["WebMenuRead"]] = []

    class Config:
        orm_mode = True


WebMenuRead.update_forward_refs()
