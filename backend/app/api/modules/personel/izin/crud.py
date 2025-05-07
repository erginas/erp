from datetime import date

from sqlalchemy.orm import Session

from .schemas import PersonelIzinCreate, PersonelIzinUpdate, PersonelIzinDetayCreate, PersonelIzinDetayUpdate, \
    PersonelIzinIptalUpdate, PersonelIzinIptalCreate, PersonelIzinTuruCreate, PersonelIzinTuruUpdate, \
    PersonelUnvanCreate, PersonelUnvanUpdate, TatilGunleriCreate, TatilGunleriUpdate
from ..models import PersonelIzin, PersonelIzinDetay, PersonelIzinIptal, PersonelIzinTuru, PersonelUnvan, TatilGunleri


def get_personel_izin(db: Session, personel_izin_id: int):
    return db.query(PersonelIzin).filter(PersonelIzin.id == personel_izin_id).first()


def get_personel_izin_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelIzin).offset(skip).limit(limit).all()


def create_personel_izin(db: Session, personel_izin: PersonelIzinCreate):
    db_personel_izin = PersonelIzin(**personel_izin.dict())
    db.add(db_personel_izin)
    db.commit()
    db.refresh(db_personel_izin)
    return db_personel_izin


def update_personel_izin(db: Session, personel_izin_id: int, personel_izin_update: PersonelIzinUpdate):
    db_personel_izin = db.query(PersonelIzin).filter(PersonelIzin.id == personel_izin_id).first()
    if not db_personel_izin:
        return None
    for key, value in personel_izin_update.dict(exclude_unset=True).items():
        setattr(db_personel_izin, key, value)
    db.commit()
    db.refresh(db_personel_izin)
    return db_personel_izin


def delete_personel_izin(db: Session, personel_izin_id: int):
    db_personel_izin = db.query(PersonelIzin).filter(PersonelIzin.id == personel_izin_id).first()
    if not db_personel_izin:
        return None
    db.delete(db_personel_izin)
    db.commit()
    return {"message": "PersonelIzin deleted"}


# Detay İşlemleri

def get_personel_izin_detay(db: Session, tarihi: date, personel_id: int, turu: int, izin_turu_id: int):
    return db.query(PersonelIzinDetay).filter(
        PersonelIzinDetay.tarihi == tarihi,
        PersonelIzinDetay.personel_id == personel_id,
        PersonelIzinDetay.turu == turu,
        PersonelIzinDetay.izin_turu_id == izin_turu_id
    ).first()


def get_personel_izin_detay_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelIzinDetay).offset(skip).limit(limit).all()


def create_personel_izin_detay(db: Session, personel_izin_detay: PersonelIzinDetayCreate):
    db_personel_izin_detay = PersonelIzinDetay(**personel_izin_detay.dict())
    db.add(db_personel_izin_detay)
    db.commit()
    db.refresh(db_personel_izin_detay)
    return db_personel_izin_detay


def update_personel_izin_detay(db: Session, tarihi: date, personel_id: int, turu: int, izin_turu_id: int,
                               personel_izin_detay_update: PersonelIzinDetayUpdate):
    db_personel_izin_detay = db.query(PersonelIzinDetay).filter(
        PersonelIzinDetay.tarihi == tarihi,
        PersonelIzinDetay.personel_id == personel_id,
        PersonelIzinDetay.turu == turu,
        PersonelIzinDetay.izin_turu_id == izin_turu_id
    ).first()
    if not db_personel_izin_detay:
        return None
    for key, value in personel_izin_detay_update.dict(exclude_unset=True).items():
        setattr(db_personel_izin_detay, key, value)
    db.commit()
    db.refresh(db_personel_izin_detay)
    return db_personel_izin_detay


def delete_personel_izin_detay(db: Session, tarihi: date, personel_id: int, turu: int, izin_turu_id: int):
    db_personel_izin_detay = db.query(PersonelIzinDetay).filter(
        PersonelIzinDetay.tarihi == tarihi,
        PersonelIzinDetay.personel_id == personel_id,
        PersonelIzinDetay.turu == turu,
        PersonelIzinDetay.izin_turu_id == izin_turu_id
    ).first()
    if not db_personel_izin_detay:
        return None
    db.delete(db_personel_izin_detay)
    db.commit()
    return {"message": "PersonelIzinDetay deleted"}


# izin iptal

def get_personel_izin_iptal(db: Session, iptal_id: int):
    return db.query(PersonelIzinIptal).filter(PersonelIzinIptal.id == iptal_id).first()


def get_personel_izin_iptal_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelIzinIptal).offset(skip).limit(limit).all()


def create_personel_izin_iptal(db: Session, iptal: PersonelIzinIptalCreate):
    db_iptal = PersonelIzinIptal(**iptal.dict())
    db.add(db_iptal)
    db.commit()
    db.refresh(db_iptal)
    return db_iptal


