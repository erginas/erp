# app/api/modules/webmenu/endpoints.py
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import SessionDep, get_db
from app.api.modules.webmenu import crud, schemas

router = APIRouter(
    prefix="/menu",
    tags=["WebMenu"],
    responses={404: {"description": "Menu not found"}},
)


@router.get("/", response_model=List[schemas.WebMenuRead])
def get_menus(
        role: str = Query(...),
        session: Session = Depends(get_db)
):
    return crud.get_menus_by_role(session=session, role=role)
