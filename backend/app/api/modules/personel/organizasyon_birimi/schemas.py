# organizason birimi
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class OrganizasyonBirimiBase(BaseModel):
    bagimli_birim: Optional[int] = None
    kisa_kod: Optional[str] = None
    adi: str
    kimlik_no: Optional[int] = None
    iptal_t: Optional[date] = None
    iptal_nedeni: Optional[str] = None
    cesidi: Optional[str] = None
    gizli: Optional[int] = None
    aktif: Optional[int] = None
    ekleyen_kullanici_kimlik_no: Optional[int] = None
    ensonguncelleyen_kullanici_kimlik_no: Optional[int] = None
    eklenme_zamani: Optional[datetime] = None
    enson_guncellenme_zamani: Optional[datetime] = None
    mac_address: Optional[str] = None
    guncelleyen_mac_address: Optional[str] = None

    model_config = {
        "from_attributes": True  # ORM modunu etkinleştir
    }


# Create Şeması
class OrganizasyonBirimiCreate(OrganizasyonBirimiBase):
    pass


# Update Şeması
class OrganizasyonBirimiUpdate(OrganizasyonBirimiBase):
    adi: Optional[str] = None  # Güncelleme sırasında zorunlu olmayabilir


# Read Şeması
class OrganizasyonBirimiRead(OrganizasyonBirimiBase):
    birim_no: int
