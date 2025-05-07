from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.modules.personel.gorev.crud import create_personel_gorev, get_personel_gorev, get_personel_gorev_list, \
    update_personel_gorev, delete_personel_gorev
from app.api.modules.personel.schemas import PersonelGorevRead, PersonelGorevCreate, PersonelGorevUpdate

router = APIRouter(prefix="/personel-gorev", tags=["PersonelGorev"])


@router.post("/", response_model=PersonelGorevRead)
def create_personel_gorev_endpoint(personel_gorev: PersonelGorevCreate, db: Session = Depends(get_db)):
    return create_personel_gorev(db, personel_gorev)


@router.get("/{personel_gorev_id}", response_model=PersonelGorevRead)
def read_personel_gorev_endpoint(personel_gorev_id: int, db: Session = Depends(get_db)):
    db_personel_gorev = get_personel_gorev(db, personel_gorev_id)
    if db_personel_gorev is None:
        raise HTTPException(status_code=404, detail="PersonelGorev not found")
    return db_personel_gorev


@router.get("/", response_model=list[PersonelGorevRead])
def read_personel_gorev_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_gorev_list(db, skip, limit)


@router.put("/{personel_gorev_id}", response_model=PersonelGorevRead)
def update_personel_gorev_endpoint(personel_gorev_id: int, personel_gorev: PersonelGorevUpdate,
                                   db: Session = Depends(get_db)):
    db_personel_gorev = update_personel_gorev(db, personel_gorev_id, personel_gorev)
    if db_personel_gorev is None:
        raise HTTPException(status_code=404, detail="PersonelGorev not found")
    return db_personel_gorev


@router.delete("/{personel_gorev_id}")
def delete_personel_gorev_endpoint(personel_gorev_id: int, db: Session = Depends(get_db)):
    result = delete_personel_gorev(db, personel_gorev_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelGorev not found")
    return result
