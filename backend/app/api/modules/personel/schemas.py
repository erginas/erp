from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PersonelCreate(BaseModel):
    # Zorunlu Alanlar
    adi: str
    soyadi: str
    kk: int
    kts: datetime  # Default değeri var, ancak zorunlu olabilir.

    # İsteğe Bağlı Alanlar
    tc_kimlik_no: Optional[int] = None
    sicil_no: Optional[str] = None
    siralama_kodu: Optional[int] = None
    cinsiyeti: Optional[str] = None
    dogum_tarihi: Optional[date] = None
    kadro_turu: Optional[int] = None
    sinif_id: Optional[int] = None
    unvan_id: Optional[int] = None
    brans_id: Optional[int] = None
    gorev_id: Optional[int] = None
    durum_id: Optional[int] = None
    birim_id: Optional[int] = None
    dis_kurum_id: Optional[int] = None
    part_time: Optional[int] = 0
    part_time_tarihi: Optional[date] = None
    otomasyon_kod: Optional[str] = None
    kisa_unvani: Optional[str] = None
    ise_baslama_tarihi: Optional[date] = None
    memuriyete_giris_tarihi: Optional[date] = None
    asil_memuriyet_tarihi: Optional[date] = None
    sigorta_sicil_no: Optional[str] = None
    emekli_sicil_no: Optional[str] = None
    bagkur_sicil_no: Optional[str] = None
    cocuk_sayisi: Optional[int] = None
    ogrenim_durumu_id: Optional[int] = None
    sendika_id: Optional[int] = None
    ev_adresi1: Optional[str] = None
    ev_adresi2: Optional[str] = None
    ev_posta_kodu: Optional[str] = None
    ev_telefonu: Optional[str] = None
    cep_telefonu: Optional[str] = None
    eposta: Optional[str] = None
    isyeri_adresi1: Optional[str] = None
    isyeri_adresi2: Optional[str] = None
    isyeri_posta_kodu: Optional[str] = None
    isyeri_telefonu: Optional[str] = None
    acil_ulasilacak_kisi: Optional[str] = None
    acil_ulasilacak_tel: Optional[str] = None
    vergi_dairesi: Optional[str] = None
    vergi_no: Optional[str] = None
    baba_adi: Optional[str] = None
    ana_adi: Optional[str] = None
    dogum_yeri: Optional[str] = None
    medeni_hal_kodu: Optional[int] = None
    kimlik_kart_seri: Optional[str] = None
    kimlik_kart_no: Optional[str] = None
    kimlik_il_id: Optional[int] = None
    kimlik_ilce_id: Optional[int] = None
    kimlik_mahalle: Optional[str] = None
    kimlik_cilt_no: Optional[str] = None
    kimlik_aile_sira_no: Optional[str] = None
    kimlik_sira_no: Optional[str] = None
    kimlik_verildigi_yer: Optional[str] = None
    kimlik_verilis_nedeni: Optional[str] = None
    kimlik_verilis_tarihi: Optional[date] = None
    kimlik_kayit_no: Optional[str] = None
    onceki_soyadi: Optional[str] = None
    kan_grubu_id: Optional[int] = None
    askere_gidis_tarihi: Optional[date] = None
    askerden_donus_tarihi: Optional[date] = None
    askerlik_degerlendirmesi: Optional[int] = None
    banka_id: Optional[int] = None
    banka_hesap_no: Optional[str] = None
    cikis_tarihi: Optional[date] = None
    cikis_turu_id: Optional[int] = None
    cikis_aciklama: Optional[str] = None
    cikis_atama_tarihi: Optional[date] = None
    cikis_tebliğ_tarihi: Optional[date] = None
    cikis_atama_yeri: Optional[str] = None
    diploma_no: Optional[str] = None
    diploma_tescil_no: Optional[str] = None
    diploma_tescil_tarihi: Optional[date] = None
    kidem_yili_dusulen: Optional[int] = None
    kidem_yili_ssk: Optional[int] = None
    resim_blob_id: Optional[int] = None
    puan_alabilir: Optional[int] = 1
    arsiv: Optional[int] = 0
    kurum_gorev_id: Optional[int] = None
    kadro_unvan_tarihi: Optional[date] = None
    asistanlik_tarihi: Optional[date] = None
    bas_asistanlik_tarihi: Optional[date] = None
    uzmanlik_tarihi: Optional[date] = None
    sef_yardimcisi_tarihi: Optional[date] = None
    sef_tarihi: Optional[date] = None
    baba_soyadi: Optional[str] = None
    temp_diploma_tescil_no: Optional[int] = None
    adi_soyadi: Optional[str] = None
    bildigi_diller: Optional[str] = None
    web_parolasi: Optional[str] = None
    docentlik_tarihi: Optional[date] = None
    temp_master_flg: Optional[int] = None
    kalite_bolumu_id: Optional[int] = None
    gizli: Optional[int] = 0
    donus_tarihi: Optional[date] = None
    giden_gelen: Optional[int] = None
    sw_engelle: Optional[int] = 0
    birlestirildi: Optional[int] = None
    master_flg: Optional[int] = None
    ikamet_il_id: Optional[int] = None
    ikamet_ilce_id: Optional[int] = None
    uyrug_kodu: Optional[str] = None
    nvi_onayli: Optional[int] = 0
    arsiv_no: Optional[int] = None
    iban_no: Optional[str] = None
    iban_no2: Optional[str] = None
    ek_banka_id: Optional[int] = None
    ek_banka_hesap_no: Optional[str] = None
    banka_sube_no: Optional[str] = None
    banka_sube_no2: Optional[str] = None
    mazeret_durum_id: Optional[int] = None
    kimlik_il_aktarma: Optional[str] = None
    kimlik_ilce_aktarma: Optional[str] = None
    cihaz_ariza_gorunsun: Optional[int] = 0
    sendika_giris_tarihi: Optional[date] = None
    sendika_cikis_tarihi: Optional[date] = None
    mezun_oldugu_okul: Optional[str] = None
    dosya_no: Optional[int] = None
    sakatlik_dercesi: Optional[int] = None
    ev_mahalle: Optional[str] = None
    ev_mahalle_kodu: Optional[str] = None
    ev_adres_no: Optional[str] = None
    nobet_saat: Optional[float] = None
    aktarma_numarasi: Optional[str] = None
    asalet_durumu: Optional[int] = None
    mezuniyet_tarihi: Optional[date] = None
    geldigi_yer: Optional[str] = None
    askerlik_durumu: Optional[int] = None
    askerlik_tecil_tarihi: Optional[date] = None
    sendika_no: Optional[str] = None
    kidem_tarihi: Optional[date] = None
    calisma_planinda_goster: Optional[int] = None
    asil_onay_no: Optional[str] = None
    saramatik_resim_goster: Optional[int] = 1
    skrs_doktor_bulunamadi: Optional[int] = None
    maas_terfi_tarihi: Optional[date] = None
    bashekim_onayi: Optional[int] = None
    terfi_durdur: Optional[int] = None
    emekli_terfi_tarihi: Optional[date] = None
    tmp_tc_kimlik_no: Optional[str] = None
    olum_tarihi: Optional[date] = None
    kart_no: Optional[str] = None
    grup_id: Optional[int] = None
    erecete_eimza: Optional[int] = None
    ihtisas_baslama_tarihi: Optional[date] = None
    ihtisas_bitis_tarihi: Optional[date] = None
    ilgi_alani: Optional[str] = None
    asistanlik_bitis_tarihi: Optional[date] = None
    asistanlik_aciklama: Optional[str] = None
    isyeri_telefonu_dahili: Optional[str] = None
    izin_aciklama: Optional[str] = None
    izin_engelle: Optional[int] = None
    nobet_muaf: Optional[int] = None
    nobet_muaf_aciklama: Optional[str] = None
    profesor_tarihi: Optional[date] = None
    aciga_alinma_tarihi: Optional[date] = None
    durum_aciklama: Optional[str] = None
    resim_dosya_yolu: Optional[str] = None
    eimza_baslangic_tarihi: Optional[date] = None
    eimza_bitis_tarihi: Optional[date] = None
    pdks_kart_no: Optional[str] = None
    pdks_kart_pin: Optional[int] = None
    banka_ekno: Optional[int] = None
    banka_ekno2: Optional[int] = None
    arsiv_kk: Optional[int] = None
    arsiv_kts: Optional[date] = None
    arac_marka: Optional[int] = None
    arac_model: Optional[int] = None
    arac_yakit: Optional[int] = None
    arac_renk: Optional[int] = None
    arac_marka2: Optional[int] = None
    arac_model2: Optional[int] = None
    arac_yakit2: Optional[int] = None
    arac_renk2: Optional[int] = None
    arac_plaka: Optional[str] = None
    arac_plaka2: Optional[str] = None
    gecis_tarihi_4d: Optional[date] = None
    aylik_hak_tarihi: Optional[date] = None
    erapor_bashekim_onayi: Optional[int] = None
    ozgecmis: Optional[str] = None
    engelli_kisi: Optional[int] = None
    ozur_orani: Optional[int] = None
    kurumdisi_ekodeme: Optional[int] = None
    ilk_sigorta_tarihi: Optional[date] = None
    hemsirelik_yapabilir: Optional[int] = None
    kurumsal_eposta: Optional[str] = None
    gecis_tarihi_sbu: Optional[date] = None
    onay_tarihi_sbu: Optional[date] = None
    vekalet_baslama_tarihi: Optional[date] = None
    kurum_brans_id: Optional[int] = None
    gunluk_mesai_saati: Optional[float] = None
    fides_durumu: Optional[int] = None
    fides_gonderim_zamani: Optional[date] = None
    fides_gonderim_kk: Optional[int] = None
    fides_grubu: Optional[int] = None
    fides_gonderme: Optional[int] = None
    misafir_doktor: Optional[int] = None
    iskurdan_gelen: Optional[int] = None
    webde_goster: Optional[int] = None
    firma_id: Optional[int] = None
    calisma_sistemi: Optional[int] = None
    dk: Optional[int] = None
    dts: Optional[date] = None
    hekim_medula_sifresi: Optional[str] = None
    terfi_tarihi: Optional[date] = None
    devlet_hizmet_yukumluluk_kodu: Optional[int] = None
    kadro_unvan_id: Optional[int] = None
    imza_unvan_id: Optional[int] = None
    adres_tipi: Optional[int] = None
    adres_kodu_seviyesi: Optional[int] = None
    kadrolu_gorev_yeri: Optional[str] = None
    izin_baslangic_tarihi_4d: Optional[date] = None
    emekli_olacagi_tarih: Optional[date] = None
    lios_kullanici: Optional[str] = None
    lios_sifre: Optional[str] = None
    bagli_birim_id: Optional[int] = None
    skrs_brans_id: Optional[int] = None
    hizmet_alim_doktoru: Optional[int] = None
    butce_turu: Optional[str] = None

    class Config:
        orm_mode = True


