from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.modules.kisiler.models import PersonelIzin, OrganizasyonBirim, Kisi

router = APIRouter(prefix="/izin-dashboard", tags=["İzin Dashboard"])


# Bugün izinde olan toplam personel sayısını almak.
@router.get("/toplam-izinli")
def toplam_izinli_personel(db: Session = Depends(get_db)):
    today = date.today()
    total = db.query(PersonelIzin).filter(
        PersonelIzin.baslama_tarihi <= today,
        PersonelIzin.donus_tarihi >= today
    ).count()
    return {"toplam_izinli": total}


# Birim bazlı olarak bugün izinde olan personel sayısını gruplu görmek.
@router.get("/izinli-birim-dagilim")
def izinli_birim_dagilim(db: Session = Depends(get_db)):
    today = date.today()
    result = db.query(
        OrganizasyonBirim.ADI.label("birim_adi"),
        func.count(PersonelIzin.id).label("sayi")
    ).join(Kisi, Kisi.ID == PersonelIzin.personel_id
           ).join(OrganizasyonBirim, OrganizasyonBirim.BIRIM_NO == Kisi.BIRIM_NO
                  ).filter(
        PersonelIzin.baslama_tarihi <= today,
        PersonelIzin.donus_tarihi >= today
    ).group_by(OrganizasyonBirim.ADI).all()

    return [{"birim": row.birim_adi, "sayi": row.sayi} for row in result]


# Seçilen birimdeki tüm izinli personellerin ad, soyad, izin başlangıç/bitiş tarihlerini göstermek.
@router.get("/izinli-detay")
def izinli_personel_detay(birim_adi: str, db: Session = Depends(get_db)):
    today = date.today()
    result = db.query(
        Kisi.ADI,
        Kisi.SOYADI,
        PersonelIzin.baslama_tarihi,
        PersonelIzin.donus_tarihi
    ).join(PersonelIzin, Kisi.ID == PersonelIzin.personel_id
           ).join(OrganizasyonBirim, Kisi.BIRIM_NO == OrganizasyonBirim.BIRIM_NO
                  ).filter(
        OrganizasyonBirim.ADI.ilike(f"%{birim_adi}%"),
        PersonelIzin.baslama_tarihi <= today,
        PersonelIzin.donus_tarihi >= today
    ).all()
    print("benim sql", result)
    return [
        {
            "adi": row.ADI,
            "soyadi": row.SOYADI,
            "baslama_tarihi": row.baslama_tarihi,
            "donus_tarihi": row.donus_tarihi
        } for row in result
    ]
