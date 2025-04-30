from datetime import date
from typing import Optional

from sqlmodel import SQLModel


# 🚀 YENİ KİŞİ OLUŞTURMA SCHEMA
class KisiCreate(SQLModel):
    kimlik_no: int
    adi: str
    soyadi: str
    baba_adi: Optional[str] = None
    ana_adi: Optional[str] = None
    meslegi: Optional[str] = None
    dogum_yeri: Optional[str] = None
    dogum_tarihi: Optional[date] = None
    kan_grubu: Optional[str] = None
    cinsiyeti: Optional[str] = None
    medeni_hali: Optional[str] = None
    ev_tel: Optional[str] = None
    cep_tel: Optional[str] = None
    is_tel: Optional[str] = None
    adres: Optional[str] = None
    ilgili_sirket: Optional[str] = None
    ise_giris_tarihi: Optional[date] = None
    isten_cikis_t: Optional[date] = None
    vergi_dairesi: Optional[str] = None
    vergi_no: Optional[str] = None
    birim_no: Optional[int] = None
    gorevi: Optional[str] = None
    mesai_fl: Optional[str] = None
    aciklama: Optional[str] = None
    gorev_kodu: Optional[int] = None
    egitim_durumu: Optional[str] = None
    takma_ad: Optional[str] = None
    sifre: Optional[str] = None
    ayakkabi_no: Optional[str] = None
    ust_beden: Optional[str] = None
    alt_beden: Optional[str] = None
    is_active: Optional[int] = 1


# 🚀 KİŞİ GÜNCELLEME SCHEMA
class KisiUpdate(SQLModel):
    adi: Optional[str] = None
    soyadi: Optional[str] = None
    baba_adi: Optional[str] = None
    ana_adi: Optional[str] = None
    meslegi: Optional[str] = None
    dogum_yeri: Optional[str] = None
    dogum_tarihi: Optional[date] = None
    kan_grubu: Optional[str] = None
    cinsiyeti: Optional[str] = None
    medeni_hali: Optional[str] = None
    ev_tel: Optional[str] = None
    cep_tel: Optional[str] = None
    is_tel: Optional[str] = None
    adres: Optional[str] = None
    ilgili_sirket: Optional[str] = None
    ise_giris_tarihi: Optional[date] = None
    isten_cikis_t: Optional[date] = None
    vergi_dairesi: Optional[str] = None
    vergi_no: Optional[str] = None
    birim_no: Optional[int] = None
    gorevi: Optional[str] = None
    mesai_fl: Optional[str] = None
    aciklama: Optional[str] = None
    gorev_kodu: Optional[int] = None
    egitim_durumu: Optional[str] = None
    takma_ad: Optional[str] = None
    sifre: Optional[str] = None
    ayakkabi_no: Optional[str] = None
    ust_beden: Optional[str] = None
    alt_beden: Optional[str] = None
    is_active: Optional[int] = None


# 🚀 KİŞİ OKUMA SCHEMA (RESPONSE)
class KisiRead(SQLModel):
    kimlik_no: int
    adi: Optional[str] = None
    soyadi: Optional[str] = None
    baba_adi: Optional[str] = None
    ana_adi: Optional[str] = None
    meslegi: Optional[str] = None
    dogum_yeri: Optional[str] = None
    dogum_tarihi: Optional[date] = None
    kan_grubu: Optional[str] = None
    cinsiyeti: Optional[str] = None
    medeni_hali: Optional[str] = None
    ev_tel: Optional[str] = None
    cep_tel: Optional[str] = None
    is_tel: Optional[str] = None
    adres: Optional[str] = None
    ilgili_sirket: Optional[str] = None
    ise_giris_tarihi: Optional[date] = None
    isten_cikis_t: Optional[date] = None
    vergi_dairesi: Optional[str] = None
    vergi_no: Optional[str] = None
    birim_no: Optional[int] = None
    gorevi: Optional[str] = None
    mesai_fl: Optional[str] = None
    aciklama: Optional[str] = None
    gorev_kodu: Optional[int] = None
    egitim_durumu: Optional[str] = None
    takma_ad: Optional[str] = None
    ayakkabi_no: Optional[str] = None
    ust_beden: Optional[str] = None
    alt_beden: Optional[str] = None
    is_active: Optional[int] = None