class PersonelRead(PersonelCreate):
    id: int
    part_time: int
    puan_alabilir: int
    arsiv: int


class PersonelUpdate(BaseModel):
    # İsteğe Bağlı Alanlar (Tüm alanlar güncellenebilir)
    tc_kimlik_no: Optional[int] = None
    sicil_no: Optional[str] = None
    adi: Optional[str] = None
    soyadi: Optional[str] = None
    siralama_kodu: Optional[int] = None
    cinsiyeti: Optional[str] = None
    dogum_tarihi: Optional[date] = None
    kadro_turu: Optional[int] = None
    sinif_id: Optional[int] = None
    unvan_id: Optional[int] = None
    brans_id: Optional[int] = None
    gorev_id: Optional[int] = None
    durum_id: Optional[int] = None
    birim_id: Optional[int] = None
    dis_kurum_id: Optional[int] = None
    part_time: Optional[int] = None
    part_time_tarihi: Optional[date] = None
    otomasyon_kodu: Optional[str] = None
    kisa_unvani: Optional[str] = None
    ise_baslama_tarihi: Optional[date] = None
    memuriyete_giris_tarihi: Optional[date] = None
    asil_memuriyet_tarihi: Optional[date] = None
    sigorta_sicil_no: Optional[str] = None
    emekli_sicil_no: Optional[str] = None
    bagkur_sicil_no: Optional[str] = None
    cocuk_sayisi: Optional[int] = None
    ogrenim_durumu_id: Optional[int] = None
    sendika_id: Optional[int] = None
    ev_adresi1: Optional[str] = None
    ev_adresi2: Optional[str] = None
    ev_posta_kodu: Optional[str] = None
    ev_telefonu: Optional[str] = None
    cep_telefonu: Optional[str] = None
    eposta: Optional[str] = None
    isyeri_adresi1: Optional[str] = None
    isyeri_adresi2: Optional[str] = None
    isyeri_posta_kodu: Optional[str] = None
    isyeri_telefonu: Optional[str] = None
    acil_ulasilacak_kisi: Optional[str] = None
    acil_ulasilacak_tel: Optional[str] = None
    vergi_dairesi: Optional[str] = None
    vergi_no: Optional[str] = None
    baba_adi: Optional[str] = None
    ana_adi: Optional[str] = None
    dogum_yeri: Optional[str] = None
    medeni_hal_kodu: Optional[int] = None
    kimlik_kart_seri: Optional[str] = None
    kimlik_kart_no: Optional[str] = None
    kimlik_il_id: Optional[int] = None
    kimlik_ilce_id: Optional[int] = None
    kimlik_mahalle: Optional[str] = None
    kimlik_cilt_no: Optional[str] = None
    kimlik_aile_sira_no: Optional[str] = None
    kimlik_sira_no: Optional[str] = None
    kimlik_verildigi_yer: Optional[str] = None
    kimlik_verilis_nedeni: Optional[str] = None
    kimlik_verilis_tarihi: Optional[date] = None
    kimlik_kayit_no: Optional[str] = None
    onceki_soyadi: Optional[str] = None
    kan_grubu_id: Optional[int] = None
    askere_gidis_tarihi: Optional[date] = None
    askerden_donus_tarihi: Optional[date] = None
    askerlik_degerlendirmesi: Optional[int] = None
    banka_id: Optional[int] = None
    banka_hesap_no: Optional[str] = None
    cikis_tarihi: Optional[date] = None
    cikis_turu_id: Optional[int] = None
    cikis_aciklama: Optional[str] = None
    cikis_atama_tarihi: Optional[date] = None
    cikis_tebliğ_tarihi: Optional[date] = None
    cikis_atama_yeri: Optional[str] = None
    diploma_no: Optional[str] = None
    diploma_tescil_no: Optional[str] = None
    diploma_tescil_tarihi: Optional[date] = None
    kidem_yili_dusulen: Optional[int] = None
    kidem_yili_ssk: Optional[int] = None
    resim_blob_id: Optional[int] = None
    puan_alabilir: Optional[int] = None
    arsiv: Optional[int] = None
    kurum_gorev_id: Optional[int] = None
    kadro_unvan_tarihi: Optional[date] = None
    asistanlik_tarihi: Optional[date] = None
    bas_asistanlik_tarihi: Optional[date] = None
    uzmanlik_tarihi: Optional[date] = None
    sef_yardimcisi_tarihi: Optional[date] = None
    sef_tarihi: Optional[date] = None
    baba_soyadi: Optional[str] = None
    temp_diploma_tescil_no: Optional[int] = None
    adi_soyadi: Optional[str] = None
    bildigi_diller: Optional[str] = None
    web_parolasi: Optional[str] = None
    docentlik_tarihi: Optional[date] = None
    temp_master_flg: Optional[int] = None
    kalite_bolumu_id: Optional[int] = None
    gizli: Optional[int] = None
    donus_tarihi: Optional[date] = None
    giden_gelen: Optional[int] = None
    sw_engelle: Optional[int] = None
    birlestirildi: Optional[int] = None
    master_flg: Optional[int] = None
    ikamet_il_id: Optional[int] = None
    ikamet_ilce_id: Optional[int] = None
    uyrug_kodu: Optional[str] = None
    nvi_onayli: Optional[int] = None
    arsiv_no: Optional[int] = None
    iban_no: Optional[str] = None
    iban_no2: Optional[str] = None
    ek_banka_id: Optional[int] = None
    ek_banka_hesap_no: Optional[str] = None
    banka_sube_no: Optional[str] = None
    banka_sube_no2: Optional[str] = None
    mazeret_durum_id: Optional[int] = None
    kimlik_il_aktarma: Optional[str] = None
    kimlik_ilce_aktarma: Optional[str] = None
    cihaz_ariza_gorunsun: Optional[int] = None
    sendika_giris_tarihi: Optional[date] = None
    sendika_cikis_tarihi: Optional[date] = None
    mezun_oldugu_okul: Optional[str] = None
    dosya_no: Optional[int] = None
    sakatlik_dercesi: Optional[int] = None
    ev_mahalle: Optional[str] = None
    ev_mahalle_kodu: Optional[str] = None
    ev_adres_no: Optional[str] = None
    nobet_saat: Optional[float] = None
    aktarma_numarasi: Optional[str] = None
    asalet_durumu: Optional[int] = None
    mezuniyet_tarihi: Optional[date] = None
    geldigi_yer: Optional[str] = None
    askerlik_durumu: Optional[int] = None
    askerlik_tecil_tarihi: Optional[date] = None
    sendika_no: Optional[str] = None
    kidem_tarihi: Optional[date] = None
    calisma_planinda_goster: Optional[int] = None
    asil_onay_no: Optional[str] = None
    saramatik_resim_goster: Optional[int] = None
    skrs_doktor_bulunamadi: Optional[int] = None
    maas_terfi_tarihi: Optional[date] = None
    bashekim_onayi: Optional[int] = None
    terfi_durdur: Optional[int] = None
    emekli_terfi_tarihi: Optional[date] = None
    tmp_tc_kimlik_no: Optional[str] = None
    olum_tarihi: Optional[date] = None
    kart_no: Optional[str] = None
    grup_id: Optional[int] = None
    erecete_eimza: Optional[int] = None
    ihtisas_baslama_tarihi: Optional[date] = None
    ihtisas_bitis_tarihi: Optional[date] = None
    ilgi_alani: Optional[str] = None
    asistanlik_bitis_tarihi: Optional[date] = None
    asistanlik_aciklama: Optional[str] = None
    isyeri_telefonu_dahili: Optional[str] = None
    izin_aciklama: Optional[str] = None
    izin_engelle: Optional[int] = None
    nobet_muaf: Optional[int] = None
    nobet_muaf_aciklama: Optional[str] = None
    profesor_tarihi: Optional[date] = None
    aciga_alinma_tarihi: Optional[date] = None
    durum_aciklama: Optional[str] = None
    resim_dosya_yolu: Optional[str] = None
    eimza_baslangic_tarihi: Optional[date] = None
    eimza_bitis_tarihi: Optional[date] = None
    pdks_kart_no: Optional[str] = None
    pdks_kart_pin: Optional[int] = None
    banka_ekno: Optional[int] = None
    banka_ekno2: Optional[int] = None
    arsiv_kk: Optional[int] = None
    arsiv_kts: Optional[date] = None
    arac_marka: Optional[int] = None
    arac_model: Optional[int] = None
    arac_yakit: Optional[int] = None
    arac_renk: Optional[int] = None
    arac_marka2: Optional[int] = None
    arac_model2: Optional[int] = None
    arac_yakit2: Optional[int] = None
    arac_renk2: Optional[int] = None
    arac_plaka: Optional[str] = None
    arac_plaka2: Optional[str] = None
    gecis_tarihi_4d: Optional[date] = None
    aylik_hak_tarihi: Optional[date] = None
    erapor_bashekim_onayi: Optional[int] = None
    ozgecmis: Optional[str] = None
    engelli_kisi: Optional[int] = None
    ozur_orani: Optional[int] = None
    kurumdisi_ekodeme: Optional[int] = None
    ilk_sigorta_tarihi: Optional[date] = None
    hemsirelik_yapabilir: Optional[int] = None
    kurumsal_eposta: Optional[str] = None
    gecis_tarihi_sbu: Optional[date] = None
    onay_tarihi_sbu: Optional[date] = None
    vekalet_baslama_tarihi: Optional[date] = None
    kurum_brans_id: Optional[int] = None
    gunluk_mesai_saati: Optional[float] = None
    fides_durumu: Optional[int] = None
    fides_gonderim_zamani: Optional[date] = None
    fides_gonderim_kk: Optional[int] = None
    fides_grubu: Optional[int] = None
    fides_gonderme: Optional[int] = None
    misafir_doktor: Optional[int] = None
    iskurdan_gelen: Optional[int] = None
    webde_goster: Optional[int] = None
    firma_id: Optional[int] = None
    calisma_sistemi: Optional[int] = None
    dk: Optional[int] = None
    dts: Optional[date] = None
    hekim_medula_sifresi: Optional[str] = None
    terfi_tarihi: Optional[date] = None
    devlet_hizmet_yukumluluk_kodu: Optional[int] = None
    kadro_unvan_id: Optional[int] = None
    imza_unvan_id: Optional[int] = None
    adres_tipi: Optional[int] = None
    adres_kodu_seviyesi: Optional[int] = None
    kadrolu_gorev_yeri: Optional[str] = None
    izin_baslangic_tarihi_4d: Optional[date] = None
    emekli_olacagi_tarih: Optional[date] = None
    lios_kullanici: Optional[str] = None
    lios_sifre: Optional[str] = None
    bagli_birim_id: Optional[int] = None
    skrs_brans_id: Optional[int] = None
    hizmet_alim_doktoru: Optional[int] = None
    butce_turu: Optional[str] = None

    class Config:
        orm_mode = True


