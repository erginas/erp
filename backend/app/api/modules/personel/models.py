from datetime import date, datetime
from typing import Optional, List

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


class Personel(SQLModel, table=True):
    __tablename__ = "PERSONEL"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    adi: str = Field(max_length=30, nullable=False)
    soyadi: str = Field(max_length=50, nullable=False)
    tc_kimlik_no: Optional[int] = Field(default=None, nullable=True)
    sicil_no: Optional[str] = Field(max_length=20, nullable=True)
    siralama_kodu: Optional[int] = Field(default=None, nullable=True)
    cinsiyeti: Optional[str] = Field(max_length=1, nullable=True)
    dogum_tarihi: Optional[date] = Field(default=None, nullable=True)
    kadro_turu: Optional[int] = Field(default=None, nullable=True)
    sinif_id: Optional[int] = Field(default=None, nullable=True)
    unvan_id: Optional[int] = Field(default=None, nullable=True)
    brans_id: Optional[int] = Field(default=None, nullable=True)
    gorev_id: Optional[int] = Field(default=None, nullable=True)
    durum_id: Optional[int] = Field(default=None, nullable=True)
    birim_id: Optional[int] = Field(default=None, nullable=True)
    dis_kurum_id: Optional[int] = Field(default=None, nullable=True)

    # İsteğe Bağlı Alanlar
    part_time: int = Field(default=0, nullable=False)  # Default değeri 0 olan zorunlu alan
    part_time_tarihi: Optional[date] = Field(default=None, nullable=True)
    otomasyon_kodu: Optional[str] = Field(max_length=15, nullable=True)
    kisa_unvani: Optional[str] = Field(max_length=15, nullable=True)
    ise_baslama_tarihi: Optional[date] = Field(default=None, nullable=True)
    memuriyete_giris_tarihi: Optional[date] = Field(default=None, nullable=True)
    asil_memuriyet_tarihi: Optional[date] = Field(default=None, nullable=True)
    sigorta_sicil_no: Optional[str] = Field(max_length=16, nullable=True)
    emekli_sicil_no: Optional[str] = Field(max_length=16, nullable=True)
    bagkur_sicil_no: Optional[str] = Field(max_length=20, nullable=True)

    # Diğer Alanlar (Tümü İsteğe Bağlı)
    kidem_terfi_gunu: Optional[int] = Field(default=None, nullable=True)
    kidem_terfi_ayi: Optional[int] = Field(default=None, nullable=True)
    maas_terfi_gunu: Optional[int] = Field(default=None, nullable=True)
    maas_terfi_ayi: Optional[int] = Field(default=None, nullable=True)
    emekli_terfi_gunu: Optional[int] = Field(default=None, nullable=True)
    emekli_terfi_ayi: Optional[int] = Field(default=None, nullable=True)
    cocuk_sayisi: Optional[int] = Field(default=None, nullable=True)
    ogrenim_durumu_id: Optional[int] = Field(default=None, nullable=True)
    sendika_id: Optional[int] = Field(default=None, nullable=True)
    ev_adresi1: Optional[str] = Field(max_length=512, nullable=True)
    ev_adresi2: Optional[str] = Field(max_length=64, nullable=True)
    ev_posta_kodu: Optional[str] = Field(max_length=6, nullable=True)
    ev_telefonu: Optional[str] = Field(max_length=64, nullable=True)
    cep_telefonu: Optional[str] = Field(max_length=20, nullable=True)
    eposta: Optional[str] = Field(max_length=40, nullable=True)
    isyeri_adresi1: Optional[str] = Field(max_length=100, nullable=True)
    isyeri_adresi2: Optional[str] = Field(max_length=100, nullable=True)
    isyeri_posta_kodu: Optional[str] = Field(max_length=5, nullable=True)
    isyeri_telefonu: Optional[str] = Field(max_length=20, nullable=True)
    acil_ulasilacak_kisi: Optional[str] = Field(max_length=128, nullable=True)
    acil_ulasilacak_tel: Optional[str] = Field(max_length=20, nullable=True)
    vergi_dairesi: Optional[str] = Field(max_length=40, nullable=True)
    vergi_no: Optional[str] = Field(max_length=15, nullable=True)
    baba_adi: Optional[str] = Field(max_length=30, nullable=True)
    ana_adi: Optional[str] = Field(max_length=30, nullable=True)
    dogum_yeri: Optional[str] = Field(max_length=20, nullable=True)
    medeni_hal_kodu: Optional[int] = Field(default=None, nullable=True)
    kimlik_kart_seri: Optional[str] = Field(max_length=3, nullable=True)
    kimlik_kart_no: Optional[str] = Field(max_length=12, nullable=True)
    kimlik_il_id: Optional[int] = Field(default=None, nullable=True)
    kimlik_ilce_id: Optional[int] = Field(default=None, nullable=True)
    kimlik_mahalle: Optional[str] = Field(max_length=30, nullable=True)
    kimlik_cilt_no: Optional[str] = Field(max_length=10, nullable=True)
    kimlik_aile_sira_no: Optional[str] = Field(max_length=10, nullable=True)
    kimlik_sira_no: Optional[str] = Field(max_length=10, nullable=True)
    kimlik_verildigi_yer: Optional[str] = Field(max_length=16, nullable=True)
    kimlik_verilis_nedeni: Optional[str] = Field(max_length=16, nullable=True)
    kimlik_verilis_tarihi: Optional[date] = Field(default=None, nullable=True)
    kimlik_kayit_no: Optional[str] = Field(max_length=10, nullable=True)
    onceki_soyadi: Optional[str] = Field(max_length=24, nullable=True)
    kan_grubu_id: Optional[int] = Field(default=None, nullable=True)
    askere_gidis_tarihi: Optional[date] = Field(default=None, nullable=True)
    askerden_donus_tarihi: Optional[date] = Field(default=None, nullable=True)
    askerlik_degerlendirmesi: Optional[int] = Field(default=None, nullable=True)
    banka_id: Optional[int] = Field(default=None, nullable=True)
    banka_hesap_no: Optional[str] = Field(max_length=35, nullable=True)
    cikis_tarihi: Optional[date] = Field(default=None, nullable=True)
    cikis_turu_id: Optional[int] = Field(default=None, nullable=True)
    cikis_aciklama: Optional[str] = Field(max_length=80, nullable=True)
    cikis_atama_tarihi: Optional[date] = Field(default=None, nullable=True)
    cikis_teblig_tarihi: Optional[date] = Field(default=None, nullable=True)
    cikis_atama_yeri: Optional[str] = Field(max_length=250, nullable=True)
    diploma_no: Optional[str] = Field(max_length=16, nullable=True)
    diploma_tescil_no: Optional[str] = Field(max_length=16, nullable=True)
    diploma_tescil_tarihi: Optional[date] = Field(default=None, nullable=True)
    kidem_yili_dusulen: Optional[int] = Field(default=None, nullable=True)
    kidem_yili_ssk: Optional[int] = Field(default=None, nullable=True)
    resim_blob_id: Optional[int] = Field(default=None, nullable=True)
    puan_alabilir: int = Field(default=1, nullable=False)  # Default değeri 1 olan zorunlu alan
    kk: int = Field(default=None, nullable=False)
    kts: Optional[datetime] = Field(default_factory=datetime.utcnow, nullable=False)
    arsiv: int = Field(default=0, nullable=False)  # Default değeri 0 olan zorunlu alan


