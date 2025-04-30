from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class Kisi(SQLModel, table=True):
    kimlik_no: Optional[int] = Field(default=None, primary_key=True)
    adi: Optional[str] = Field(default=None, max_length=80)
    soyadi: Optional[str] = Field(default=None, max_length=80)
    baba_adi: Optional[str] = Field(default=None, max_length=80)
    ana_adi: Optional[str] = Field(default=None, max_length=80)
    meslegi: Optional[str] = Field(default=None, max_length=80)
    dogum_yeri: Optional[str] = Field(default=None, max_length=80)
    dogum_tarihi: Optional[date] = Field(default=None)
    kan_grubu: Optional[str] = Field(default=None, max_length=10)
    cinsiyeti: Optional[str] = Field(default=None, max_length=1)
    medeni_hali: Optional[str] = Field(default=None, max_length=10)
    ev_tel: Optional[str] = Field(default=None, max_length=50)
    cep_tel: Optional[str] = Field(default=None, max_length=50)
    is_tel: Optional[str] = Field(default=None, max_length=50)
    adres: Optional[str] = Field(default=None, max_length=255)
    ilgili_sirket: Optional[str] = Field(default=None, max_length=5)
    ise_giris_tarihi: Optional[date] = Field(default=None)
    isten_cikis_t: Optional[date] = Field(default=None)
    vergi_dairesi: Optional[str] = Field(default=None, max_length=120)
    vergi_no: Optional[str] = Field(default=None, max_length=20)
    birim_no: Optional[int] = Field(default=None)
    gorevi: Optional[str] = Field(default=None, max_length=80)
    mesai_fl: Optional[str] = Field(default=None, max_length=1)
    aciklama: Optional[str] = Field(default=None, max_length=1024)
    gorev_kodu: Optional[int] = Field(default=None)
    egitim_durumu: Optional[str] = Field(default=None, max_length=80)
    takma_ad: Optional[str] = Field(default=None, max_length=80)
    sifre: Optional[str] = Field(default=None, max_length=255)
    ayakkabi_no: Optional[str] = Field(default=None, max_length=10)
    ust_beden: Optional[str] = Field(default=None, max_length=10)
    alt_beden: Optional[str] = Field(default=None, max_length=10)
    is_active: Optional[int] = Field(default=1)  # 1: aktif, 0: pasif
