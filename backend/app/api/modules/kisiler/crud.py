# crud.py
from datetime import date, timedelta
from math import ceil

from sqlalchemy import func
from sqlmodel import Session, select

from .models import Kisi, OrganizasyonBirim
from .schemas import KisiCreate, KisiUpdate, KisiFilter, Pagination


def get_paginated_kisiler(session: Session, filters: KisiFilter, page: int = 1, size: int = 100) -> Pagination[Kisi]:
    # Başlangıç sorgusu
    query = select(Kisi)

    # Genel filtreler - adi, soyadi vs.
    if filters.adi:
        query = query.where(Kisi.ADI.ilike(f"%{filters.adi}%"))
    if filters.soyadi:
        query = query.where(Kisi.SOYADI.ilike(f"%{filters.soyadi}%"))
    if filters.kimlik_no:
        query = query.where(Kisi.KIMLIK_NO == filters.kimlik_no)

    # Durum filtresi (aktif/çalışan)
    if filters.filter_type == "active":
        query = query.where(Kisi.ISTEN_CIKIS_T.is_(None))
    elif filters.filter_type == "inactive":
        query = query.where(Kisi.ISTEN_CIKIS_T.is_not(None))

    # Birime göre filtreleme
    if filters.birim_adi:
        query = (
            query.join(OrganizasyonBirim, Kisi.BIRIM_NO == OrganizasyonBirim.BIRIM_NO)
            .where(OrganizasyonBirim.ADI.ilike(f"%{filters.birim_adi}%"))
        )
        query = query.where(Kisi.ISTEN_CIKIS_T.is_(None))

    if filters.filter_type == "today-birthday":
        today = date.today()
        query = query.where(
            func.extract("day", Kisi.DOGUM_TARIHI) == today.day,
            func.extract("month", Kisi.DOGUM_TARIHI) == today.month
        )
        query = query.where(Kisi.ISTEN_CIKIS_T.is_(None))

    if filters.izin_donus_zamani:
        today = date.today()

        if filters.izin_donus_zamani == "bugun":
            baslangic = today
            bitis = today
        elif filters.izin_donus_zamani == "yarin":
            baslangic = today + timedelta(days=1)
            bitis = baslangic
        elif filters.izin_donus_zamani == "haftaya":
            baslangic = today + timedelta(days=2)
            bitis = today + timedelta(days=7)
        else:
            baslangic = bitis = None

        if baslangic and bitis:
            query = query.where(
                Kisi.IZINDEN_DONUS_TARIHI.between(baslangic, bitis)  # bu kısım varsayım böyle bir alan kontrol edilecek
            )

        if filters.izin_baslangic and filters.izin_bitis:
            query = query.where(
                Kisi.IZIN_BASLANGIC_TARIHI <= filters.izin_bitis,
                Kisi.IZIN_BITIS_TARIHI >= filters.izin_baslangic
            )

        if filters.dogum_gunu_gelecek_gun:
            today = date.today()
            days_range = filters.dogum_gunu_gelecek_gun
            end_date = today + timedelta(days=days_range)

            # Bu filtre sadece gün ve ay karşılaştırması yapar, yılı dikkate almaz.
            query = query.where(
                func.to_char(Kisi.DOGUM_TARIHI, 'MM-DD').between(
                    today.strftime('%m-%d'),
                    end_date.strftime('%m-%d')
                )
            )

    # Sayfalama ve toplam kişi sayısı
    count_statement = select(func.count()).select_from(query.subquery())
    total = session.exec(count_statement).one()

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