class PersonelGorev(SQLModel, table=True):
    __tablename__ = "PERSONEL_GOREV"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    adi: str = Field(max_length=128, nullable=False)
    sinif_id: int = Field(nullable=False)

    # İsteğe Bağlı Alanlar
    ozel_isyeri_olabilir: int = Field(default=0, nullable=False)
    oncekilik: Optional[int] = Field(default=None, nullable=True)
    tg_yuzde: Optional[int] = Field(default=None, nullable=True)
    unvan_kodu: Optional[int] = Field(default=None, nullable=True)
    grup_id: Optional[int] = Field(default=None, nullable=True)
    bakanlik_kodu: Optional[str] = Field(max_length=32, nullable=True)
    aktif: Optional[int] = Field(default=None, nullable=True)
    derece_araligi: Optional[str] = Field(max_length=16, nullable=True)
    eobs_kodu: Optional[int] = Field(default=None, nullable=True)
    doktor: Optional[int] = Field(default=None, nullable=True)
    kisa_kodu: Optional[str] = Field(max_length=32, nullable=True)
    meslek_kodu: Optional[str] = Field(max_length=16, nullable=True)


from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field


class PersonelIzin(SQLModel, table=True):
    __tablename__ = "PERSONEL_IZIN"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    personel_id: int = Field(nullable=False)
    yili: int = Field(nullable=False)
    tur_id: int = Field(nullable=False)
    plan_izin: int = Field(nullable=False)
    baslama_tarihi: date = Field(nullable=False)
    suresi: int = Field(nullable=False)
    yol: int = Field(nullable=False)

    # İsteğe Bağlı Alanlar
    donus_tarihi: Optional[date] = Field(default=None, nullable=True)
    aciklama: Optional[str] = Field(max_length=512, nullable=True)
    adresi: Optional[str] = Field(max_length=60, nullable=True)
    kk: int = Field(default=None, nullable=False)
    sayi: Optional[int] = Field(default=None, nullable=True)
    kts: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    hbys_engelle: int = Field(default=0, nullable=False)
    ukk: Optional[int] = Field(default=None, nullable=True)
    ukts: Optional[datetime] = Field(default=None, nullable=True)
    ait_oldugu_yil: Optional[int] = Field(default=None, nullable=True)
    ait_oldugu_yil_detay: Optional[str] = Field(max_length=256, nullable=True)
    vekil_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza1_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza2_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza3_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza4_personel_id: Optional[int] = Field(default=None, nullable=True)
    tatil_gunu: Optional[int] = Field(default=None, nullable=True)
    teslim_edildi: Optional[int] = Field(default=None, nullable=True)
    onay: Optional[int] = Field(default=None, nullable=True)
    onay_kk: Optional[int] = Field(default=None, nullable=True)
    onay_kts: Optional[datetime] = Field(default=None, nullable=True)
    resmi_tatil: Optional[int] = Field(default=None, nullable=True)
    isci_tatil_haric: Optional[int] = Field(default=None, nullable=True)
    izin_aciklama: Optional[str] = Field(max_length=2048, nullable=True)
    cinsiyet: Optional[int] = Field(default=None, nullable=True)
    fides_gonderim_zamani: Optional[datetime] = Field(default=None, nullable=True)
    sgk_bildirildi: Optional[int] = Field(default=None, nullable=True)
    sgk_bildirilme_kts: Optional[datetime] = Field(default=None, nullable=True)
    sgk_bildirilme_kk: Optional[int] = Field(default=None, nullable=True)
    fides_gonder: Optional[int] = Field(default=None, nullable=True)
    dk: Optional[float] = Field(default=None, nullable=True)
    dts: Optional[datetime] = Field(default=None, nullable=True)
    maas_teslim_edildi: Optional[int] = Field(default=None, nullable=True)
    gizli: Optional[int] = Field(default=None, nullable=True)
    rapor_kurum_id: Optional[int] = Field(default=None, nullable=True)


