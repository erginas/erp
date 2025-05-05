from typing import Optional, List

from pydantic import Field
from sqlmodel import Relationship, SQLModel


class WebMenu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # ✅ MUTLAKA OLMALI
    label: str = Field(max_length=100)
    to_path: str = Field(max_length=200)
    module_key: Optional[str] = Field(default=None, max_length=50)
    parent_id: Optional[int] = Field(default=None, foreign_key="web_menu.id")
    icon_name: Optional[str] = Field(default=None, max_length=50)
    roles: Optional[str] = Field(default=None, max_length=200)

    # 👇 Yeni alan: recursive ilişki
    children: List["WebMenu"] = Relationship(back_populates="parent")

    # 👇 opsiyonel: eğer ters ilişki de istenirse
    parent: Optional["WebMenu"] = Relationship(back_populates="children")
