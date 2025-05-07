from typing import Optional

from pydantic import BaseModel


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
