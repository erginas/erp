from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlmodel import select, or_, col

from .models import Personel
from .schemas import PersonelCreate, PersonelUpdate


def get_filtered_personel_list(
    db: Session,
    page: int = 0,
    size: int = 20,
    search: Optional[str] = None,
    durum: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
    filters: dict = {}
):
    query = select(Personel)

    if durum == "aktif":
        query = query.where(Personel.cikis_tarihi == None)
    elif durum == "ayrilan":
        query = query.where(Personel.cikis_tarihi != None)

    if search:
        search_expr = f"%{search.lower()}%"
        query = query.where(
            or_(
                col(Personel.adi).ilike(search_expr),
                col(Personel.soyadi).ilike(search_expr),
                col(Personel.tc_kimlik_no).ilike(search_expr)
            )
        )

    for key, value in filters.items():
        column = getattr(Personel, key, None)
        if column is not None and value != "":
            query = query.where(column == value)

    if sort_by:
        sort_column = getattr(Personel, sort_by, None)
        if sort_column is not None:
            query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())

    count_query = query.with_only_columns(func.count()).order_by(None)
    total = db.exec(count_query).one()
    results = db.exec(query.offset(page * size).limit(size)).all()

    return {"items": results, "total": total}



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
