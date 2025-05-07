from sqlalchemy.orm import Session

from . import models, schemas


def get_all(db: Session):
    return db.query(models.HRPersonel).all()


def get_by_id(db: Session, id: int):
    return db.query(models.HRPersonel).filter(models.HRPersonel.id == id).first()


def create(db: Session, personel: schemas.HRPersonelCreate):
    db_personel = models.HRPersonel(**personel.dict())
    db.add(db_personel)
    db.commit()
    db.refresh(db_personel)
    return db_personel


def update(db: Session, id: int, personel: schemas.HRPersonelUpdate):
    db_personel = get_by_id(db, id)
    if db_personel:
        for field, value in personel.dict(exclude_unset=True).items():
            setattr(db_personel, field, value)
        db.commit()
        db.refresh(db_personel)
    return db_personel


def delete(db: Session, id: int):
    db_personel = get_by_id(db, id)
    if db_personel:
        db.delete(db_personel)
        db.commit()
    return db_personel
