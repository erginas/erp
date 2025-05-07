from sqlalchemy.orm import Session

from models import PNTS_KOD
from schemas import PNTS_KODCreate, PNTS_KODUpdate


# Create
def create_pnts_kod(db: Session, pnts_kod: PNTS_KODCreate):
    db_pnts_kod = PNTS_KOD(**pnts_kod.model_dump())
    db.add(db_pnts_kod)
    db.commit()
    db.refresh(db_pnts_kod)
    return db_pnts_kod


# Read All
def get_pnts_kodlar(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PNTS_KOD).offset(skip).limit(limit).all()


# Read One
def get_pnts_kod(db: Session, turu: str, kodu: str):
    return db.query(PNTS_KOD).filter(PNTS_KOD.turu == turu, PNTS_KOD.kodu == kodu).first()


# Update
def update_pnts_kod(db: Session, turu: str, kodu: str, pnts_kod: PNTS_KODUpdate):
    db_pnts_kod = db.query(PNTS_KOD).filter(PNTS_KOD.turu == turu, PNTS_KOD.kodu == kodu).first()
    if not db_pnts_kod:
        return None
    for key, value in pnts_kod.model_dump(exclude_unset=True).items():
        setattr(db_pnts_kod, key, value)
    db.commit()
    db.refresh(db_pnts_kod)
    return db_pnts_kod


# Delete
def delete_pnts_kod(db: Session, turu: str, kodu: str):
    db_pnts_kod = db.query(PNTS_KOD).filter(PNTS_KOD.turu == turu, PNTS_KOD.kodu == kodu).first()
    if not db_pnts_kod:
        return None
    db.delete(db_pnts_kod)
    db.commit()
    return {"message": "PNTS_KOD başarıyla silindi."}
