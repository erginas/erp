from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from crud import (
    create_organizasyon_birimi,
    get_organizasyon_birimleri,
    get_organizasyon_birimi,
    update_organizasyon_birimi,
    delete_organizasyon_birimi,
)
from schemas import (
    OrganizasyonBirimiCreate,
    OrganizasyonBirimiUpdate,
    OrganizasyonBirimiRead,
)

router = APIRouter()


# Create
@router.post("/organizasyon-birimleri/", response_model=OrganizasyonBirimiRead)
def create_organizasyon_birimi_endpoint(
        organizasyon_birimi: OrganizasyonBirimiCreate, db: Session = Depends(get_db)
):
    return create_organizasyon_birimi(db, organizasyon_birimi)


# Read All
@router.get("/organizasyon-birimleri/", response_model=list[OrganizasyonBirimiRead])
def read_organizasyon_birimleri(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_organizasyon_birimleri(db, skip=skip, limit=limit)


# Read One
@router.get("/organizasyon-birimleri/{birim_no}", response_model=OrganizasyonBirimiRead)
def read_organizasyon_birimi(birim_no: int, db: Session = Depends(get_db)):
    db_organizasyon_birimi = get_organizasyon_birimi(db, birim_no=birim_no)
    if db_organizasyon_birimi is None:
        raise HTTPException(status_code=404, detail="Organizasyon Birimi bulunamadı.")
    return db_organizasyon_birimi


# Update
@router.put("/organizasyon-birimleri/{birim_no}", response_model=OrganizasyonBirimiRead)
def update_organizasyon_birimi_endpoint(
        birim_no: int, organizasyon_birimi: OrganizasyonBirimiUpdate, db: Session = Depends(get_db)
):
    updated_organizasyon_birimi = update_organizasyon_birimi(db, birim_no, organizasyon_birimi)
    if updated_organizasyon_birimi is None:
        raise HTTPException(status_code=404, detail="Organizasyon Birimi bulunamadı.")
    return updated_organizasyon_birimi


# Delete
@router.delete("/organizasyon-birimleri/{birim_no}")
def delete_organizasyon_birimi_endpoint(birim_no: int, db: Session = Depends(get_db)):
    result = delete_organizasyon_birimi(db, birim_no)
    if result is None:
        raise HTTPException(status_code=404, detail="Organizasyon Birimi bulunamadı.")
    return result