def update_personel_izin_iptal(db: Session, iptal_id: int, iptal_update: PersonelIzinIptalUpdate):
    db_iptal = db.query(PersonelIzinIptal).filter(PersonelIzinIptal.id == iptal_id).first()
    if not db_iptal:
        return None
    for key, value in iptal_update.dict(exclude_unset=True).items():
        setattr(db_iptal, key, value)
    db.commit()
    db.refresh(db_iptal)
    return db_iptal


def delete_personel_izin_iptal(db: Session, iptal_id: int):
    db_iptal = db.query(PersonelIzinIptal).filter(PersonelIzinIptal.id == iptal_id).first()
    if not db_iptal:
        return None
    db.delete(db_iptal)
    db.commit()
    return {"message": "PersonelIzinIptal deleted"}


# izin türü

def get_personel_izin_turu(db: Session, izin_turu_id: int):
    return db.query(PersonelIzinTuru).filter(PersonelIzinTuru.id == izin_turu_id).first()


def get_personel_izin_turu_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelIzinTuru).offset(skip).limit(limit).all()


def create_personel_izin_turu(db: Session, izin_turu: PersonelIzinTuruCreate):
    db_izin_turu = PersonelIzinTuru(**izin_turu.dict())
    db.add(db_izin_turu)
    db.commit()
    db.refresh(db_izin_turu)
    return db_izin_turu


def update_personel_izin_turu(db: Session, izin_turu_id: int, izin_turu_update: PersonelIzinTuruUpdate):
    db_izin_turu = db.query(PersonelIzinTuru).filter(PersonelIzinTuru.id == izin_turu_id).first()
    if not db_izin_turu:
        return None
    for key, value in izin_turu_update.dict(exclude_unset=True).items():
        setattr(db_izin_turu, key, value)
    db.commit()
    db.refresh(db_izin_turu)
    return db_izin_turu


def delete_personel_izin_turu(db: Session, izin_turu_id: int):
    db_izin_turu = db.query(PersonelIzinTuru).filter(PersonelIzinTuru.id == izin_turu_id).first()
    if not db_izin_turu:
        return None
    db.delete(db_izin_turu)
    db.commit()
    return {"message": "PersonelIzinTuru deleted"}


# perosnel unvan
def get_personel_unvan(db: Session, unvan_id: int):
    return db.query(PersonelUnvan).filter(PersonelUnvan.id == unvan_id).first()


def get_personel_unvan_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PersonelUnvan).offset(skip).limit(limit).all()


def create_personel_unvan(db: Session, unvan: PersonelUnvanCreate):
    db_unvan = PersonelUnvan(**unvan.dict())
    db.add(db_unvan)
    db.commit()
    db.refresh(db_unvan)
    return db_unvan


def update_personel_unvan(db: Session, unvan_id: int, unvan_update: PersonelUnvanUpdate):
    db_unvan = db.query(PersonelUnvan).filter(PersonelUnvan.id == unvan_id).first()
    if not db_unvan:
        return None
    for key, value in unvan_update.dict(exclude_unset=True).items():
        setattr(db_unvan, key, value)
    db.commit()
    db.refresh(db_unvan)
    return db_unvan


def delete_personel_unvan(db: Session, unvan_id: int):
    db_unvan = db.query(PersonelUnvan).filter(PersonelUnvan.id == unvan_id).first()
    if not db_unvan:
        return None
    db.delete(db_unvan)
    db.commit()
    return {"message": "PersonelUnvan deleted"}


# tatil günleri

def get_tatil_gunleri(db: Session, ilk_tarih: date, adi: str):
    return db.query(TatilGunleri).filter(
        TatilGunleri.ilk_tarih == ilk_tarih,
        TatilGunleri.adi == adi
    ).first()


def get_tatil_gunleri_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TatilGunleri).offset(skip).limit(limit).all()


def create_tatil_gunleri(db: Session, tatil_gunleri: TatilGunleriCreate):
    db_tatil_gunleri = TatilGunleri(**tatil_gunleri.dict())
    db.add(db_tatil_gunleri)
    db.commit()
    db.refresh(db_tatil_gunleri)
    return db_tatil_gunleri


def update_tatil_gunleri(db: Session, ilk_tarih: date, adi: str, tatil_gunleri_update: TatilGunleriUpdate):
    db_tatil_gunleri = db.query(TatilGunleri).filter(
        TatilGunleri.ilk_tarih == ilk_tarih,
        TatilGunleri.adi == adi
    ).first()
    if not db_tatil_gunleri:
        return None
    for key, value in tatil_gunleri_update.dict(exclude_unset=True).items():
        setattr(db_tatil_gunleri, key, value)
    db.commit()
    db.refresh(db_tatil_gunleri)
    return db_tatil_gunleri


def delete_tatil_gunleri(db: Session, ilk_tarih: date, adi: str):
    db_tatil_gunleri = db.query(TatilGunleri).filter(
        TatilGunleri.ilk_tarih == ilk_tarih,
        TatilGunleri.adi == adi
    ).first()
    if not db_tatil_gunleri:
        return None
    db.delete(db_tatil_gunleri)
    db.commit()
    return {"message": "TatilGunleri deleted"}
