from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from typing import Optional, Annotated

from app.api.deps import get_db
from app.api.modules.personel.crud import create_personel, get_personel, get_personel_list, update_personel, \
    delete_personel
from app.api.modules.personel.schemas import PersonelRead, PersonelCreate, PersonelUpdate
from app.api.modules.personel.crud import get_filtered_personel_list

router = APIRouter(prefix="/personel", tags=["Personel"])


@router.get("/", response_model=dict)
def read_filtered_personel_list(
    page: int = Query(0),
    size: int = Query(20),
    search: Optional[str] = Query(None),
    durum: Optional[str] = Query(None),
    sortBy: Optional[str] = Query(None),
    sortOrder: Optional[str] = Query("asc"),
    birim_id: Optional[int] = Query(None),
    unvan_id: Optional[int] = Query(None),
    brans_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {}
    if birim_id is not None:
        filters["birim_id"] = birim_id
    if unvan_id is not None:
        filters["unvan_id"] = unvan_id
    if brans_id is not None:
        filters["brans_id"] = brans_id

    return get_filtered_personel_list(
        db=db,
        page=page,
        size=size,
        search=search,
        durum=durum,
        sort_by=sortBy,
        sort_order=sortOrder,
        filters=filters
    )


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
