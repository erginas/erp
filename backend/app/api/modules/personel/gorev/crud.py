from sqlalchemy.orm import Session

from app.api.modules.personel.models import PersonelGorev
from app.api.modules.personel.schemas import PersonelGorevCreate, PersonelGorevUpdate


def get_personel_gorev(db: Session, personel_gorev_id: int):
    return db.query(PersonelGorev).filter(PersonelGorev.id == personel_gorev_id).first()


def get_personel_gorev_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelGorev).offset(skip).limit(limit).all()


def create_personel_gorev(db: Session, personel_gorev: PersonelGorevCreate):
    db_personel_gorev = PersonelGorev(**personel_gorev.dict())
    db.add(db_personel_gorev)
    db.commit()
    db.refresh(db_personel_gorev)
    return db_personel_gorev


def update_personel_gorev(db: Session, personel_gorev_id: int, personel_gorev_update: PersonelGorevUpdate):
    db_personel_gorev = db.query(PersonelGorev).filter(PersonelGorev.id == personel_gorev_id).first()
    if not db_personel_gorev:
        return None
    for key, value in personel_gorev_update.dict(exclude_unset=True).items():
        setattr(db_personel_gorev, key, value)
    db.commit()
    db.refresh(db_personel_gorev)
    return db_personel_gorev


def delete_personel_gorev(db: Session, personel_gorev_id: int):
    db_personel_gorev = db.query(PersonelGorev).filter(PersonelGorev.id == personel_gorev_id).first()
    if not db_personel_gorev:
        return None
    db.delete(db_personel_gorev)
    db.commit()
    return {"message": "PersonelGorev deleted"}
