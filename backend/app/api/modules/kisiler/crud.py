from typing import List, Optional

from sqlmodel import Session, select

from app.api.modules.kisiler.models import Kisi
from app.api.modules.kisiler.schemas import KisiCreate, KisiUpdate


# 🚀 Yeni kişi oluşturma
def create_kisi(session: Session, kisi_in: KisiCreate) -> Kisi:
    # Yeni kimlik_no oluştur (manuel giriyorsan aşağıdaki kısmı kaldırabilirsin)
    kisi = Kisi(**kisi_in.model_dump())
    session.add(kisi)
    session.commit()
    session.refresh(kisi)
    return kisi


# 🚀 ID'ye göre kişi çekme
def get_kisi_by_id(session: Session, kimlik_no: int) -> Optional[Kisi]:
    return session.get(Kisi, kimlik_no)


# 🚀 Tüm kişileri listeleme (aktif filtreli + skip/limit destekli)
def list_kisiler(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[int] = None,
        kimlik_no: Optional[int] = None,
        adi: Optional[str] = None,
        soyadi: Optional[str] = None,
        cep_tel: Optional[str] = None,

) -> List[Kisi]:
    statement = select(Kisi)

    if is_active is not None:
        statement = statement.where(Kisi.is_active == is_active)
    if kimlik_no is not None:
        statement = statement.where(Kisi.kimlik_no == kimlik_no)
    if adi:
        statement = statement.where(Kisi.adi.contains(adi))
    if soyadi:
        statement = statement.where(Kisi.soyadi.contains(soyadi))
    if cep_tel:
        statement = statement.where(Kisi.cep_tel.contains(cep_tel))

    statement = statement.offset(skip).limit(limit)

    kisiler = session.exec(statement).all()
    return kisiler


# 🚀 Kişi güncelleme
def update_kisi(session: Session, kimlik_no: int, kisi_in: KisiUpdate) -> Optional[Kisi]:
    kisi = session.get(Kisi, kimlik_no)
    if not kisi:
        return None

    kisi_data = kisi_in.model_dump(exclude_unset=True)
    for key, value in kisi_data.items():
        setattr(kisi, key, value)

    session.add(kisi)
    session.commit()
    session.refresh(kisi)
    return kisi


# 🚀 Kişi soft delete (aktif = 0 yap)
def delete_kisi(session: Session, kimlik_no: int) -> Optional[Kisi]:
    kisi = session.get(Kisi, kimlik_no)
    if not kisi:
        return None

    kisi.is_active = 0
    session.add(kisi)
    session.commit()
    session.refresh(kisi)
    return kisi
