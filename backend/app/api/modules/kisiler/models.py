# models.py

from datetime import date, datetime
from typing import Optional, List

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
