from sqlalchemy.orm import Session

from app.api.modules.personel.models import OrganizasyonBirimi
from app.api.modules.personel.organizasyon_birimi.schemas import OrganizasyonBirimiCreate, OrganizasyonBirimiUpdate


# Create
def create_organizasyon_birimi(db: Session, organizasyon_birimi: OrganizasyonBirimiCreate):
    db_organizasyon_birimi = OrganizasyonBirimi(**organizasyon_birimi.model_dump())
    db.add(db_organizasyon_birimi)
    db.commit()
    db.refresh(db_organizasyon_birimi)
    return db_organizasyon_birimi


# Read All
def get_organizasyon_birimleri(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrganizasyonBirimi).offset(skip).limit(limit).all()


# Read One
def get_organizasyon_birimi(db: Session, birim_no: int):
    return db.query(OrganizasyonBirimi).filter(OrganizasyonBirimi.birim_no == birim_no).first()


# Update
def update_organizasyon_birimi(db: Session, birim_no: int, organizasyon_birimi: OrganizasyonBirimiUpdate):
    db_organizasyon_birimi = db.query(OrganizasyonBirimi).filter(OrganizasyonBirimi.birim_no == birim_no).first()
    if not db_organizasyon_birimi:
        return None
    for key, value in organizasyon_birimi.model_dump(exclude_unset=True).items():
        setattr(db_organizasyon_birimi, key, value)
    db.commit()
    db.refresh(db_organizasyon_birimi)
    return db_organizasyon_birimi


# Delete
def delete_organizasyon_birimi(db: Session, birim_no: int):
    db_organizasyon_birimi = db.query(OrganizasyonBirimi).filter(OrganizasyonBirimi.birim_no == birim_no).first()
    if not db_organizasyon_birimi:
        return None
    db.delete(db_organizasyon_birimi)
    db.commit()
    return {"message": "Organizasyon Birimi başarıyla silindi."}
