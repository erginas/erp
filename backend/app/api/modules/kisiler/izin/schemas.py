from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PersonelIzinCreate(BaseModel):
    personel_id: int
    yili: int
    tur_id: int
    plan_izin: int
    baslama_tarihi: date
    suresi: int
    yol: int
    donus_tarihi: Optional[date] = None
    aciklama: Optional[str] = None
    adresi: Optional[str] = None
    sayi: Optional[int] = None
    hbys_engelle: Optional[int] = 0
    ukk: Optional[int] = None
    ukts: Optional[datetime] = None
    ait_oldugu_yil: Optional[int] = None
    ait_oldugu_yil_detay: Optional[str] = None
    vekil_personel_id: Optional[int] = None
    imza1_personel_id: Optional[int] = None
    imza2_personel_id: Optional[int] = None
    imza3_personel_id: Optional[int] = None
    imza4_personel_id: Optional[int] = None
    tatil_gunu: Optional[int] = None
    teslim_edildi: Optional[int] = None
    onay: Optional[int] = None
    onay_kk: Optional[int] = None
    onay_kts: Optional[datetime] = None
    resmi_tatil: Optional[int] = None
    isci_tatil_haric: Optional[int] = None
    izin_aciklama: Optional[str] = None
    cinsiyet: Optional[int] = None
    fides_gonderim_zamani: Optional[datetime] = None
    sgk_bildirildi: Optional[int] = None
    sgk_bildirilme_kts: Optional[datetime] = None
    sgk_bildirilme_kk: Optional[int] = None
    fides_gonder: Optional[int] = None
    dk: Optional[float] = None
    dts: Optional[datetime] = None
    maas_teslim_edildi: Optional[int] = None
    gizli: Optional[int] = None
    rapor_kurum_id: Optional[int] = None

    class Config:
        from_attributes = True


class PersonelIzinRead(PersonelIzinCreate):
    id: int


class PersonelIzinUpdate(BaseModel):
    personel_id: Optional[int] = None
    yili: Optional[int] = None
    tur_id: Optional[int] = None
    plan_izin: Optional[int] = None
    baslama_tarihi: Optional[date] = None
    suresi: Optional[int] = None
    yol: Optional[int] = None
    donus_tarihi: Optional[date] = None
    aciklama: Optional[str] = None
    adresi: Optional[str] = None
    sayi: Optional[int] = None
    hbys_engelle: Optional[int] = None
    ukk: Optional[int] = None
    ukts: Optional[datetime] = None
    ait_oldugu_yil: Optional[int] = None
    ait_oldugu_yil_detay: Optional[str] = None
    vekil_personel_id: Optional[int] = None
    imza1_personel_id: Optional[int] = None
    imza2_personel_id: Optional[int] = None
    imza3_personel_id: Optional[int] = None
    imza4_personel_id: Optional[int] = None
    tatil_gunu: Optional[int] = None
    teslim_edildi: Optional[int] = None
    onay: Optional[int] = None
    onay_kk: Optional[int] = None
    onay_kts: Optional[datetime] = None
    resmi_tatil: Optional[int] = None
    isci_tatil_haric: Optional[int] = None
    izin_aciklama: Optional[str] = None
    cinsiyet: Optional[int] = None
    fides_gonderim_zamani: Optional[datetime] = None
    sgk_bildirildi: Optional[int] = None
    sgk_bildirilme_kts: Optional[datetime] = None
    sgk_bildirilme_kk: Optional[int] = None
    fides_gonder: Optional[int] = None
    dk: Optional[float] = None
    dts: Optional[datetime] = None
    maas_teslim_edildi: Optional[int] = None
    gizli: Optional[int] = None
    rapor_kurum_id: Optional[int] = None

    class Config:
        from_attributes = True


class PersonelIzinDetayCreate(BaseModel):
    tarihi: date
    personel_id: int
    turu: int
    izin_turu_id: int
    personel_izin_id: Optional[int] = None
    personel_rotasyon_id: Optional[int] = None
    mhrs_istisna_id: Optional[int] = None

    class Config:
        from_attributes = True


class PersonelIzinDetayRead(PersonelIzinDetayCreate):
    pass


class PersonelIzinDetayUpdate(BaseModel):
    tarihi: Optional[date] = None
    personel_id: Optional[int] = None
    turu: Optional[int] = None
    izin_turu_id: Optional[int] = None
    personel_izin_id: Optional[int] = None
    personel_rotasyon_id: Optional[int] = None
    mhrs_istisna_id: Optional[int] = None

    class Config:
        from_attributes = True


# izin iptal

class PersonelIzinIptalCreate(BaseModel):
    personel_id: int
    yili: int
    tur_id: int
    plan_izin: int
    baslama_tarihi: date
    suresi: int
    yol: int
    donus_tarihi: Optional[date] = None
    aciklama: Optional[str] = None
    adresi: Optional[str] = None
    mgp_engelle: Optional[int] = None
    ait_oldugu_yil: Optional[int] = None
    ait_oldugu_yil_detay: Optional[str] = None
    vekil_personel_id: Optional[int] = None
    imza1_personel_id: Optional[int] = None
    imza2_personel_id: Optional[int] = None
    imza3_personel_id: Optional[int] = None
    imza4_personel_id: Optional[int] = None
    cinsiyet: Optional[int] = None
    izin_aciklama: Optional[str] = None
    onay_kk: Optional[int] = None
    onay_kts: Optional[datetime] = None
    onay: Optional[int] = None
    bitis_tarihi: Optional[date] = None

    class Config:
        from_attributes = True


