from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.db import get_session  # assuming this is the correct path to get_session
from . import crud
from .models import HRPersonel

router = APIRouter(prefix="/hr/personel", tags=["İnsan Kaynakları"])


@router.get("/", response_model=list[HRPersonel])
def read_all(db: Session = Depends(get_session)):
    return crud.get_all(db)


@router.get("/{id}", response_model=HRPersonel)
def read_one(id: int, db: Session = Depends(get_session)):
    personel = crud.get_by_id(db, id)
    if not personel:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    return personel


@router.post("/", response_model=HRPersonel)
def create(personel: HRPersonel, db: Session = Depends(get_session)):
    return crud.create(db, personel)


@router.put("/{id}", response_model=HRPersonel)
def update(id: int, personel: HRPersonel, db: Session = Depends(get_session)):
    return crud.update(db, id, personel)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_session)):
    crud.delete(db, id)
    return {"ok": True}
