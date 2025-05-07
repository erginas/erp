from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.modules.personel.crud import create_personel, get_personel, get_personel_list, update_personel, \
    delete_personel
from app.api.modules.personel.schemas import PersonelRead, PersonelCreate, PersonelUpdate

router = APIRouter(prefix="/personel", tags=["Personel"])


@router.get("/", response_model=list[PersonelRead])
def read_personel_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_list(db, skip, limit)


@router.post("/", response_model=PersonelRead)
def create_personel_endpoint(personel: PersonelCreate, db: Session = Depends(get_db)):
    return create_personel(db, personel)


@router.get("/{personel_id}", response_model=PersonelRead)
def read_personel_endpoint(personel_id: int, db: Session = Depends(get_db)):
    db_personel = get_personel(db, personel_id)
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel not found")
    return db_personel


@router.put("/{personel_id}", response_model=PersonelRead)
def update_personel_endpoint(personel_id: int, personel: PersonelUpdate, db: Session = Depends(get_db)):
    db_personel = update_personel(db, personel_id, personel)
    if db_personel is None:
        raise HTTPException(status_code=404, detail="Personel not found")
    return db_personel


@router.delete("/{personel_id}")
def delete_personel_endpoint(personel_id: int, db: Session = Depends(get_db)):
    result = delete_personel(db, personel_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Personel not found")
    return result
