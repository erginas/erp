# crud.py
from math import ceil

from sqlalchemy import func
from sqlmodel import Session, select

from .models import Kisi
from .schemas import KisiCreate, KisiUpdate, KisiFilter, Pagination


def get_paginated_kisiler(session: Session, filters: KisiFilter, page: int = 1, size: int = 100) -> Pagination[Kisi]:
    # Temel sorgu
    query = select(Kisi)

    # Filtre uygulama
    if filters.adi:
        query = query.where(Kisi.ADI.ilike(f"%{filters.adi}%"))
    if filters.soyadi:
        query = query.where(Kisi.SOYADI.ilike(f"%{filters.soyadi}%"))
    if filters.kimlik_no:
        query = query.where(Kisi.KIMLIK_NO == filters.kimlik_no)
    if filters.birim_no:
        query = query.where(Kisi.BIRIM_NO == filters.birim_no)
    if filters.isten_cikis_t is not None:
        if filters.isten_cikis_t:
            query = query.where(Kisi.ISTEN_CIKIS_T.is_not(None))
        else:
            query = query.where(Kisi.ISTEN_CIKIS_T.is_(None))

    # Toplam kayıt sayısını al (filtreye göre)
    count_statement = select(func.count()).select_from(query.subquery())
    total = session.exec(count_statement).one()

    # Sayfalama uygula
    items = session.exec(query.offset((page - 1) * size).limit(size)).all()

    total_pages = ceil(total / size) if size > 0 else 0

    return Pagination[Kisi](
        data=items,
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )


def get_kisi(session: Session, kimlik_no: int):
    return session.get(Kisi, kimlik_no)


def get_kisiler(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Kisi).offset(skip).limit(limit)).all()


def create_kisi(session: Session, kisi: KisiCreate):
    db_kisi = Kisi.model_validate(kisi)
    session.add(db_kisi)
    session.commit()
    session.refresh(db_kisi)
    return db_kisi


def update_kisi(session: Session, kimlik_no: int, kisi: KisiUpdate):
    db_kisi = session.get(Kisi, kimlik_no)
    if not db_kisi:
        return None
    kisi_data = kisi.model_dump(exclude_unset=True)
    for key, value in kisi_data.items():
        setattr(db_kisi, key, value)
    session.commit()
    session.refresh(db_kisi)
    return db_kisi


def delete_kisi(session: Session, kimlik_no: int):
    db_kisi = session.get(Kisi, kimlik_no)
    if not db_kisi:
        return None
    session.delete(db_kisi)
    session.commit()
    return {"message": "Kişi başarıyla silindi."}
