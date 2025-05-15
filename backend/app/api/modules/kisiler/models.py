# models.py

from datetime import date, datetime
from typing import Optional, List

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from app.api.modules.kisiler.fields import KisiFields


# models.py


class OrganizasyonBirim(SQLModel, table=True):
    __tablename__ = "ORGANIZASYON_BIRIMI"
    __table_args__ = {"schema": "MGP"}

    BIRIM_NO: int = Field(primary_key=True)
    BAGIMLI_BIRIM: Optional[int] = Field(default=None, foreign_key="MGP.ORGANIZASYON_BIRIMI.BIRIM_NO")
    KISA_KOD: Optional[str] = Field(default=None, max_length=5)
    ADI: Optional[str] = Field(default=None, max_length=25)
    KIMLIK_NO: Optional[int] = Field(default=None, foreign_key="MGP.KISI.KIMLIK_NO")
    IPTAL_T: Optional[date] = None
    IPTAL_NEDENI: Optional[str] = Field(default=None, max_length=4000)
    CESIDI: Optional[str] = Field(default=None, max_length=1)
    GIZLI: Optional[int] = Field(default=None, ge=0, le=1)
    AKTIF: Optional[int] = Field(default=None, ge=0, le=1)

    # Audit Alanları
    EKLEYEN_KULLANICI_KIMLIK_NO: Optional[int] = Field(default=None)
    ENSONGUNCELLEYEN_KULLANICI_KIMLIK_NO: Optional[int] = Field(default=None)
    EKLENME_ZAMANI: Optional[datetime] = None
    ENSON_GUNCELLENME_ZAMANI: Optional[datetime] = None
    MAC_ADDRESS: Optional[str] = Field(default=None, max_length=48)
    GUNCELLEYEN_MAC_ADDRESS: Optional[str] = Field(default=None, max_length=48)

    # Self-referans ilişki (Parent-Child)
    ust_birim: Optional["OrganizasyonBirim"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "OrganizasyonBirim.BAGIMLI_BIRIM",
            "remote_side": "OrganizasyonBirim.BIRIM_NO",
            "uselist": False,
            "viewonly": False,
        }
    )

    alt_birimler: List["OrganizasyonBirim"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "OrganizasyonBirim.BAGIMLI_BIRIM",
            "primaryjoin": "OrganizasyonBirim.BAGIMLI_BIRIM == OrganizasyonBirim.BIRIM_NO",
            "uselist": True,
            "viewonly": False,
        },
        back_populates="ust_birim"
    )

    # OrganizasyonBirim'e ekle:
    personeller: List["Kisi"] = Relationship(
        back_populates="birim",
        sa_relationship_kwargs={
            "foreign_keys": "Kisi.BIRIM_NO",
            "primaryjoin": "OrganizasyonBirim.BIRIM_NO == Kisi.BIRIM_NO"
        }
    )

    gorevdeki_kisiler: List["Kisi"] = Relationship(
        back_populates="gorev_birimi",
        sa_relationship_kwargs={
            "foreign_keys": "Kisi.GOREV_KODU",
            "primaryjoin": "OrganizasyonBirim.BIRIM_NO == Kisi.GOREV_KODU"
        }
    )


class Kisi(KisiFields, SQLModel, table=True):
    __tablename__ = "KISI"
    __table_args__ = {"schema": "MGP"}

    KIMLIK_NO: int = Field(primary_key=True)

    # İlişkiler
    birim: Optional["OrganizasyonBirim"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "Kisi.BIRIM_NO",
            "primaryjoin": "Kisi.BIRIM_NO == OrganizasyonBirim.BIRIM_NO",
        },
        back_populates="personeller"
    )

    gorev_birimi: Optional["OrganizasyonBirim"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "Kisi.GOREV_KODU",
            "primaryjoin": "Kisi.GOREV_KODU == OrganizasyonBirim.BIRIM_NO",
        },
        back_populates="gorevdeki_kisiler"
    )


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
    # fides_gonder: Optional[int] = Field(default=None, nullable=True)
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
    # fides_gonder: Optional[int] = Field(default=None, nullable=True)
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