class PersonelIzinDetay(SQLModel, table=True):
    __tablename__ = "PERSONEL_IZIN_DETAY"
    __table_args__ = (
        UniqueConstraint("tarihi", "personel_id", "turu", "izin_turu_id", name="PK_PERSONEL_IZIN_DETAY"),
        {"schema": "MGP"}  # Oracle şema adı
    )

    # Primary Key Alanları (Composite Key)
    tarihi: date = Field(nullable=False, primary_key=True)
    personel_id: int = Field(nullable=False, primary_key=True)
    turu: int = Field(nullable=False, primary_key=True)
    izin_turu_id: int = Field(nullable=False, primary_key=True)

    # İsteğe Bağlı Alanlar
    personel_izin_id: Optional[int] = Field(default=None, nullable=True)
    personel_rotasyon_id: Optional[int] = Field(default=None, nullable=True)
    mhrs_istisna_id: Optional[int] = Field(default=None, nullable=True)


class PersonelIzinIptal(SQLModel, table=True):
    __tablename__ = "PERSONEL_IZIN_IPTAL"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    personel_id: int = Field(nullable=False)
    yili: int = Field(nullable=False)
    tur_id: int = Field(nullable=False)
    plan_izin: int = Field(nullable=False)
    baslama_tarihi: date = Field(nullable=False)
    suresi: int = Field(nullable=False)
    yol: int = Field(nullable=False)

    # İsteğe Bağlı Alanlar
    donus_tarihi: Optional[date] = Field(default=None, nullable=True)
    aciklama: Optional[str] = Field(max_length=2048, nullable=True)
    adresi: Optional[str] = Field(max_length=60, nullable=True)
    kk: int = Field(nullable=False)
    kts: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    mgp_engelle: Optional[int] = Field(default=None, nullable=True)
    ait_oldugu_yil: Optional[int] = Field(default=None, nullable=True)
    ait_oldugu_yil_detay: Optional[str] = Field(max_length=256, nullable=True)
    vekil_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza1_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza2_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza3_personel_id: Optional[int] = Field(default=None, nullable=True)
    imza4_personel_id: Optional[int] = Field(default=None, nullable=True)
    cinsiyet: Optional[int] = Field(default=None, nullable=True)
    izin_aciklama: Optional[str] = Field(max_length=2048, nullable=True)
    onay_kk: Optional[int] = Field(default=None, nullable=True)
    onay_kts: Optional[datetime] = Field(default=None, nullable=True)
    onay: Optional[int] = Field(default=None, nullable=True)
    bitis_tarihi: Optional[date] = Field(default=None, nullable=True)


# izin Turu

