from sqlalchemy.orm import Session

from .models import Personel
from .schemas import PersonelCreate, PersonelUpdate


def get_personel(db: Session, personel_id: int):
    return db.query(Personel).filter(Personel.id == personel_id).first()


def get_personel_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Personel).offset(skip).limit(limit).all()


def create_personel(db: Session, personel: PersonelCreate):
    db_personel = Personel(**personel.dict())
    db.add(db_personel)
    db.commit()
    db.refresh(db_personel)
    return db_personel


def update_personel(db: Session, personel_id: int, personel_update: PersonelUpdate):
    db_personel = db.query(Personel).filter(Personel.id == personel_id).first()
    if not db_personel:
        return None
    for key, value in personel_update.dict(exclude_unset=True).items():
        setattr(db_personel, key, value)
    db.commit()
    db.refresh(db_personel)
    return db_personel


def delete_personel(db: Session, personel_id: int):
    db_personel = db.query(Personel).filter(Personel.id == personel_id).first()
    if not db_personel:
        return None
    db.delete(db_personel)
    db.commit()
    return {"message": "Personel deleted"}