class PersonelIzinDetayCreate(BaseModel):
    tarihi: date
    personel_id: int
    turu: int
    izin_turu_id: int
    personel_izin_id: Optional[int] = None
    personel_rotasyon_id: Optional[int] = None
    mhrs_istisna_id: Optional[int] = None

    class Config:
        orm_mode = True  # ORM modeliyle uyumlu hale getirir.


class PersonelGorevCreate(BaseModel):
    adi: str
    sinif_id: int
    ozel_isyeri_olabilir: Optional[int] = 0
    oncekilik: Optional[int] = None
    tg_yuzde: Optional[int] = None
    unvan_kodu: Optional[int] = None
    grup_id: Optional[int] = None
    bakanlik_kodu: Optional[str] = None
    aktif: Optional[int] = None
    derece_araligi: Optional[str] = None
    eobs_kodu: Optional[int] = None
    doktor: Optional[int] = None
    kisa_kodu: Optional[str] = None
    meslek_kodu: Optional[str] = None

    class Config:
        orm_mode = True


class PersonelGorevRead(PersonelGorevCreate):
    id: int


class PersonelGorevUpdate(BaseModel):
    adi: Optional[str] = None
    sinif_id: Optional[int] = None
    ozel_isyeri_olabilir: Optional[int] = None
    oncekilik: Optional[int] = None
    tg_yuzde: Optional[int] = None
    unvan_kodu: Optional[int] = None
    grup_id: Optional[int] = None
    bakanlik_kodu: Optional[str] = None
    aktif: Optional[int] = None
    derece_araligi: Optional[str] = None
    eobs_kodu: Optional[int] = None
    doktor: Optional[int] = None
    kisa_kodu: Optional[str] = None
    meslek_kodu: Optional[str] = None

    class Config:
        orm_mode = True
