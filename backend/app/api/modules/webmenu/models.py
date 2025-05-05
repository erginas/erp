# app/api/modules/webmenu/models.py
from typing import Optional

from sqlmodel import Field, SQLModel


class WebMenu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(max_length=100)
    to_path: str = Field(max_length=200)
    module_key: Optional[str] = Field(default=None, max_length=50)
    parent_id: Optional[int] = Field(default=None, foreign_key="web_menu.id")
    icon_name: Optional[str] = Field(default=None, max_length=50)
    roles: Optional[str] = Field(default=None, max_length=200)  # CSV format