class PersonelIzinIptalRead(PersonelIzinIptalCreate):
    id: int


class PersonelIzinIptalUpdate(BaseModel):
    personel_id: Optional[int] = None
    yili: Optional[int] = None
    tur_id: Optional[int] = None
    plan_izin: Optional[int] = None
    baslama_tarihi: Optional[date] = None
    suresi: Optional[int] = None
    yol: Optional[int] = None
    donus_tarihi: Optional[date] = None
    aciklama: Optional[str] = None
    adresi: Optional[str] = None
    mgp_engelle: Optional[int] = None
    ait_oldugu_yil: Optional[int] = None
    ait_oldugu_yil_detay: Optional[str] = None
    vekil_personel_id: Optional[int] = None
    imza1_personel_id: Optional[int] = None
    imza2_personel_id: Optional[int] = None
    imza3_personel_id: Optional[int] = None
    imza4_personel_id: Optional[int] = None
    cinsiyet: Optional[int] = None
    izin_aciklama: Optional[str] = None
    onay_kk: Optional[int] = None
    onay_kts: Optional[datetime] = None
    onay: Optional[int] = None
    bitis_tarihi: Optional[date] = None

    class Config:
        from_attributes = True


# izin Türü

class PersonelIzinTuruCreate(BaseModel):
    adi: str
    tipi: str
    ucretlimi: str
    min_suresi: Optional[int] = None
    max_suresi: Optional[int] = None
    aciklama: Optional[str] = None
    kk: int
    saatlik: Optional[int] = 0
    turu: Optional[str] = None
    ay_max_suresi: Optional[int] = None
    engelle: Optional[int] = None
    aksiyon_kodu: Optional[str] = None
    terfi_durdur: Optional[int] = None
    haric: Optional[int] = None
    ay_max_adedi: Optional[int] = None
    sms_gonder: Optional[int] = None
    cinsiyet_zorunlu: Optional[int] = None
    nobet_turu: Optional[int] = None
    sgk_zorunlu: Optional[int] = None
    tatil_gunu: Optional[int] = None
    fides_gonder: Optional[int] = None
    yillik_max_adet: Optional[int] = None
    calisma_listesi_dahil: Optional[int] = None

    class Config:
        from_attributes = True


class PersonelIzinTuruRead(PersonelIzinTuruCreate):
    id: int


class PersonelIzinTuruUpdate(BaseModel):
    adi: Optional[str] = None
    tipi: Optional[str] = None
    ucretlimi: Optional[str] = None
    min_suresi: Optional[int] = None
    max_suresi: Optional[int] = None
    aciklama: Optional[str] = None
    kk: Optional[int] = None
    saatlik: Optional[int] = None
    turu: Optional[str] = None
    ay_max_suresi: Optional[int] = None
    engelle: Optional[int] = None
    aksiyon_kodu: Optional[str] = None
    terfi_durdur: Optional[int] = None
    haric: Optional[int] = None
    ay_max_adedi: Optional[int] = None
    sms_gonder: Optional[int] = None
    cinsiyet_zorunlu: Optional[int] = None
    nobet_turu: Optional[int] = None
    sgk_zorunlu: Optional[int] = None
    tatil_gunu: Optional[int] = None
    fides_gonder: Optional[int] = None
    yillik_max_adet: Optional[int] = None
    calisma_listesi_dahil: Optional[int] = None

    class Config:
        from_attributes = True


# personel unvan
class PersonelUnvanCreate(BaseModel):
    adi: str
    oncelik_no: int
    kk: int
    standart_adet: Optional[int] = None
    mevcut_adet: Optional[int] = None
    bakanlik_kodu: Optional[str] = None
    aktif: Optional[int] = None

    class Config:
        from_attributes = True


class PersonelUnvanRead(PersonelUnvanCreate):
    id: int


class PersonelUnvanUpdate(BaseModel):
    adi: Optional[str] = None
    oncelik_no: Optional[int] = None
    standart_adet: Optional[int] = None
    mevcut_adet: Optional[int] = None
    bakanlik_kodu: Optional[str] = None
    aktif: Optional[int] = None

    class Config:
        from_attributes = True


# tatil günleri
class TatilGunleriCreate(BaseModel):
    ilk_tarih: date
    son_tarih: date
    adi: str
    tipi: int
    nobet_haric: Optional[int] = None

    class Config:
        from_attributes = True


class TatilGunleriRead(TatilGunleriCreate):
    pass


class TatilGunleriUpdate(BaseModel):
    ilk_tarih: Optional[date] = None
    son_tarih: Optional[date] = None
    adi: Optional[str] = None
    tipi: Optional[int] = None
    nobet_haric: Optional[int] = None

    class Config:
        from_attributes = True
