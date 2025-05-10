# fields.py

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field as SQLField


class AuditFields:
    EKLEYEN_KULLANICI_KIMLIK_NO: Optional[int] = SQLField(default=None)
    ENSONGUNCELLEYEN_KULLANICI_KIMLIK_NO: Optional[int] = SQLField(default=None)
    EKLENME_ZAMANI: Optional[datetime] = None
    ENSON_GUNCELLENME_ZAMANI: Optional[datetime] = None
    MAC_ADDRESS: Optional[str] = SQLField(default=None, max_length=48)
    GUNCELLEYEN_MAC_ADDRESS: Optional[str] = SQLField(default=None, max_length=48)


class KisiFields(AuditFields):
    ADI: Optional[str] = SQLField(default=None, max_length=80)
    SOYADI: Optional[str] = SQLField(default=None, max_length=80)
    BABA_ADI: Optional[str] = SQLField(default=None, max_length=80)
    ANA_ADI: Optional[str] = SQLField(default=None, max_length=30)
    MESLEGI: Optional[str] = SQLField(default=None, max_length=80)
    DOGUM_YERI: Optional[str] = SQLField(default=None, max_length=80)
    DOGUM_TARIHI: Optional[date] = None
    KAN_GRUBU: Optional[str] = SQLField(default=None, max_length=10)
    CINSIYETI: Optional[str] = SQLField(default=None, max_length=1)
    MEDENI_HALI: Optional[str] = SQLField(default=None, max_length=10)
    EV_TEL: Optional[str] = SQLField(default=None, max_length=50)
    CEP_TEL: Optional[str] = SQLField(default=None, max_length=50)
    IS_TEL: Optional[str] = SQLField(default=None, max_length=50)
    ADRES: Optional[str] = SQLField(default=None, max_length=255)
    SSK_NO: Optional[str] = SQLField(default=None, max_length=30)
    ILGILI_SIRKET: Optional[str] = SQLField(default=None, max_length=5)
    ISE_GIRIS_TARIHI: Optional[date] = None
    ISTEN_CIKIS_T: Optional[date] = None
    VERGI_DAIRESI: Optional[str] = SQLField(default=None, max_length=120)
    VERGI_NO: Optional[str] = SQLField(default=None, max_length=20)
    BIRIM_NO: Optional[int] = SQLField(default=None, foreign_key="ORGANIZASYON_BIRIMI.BIRIM_NO")
    GOREVI: Optional[str] = SQLField(default=None, max_length=80)
    MESAI_FL: Optional[str] = SQLField(default=None, max_length=1)
    ACIKLAMA: Optional[str] = SQLField(default=None, max_length=1024)
    GOREV_KODU: Optional[int] = SQLField(default=None, foreign_key="ORGANIZASYON_BIRIMI.BIRIM_NO")
    EGITIM_DURUMU: Optional[str] = SQLField(default=None, max_length=80)
    TAKMA_AD: Optional[str] = SQLField(default=None, unique=True, max_length=80)
    SIFRE: Optional[str] = SQLField(default=None, max_length=255)
    AYAKKABI_NO: Optional[str] = SQLField(default=None, max_length=10)
    UST_BEDEN: Optional[str] = SQLField(default=None, max_length=10)
    ALT_BEDEN: Optional[str] = SQLField(default=None, max_length=10)
    SIFRESI: Optional[str] = SQLField(default=None, max_length=255)
    KILIT: Optional[int] = None
    ID: Optional[int] = SQLField(default=None)
    PASSWORD: Optional[str] = SQLField(default=None, max_length=128)
    LAST_LOGIN: Optional[datetime] = None
    IS_SUPERUSER: Optional[int] = SQLField(default=None, ge=0, le=1)
    USERNAME: Optional[str] = SQLField(default=None, max_length=150)
    FIRST_NAME: Optional[str] = SQLField(default=None, max_length=150)
    EMAIL: Optional[str] = SQLField(default=None, max_length=250)
    IS_STAFF: Optional[int] = SQLField(default=None, ge=0, le=1)
    IS_ACTIVE: Optional[int] = SQLField(default=None, ge=0, le=1)
    DATE_JOINED: Optional[datetime] = None
    AKTIF: Optional[int] = SQLField(default=None, ge=0, le=1)


class OrganizasyonBirimFields(AuditFields):
    BAGIMLI_BIRIM: Optional[int] = SQLField(default=None, foreign_key="ORGANIZASYON_BIRIMI.BIRIM_NO")
    KISA_KOD: Optional[str] = SQLField(default=None, max_length=5)
    ADI: Optional[str] = SQLField(default=None, max_length=25)
    KIMLIK_NO: Optional[int] = SQLField(default=None, foreign_key="KISI.KIMLIK_NO")
    IPTAL_T: Optional[date] = None
    IPTAL_NEDENI: Optional[str] = SQLField(default=None, max_length=4000)
    CESIDI: Optional[str] = SQLField(default=None, max_length=1)
    GIZLI: Optional[int] = SQLField(default=None, ge=0, le=1)
    AKTIF: Optional[int] = SQLField(default=None, ge=0, le=1)
