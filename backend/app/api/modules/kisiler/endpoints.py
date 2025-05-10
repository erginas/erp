# routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session
from . import schemas, crud
from .crud import get_paginated_kisiler
from .models import Kisi
from .schemas import KisiFilter, Pagination

router = APIRouter(prefix="/kisi", tags=["Kisi"])


@router.post("/", response_model=schemas.KisiRead)
def create_kisi_endpoint(kisi: schemas.KisiCreate, session: Session = Depends(get_session)):
    return crud.create_kisi(session=session, kisi=kisi)


@router.get("/{kimlik_no}", response_model=schemas.KisiRead)
def read_kisi(kimlik_no: int, session: Session = Depends(get_session)):
    db_kisi = crud.get_kisi(session=session, kimlik_no=kimlik_no)
    if not db_kisi:
        raise HTTPException(status_code=404, detail="Kişi bulunamadı")
    return db_kisi


@router.get("/", response_model=Pagination[Kisi])
def read_kisiler(
        filters: KisiFilter = Depends(),
        page: int = 1,
        size: int = 100,
        session: Session = Depends(get_session)
):
    return get_paginated_kisiler(session=session, filters=filters, page=page, size=size)


@router.put("/{kimlik_no}", response_model=schemas.KisiRead)
def update_kisi_endpoint(kimlik_no: int, kisi: schemas.KisiUpdate, session: Session = Depends(get_session)):
    updated_kisi = crud.update_kisi(session=session, kimlik_no=kimlik_no, kisi=kisi)
    if not updated_kisi:
        raise HTTPException(status_code=404, detail="Kişi bulunamadı")
    return updated_kisi


@router.delete("/{kimlik_no}")
def delete_kisi_endpoint(kimlik_no: int, session: Session = Depends(get_session)):
    result = crud.delete_kisi(session=session, kimlik_no=kimlik_no)
    if not result:
        raise HTTPException(status_code=404, detail="Kişi bulunamadı")
    return result
