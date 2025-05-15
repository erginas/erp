# schemas.py
from datetime import date
from typing import Optional, TypeVar, List, Generic

from pydantic import BaseModel

from app.api.modules.kisiler.fields import KisiFields

T = TypeVar("T")


class OrganizasyonBirimRead(BaseModel):
    BIRIM_NO: int
    BAGIMLI_BIRIM: Optional[int]
    KISA_KOD: Optional[str]
    ADI: Optional[str]
    KIMLIK_NO: Optional[int]
    IPTAL_T: Optional[date]
    IPTAL_NEDENI: Optional[str]
    CESIDI: Optional[str]
    GIZLI: Optional[int]
    AKTIF: Optional[int]

    class Config:
        from_attributes = True


class KisiBase(KisiFields, BaseModel):
    KIMLIK_NO: int
    ADI: Optional[str]
    SOYADI: Optional[str]
    BIRIM_NO: Optional[int]
    GOREV_KODU: Optional[int]
    TAKMA_AD: Optional[str]

    birim: Optional[OrganizasyonBirimRead] = None
    gorev_birimi: Optional[OrganizasyonBirimRead] = None

    class Config:
        from_attributes = True


class KisiCreate(KisiBase):
    KIMLIK_NO: int
    TAKMA_AD: str  # Unique olduğu için zorunlu


class KisiUpdate(KisiBase):
    pass


class KisiRead(KisiBase):
    KIMLIK_NO: int


class KisiFilter(BaseModel):
    adi: Optional[str] = None
    soyadi: Optional[str] = None
    kimlik_no: Optional[int] = None
    birim_adi: Optional[str] = None  # 👈 Burayı ekliyoruz
    isten_cikis_t: Optional[bool] = None  # ✅ Bu alan eksikse veya yanlış tanımlıysa çalışmaz
    filter_type: Optional[str] = None
    unit_name: Optional[str] = None
    unit: Optional[str] = None
    dogum_tarihi: Optional[str] = None
    izin_donus_zamani: Optional[str] = None  # "bugun", "yarin", "haftaya"
    izin_baslangic: Optional[date] = None
    izin_bitis: Optional[date] = None
    dogum_gunu_gelecek_gun: Optional[int] = None  # örn: 7


class Pagination(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int
    total_pages: int

    class Config:
        from_attributes = True