class PersonelIzinTuru(SQLModel, table=True):
    __tablename__ = "PERSONEL_IZIN_TURU"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    adi: str = Field(max_length=20, nullable=False)
    tipi: str = Field(max_length=1, nullable=False)
    ucretlimi: str = Field(max_length=1, nullable=False)

    # İsteğe Bağlı Alanlar
    min_suresi: Optional[int] = Field(default=None, nullable=True)
    max_suresi: Optional[int] = Field(default=None, nullable=True)
    aciklama: Optional[str] = Field(max_length=40, nullable=True)
    kk: int = Field(nullable=False)
    saatlik: int = Field(default=0, nullable=False)
    turu: Optional[str] = Field(max_length=32, nullable=True)
    ay_max_suresi: Optional[int] = Field(default=None, nullable=True)
    engelle: Optional[int] = Field(default=None, nullable=True)
    aksiyon_kodu: Optional[str] = Field(max_length=32, nullable=True)
    terfi_durdur: Optional[int] = Field(default=None, nullable=True)
    haric: Optional[int] = Field(default=None, nullable=True)
    ay_max_adedi: Optional[int] = Field(default=None, nullable=True)
    sms_gonder: Optional[int] = Field(default=None, nullable=True)
    cinsiyet_zorunlu: Optional[int] = Field(default=None, nullable=True)
    nobet_turu: Optional[int] = Field(default=None, nullable=True)
    sgk_zorunlu: Optional[int] = Field(default=None, nullable=True)
    tatil_gunu: Optional[int] = Field(default=None, nullable=True)
    fides_gonder: Optional[int] = Field(default=None, nullable=True)
    yillik_max_adet: Optional[int] = Field(default=None, nullable=True)
    calisma_listesi_dahil: Optional[int] = Field(default=None, nullable=True)


# Personel Unvan
class PersonelUnvan(SQLModel, table=True):
    __tablename__ = "PERSONEL_UNVAN"
    __table_args__ = {"schema": "MGP"}

    # Primary Key
    id: int = Field(default=None, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    adi: str = Field(max_length=128, nullable=False)
    oncelik_no: int = Field(nullable=False)
    kk: int = Field(nullable=False)

    # İsteğe Bağlı Alanlar
    standart_adet: Optional[int] = Field(default=None, nullable=True)
    mevcut_adet: Optional[int] = Field(default=None, nullable=True)
    bakanlik_kodu: Optional[str] = Field(max_length=32, nullable=True)
    aktif: Optional[int] = Field(default=None, nullable=True)


# tatil günleri

class TatilGunleri(SQLModel, table=True):
    __tablename__ = "TATIL_GUNLERI"
    __table_args__ = (
        UniqueConstraint("ilk_tarih", "adi", name="PK_TATIL_GUNLERI"),
        {"schema": "MGP"}  # Oracle şema adı
    )

    # Primary Key Alanları (Composite Key)
    ilk_tarih: date = Field(nullable=False, primary_key=True)
    adi: str = Field(max_length=128, nullable=False, primary_key=True)

    # Zorunlu Alanlar
    tipi: int = Field(nullable=False)

    # İsteğe Bağlı Alanlar
    nobet_haric: Optional[int] = Field(default=None, nullable=True)


# organizasyon birimi
class OrganizasyonBirimi(SQLModel, table=True):
    __tablename__ = "ORGANIZASYON_BIRIMI"

    # Anahtarlar ve Zorunlu Alanlar
    birim_no: int = Field(default=None, primary_key=True, nullable=False)
    bagimli_birim: Optional[int] = Field(default=None, foreign_key="ORGANIZASYON_BIRIMI.birim_no")
    kisa_kod: Optional[str] = Field(default=None, max_length=5)
    adi: str = Field(max_length=25)
    kimlik_no: Optional[int] = Field(default=None)

    # Diğer Alanlar
    iptal_t: Optional[date] = Field(default=None)
    iptal_nedeni: Optional[str] = Field(default=None, max_length=4000)
    cesidi: Optional[str] = Field(default=None, max_length=1)
    gizli: Optional[int] = Field(default=None)
    aktif: Optional[int] = Field(default=None)
    ekleyen_kullanici_kimlik_no: Optional[int] = Field(default=None)
    ensonguncelleyen_kullanici_kimlik_no: Optional[int] = Field(default=None)
    eklenme_zamani: Optional[datetime] = Field(default=None)
    enson_guncellenme_zamani: Optional[datetime] = Field(default=None)
    mac_address: Optional[str] = Field(default=None, max_length=48)
    guncelleyen_mac_address: Optional[str] = Field(default=None, max_length=48)

    # İlişkiler
    bagimli_birim_ilişki: Optional["OrganizasyonBirimi"] = Relationship(
        back_populates="alt_birimler",
        sa_relationship_kwargs={"remote_side": "OrganizasyonBirimi.birim_no"}
    )
    alt_birimler: List["OrganizasyonBirimi"] = Relationship(
        back_populates="bagimli_birim_ilişki",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
