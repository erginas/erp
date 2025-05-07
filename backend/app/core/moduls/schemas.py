from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# Ortak Alanlar
class PNTS_KODBase(BaseModel):
    turu: str
    kodu: str
    adi: Optional[str] = None
    skrs_kodu: Optional[int] = None
    yontem: Optional[str] = None
    renk_kodu: Optional[int] = None
    min_puan: Optional[int] = None
    max_puan: Optional[int] = None
    hesap_no: Optional[str] = None
    aktif: Optional[int] = None
    tetkik_grubu: Optional[int] = None
    sira: Optional[int] = None
    kk: Optional[int] = None
    maas_katsayisi: Optional[float] = None
    banka_hesap_no: Optional[str] = None
    aciklama: Optional[str] = None
    icerik_miktari: Optional[str] = None
    form: Optional[str] = None
    adet_miktar: Optional[str] = None
    detay: Optional[str] = None
    hesap_no_ds: Optional[str] = None
    dis_kodu: Optional[int] = None
    parent_turu: Optional[str] = None
    parent_kodu: Optional[str] = None
    onceki_sirasi: Optional[int] = None
    saramatik_baslangic_no: Optional[int] = None
    on_ek: Optional[int] = None
    sql_: Optional[str] = None
    sql_detay: Optional[str] = None
    banka_adi: Optional[str] = None
    banka_subesi: Optional[str] = None
    adres: Optional[str] = None
    deger: Optional[str] = None
    ent_resmi_kodu: Optional[str] = None
    ent_salon_adi: Optional[str] = None
    tetkik_id: Optional[int] = None
    malzeme_id: Optional[int] = None
    raf_omru_gunu: Optional[int] = None
    vergi_no: Optional[str] = None
    vergi_dairesi: Optional[str] = None
    saklama_sicakligi: Optional[int] = None
    skrs3_kodu: Optional[str] = None
    oncekinden_al: Optional[int] = None
    skrs3_master_kodu: Optional[int] = None
    skrs3_detay_kodu: Optional[str] = None
    medula_kodu: Optional[str] = None
    recete_tipi: Optional[str] = None
    parametreli_test: Optional[int] = None
    kultur_testi: Optional[int] = None
    taburcu_izin_saat: Optional[str] = None
    teslim: Optional[int] = None
    diskatman: Optional[str] = None
    bakanlik_kodu: Optional[str] = None
    modalite: Optional[str] = None
    yurtdisiilac_etkeni: Optional[int] = None
    ip_adresi: Optional[str] = None
    barkod_cihaz_kodu: Optional[str] = None
    port_numarasi: Optional[str] = None
    saat: Optional[float] = None
    barkod_cihaz_kodu2: Optional[str] = None
    vadecum_id: Optional[int] = None
    veri_tipi: Optional[str] = None
    donor_tetkik_id: Optional[int] = None
    dosya: Optional[bytes] = None
    donor_mu: Optional[int] = None
    tetkik_id_4: Optional[int] = None
    tetkik_id_6: Optional[int] = None
    mola_saat: Optional[str] = None
    tetkik_id_0_1: Optional[int] = None
    teletip_gonderilsin: Optional[int] = None
    teletip_mukerrer_sorgulama: Optional[int] = None
    sms_gonder: Optional[int] = None
    fides_gonder: Optional[int] = None
    dk: Optional[float] = None
    dts: Optional[datetime] = None
    kts: Optional[datetime] = None
    kan_yikama_uygunluk_durumu: Optional[float] = None
    kan_isinlama_uygunluk_durumu: Optional[float] = None
    kan_ayirma_uygunluk: Optional[float] = None
    buffycoat_uzaklastirmaya_uygun: Optional[float] = None
    kan_bolme_uygunluk: Optional[float] = None
    kan_filtreleme_uygunluk: Optional[float] = None
    kan_havuzlama_uygunluk: Optional[float] = None
    token: Optional[str] = None
    token_tarihi: Optional[date] = None
    saat_kontrolu_yapma: Optional[int] = None
    port_adresi: Optional[str] = None
    panates_id: Optional[int] = None
    doktor_teslim: Optional[int] = None
    sendika_odenek_orani: Optional[float] = None
    puantaj_saat: Optional[float] = None
    gonderilme_zamani: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # ORM modunu etkinleştir
    }


# Create Şeması
class PNTS_KODCreate(PNTS_KODBase):
    pass


# Update Şeması
class PNTS_KODUpdate(PNTS_KODBase):
    turu: Optional[str] = None
    kodu: Optional[str] = None


# Read Şeması
class PNTS_KODRead(PNTS_KODBase):
    turu: str
    kodu: str
