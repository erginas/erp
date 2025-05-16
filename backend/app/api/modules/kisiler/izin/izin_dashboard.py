from datetime import date, timedelta
from typing import Optional

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


@router.get("/tum-izinliler")
def tum_izinli_personeller(
        baslangic: Optional[date] = None,
        bitis: Optional[date] = None,
        db: Session = Depends(get_db)
):
    today = date.today()
    bas = baslangic or today
    bit = bitis or today

    result = db.query(
        Kisi.ADI,
        Kisi.SOYADI,
        PersonelIzin.baslama_tarihi,
        PersonelIzin.donus_tarihi,
        OrganizasyonBirim.ADI.label("birim"),
        Kisi.ID.label("kimlikNo")
    ).join(PersonelIzin, Kisi.ID == PersonelIzin.personel_id
           ).join(OrganizasyonBirim, Kisi.BIRIM_NO == OrganizasyonBirim.BIRIM_NO
                  ).filter(
        PersonelIzin.baslama_tarihi <= bit,
        PersonelIzin.donus_tarihi >= bas
    ).all()

    return [
        {
            "adi": row.ADI,
            "soyadi": row.SOYADI,
            "baslama_tarihi": row.baslama_tarihi,
            "donus_tarihi": row.donus_tarihi,
            "birim": row.birim,
            "kimlikNo": row.kimlikNo
        } for row in result
    ]


@router.get("/ozet/{kimlik_no}")
def izin_ozet(kimlik_no: int, db: Session = Depends(get_db)):
    result = db.query(
        PersonelIzin.yili,
        func.sum(PersonelIzin.plan_izin).label("toplam_hak"),
        func.sum(PersonelIzin.suresi).label("kullanilan")
    ).filter(
        PersonelIzin.personel_id == kimlik_no,
        PersonelIzin.onay == 1  # sadece onaylı izinleri dikkate al
    ).group_by(PersonelIzin.yili).order_by(PersonelIzin.yili.desc()).all()

    return [
        {
            "yil": row.yili,
            "hak": row.toplam_hak,
            "kullanilan": row.kullanilan,
            "kalan": (row.toplam_hak or 0) - (row.kullanilan or 0)
        }
        for row in result
    ]


@router.get("/gunluk-giris-cikis/{kimlik_no}")
def pdks_giris_cikis(
        kimlik_no: int,
        start: Optional[date] = None,
        end: Optional[date] = None,
        db: Session = Depends(get_db)
):
    today = date.today()
    start_date = start or today - timedelta(days=14)
    end_date = end or today

    # PDKS kayıtları örnek tablo: PDKS_KAYIT (personel_id, tarih, giris, cikis)
    result = db.query(
        PdksKayit.tarih,
        PdksKayit.giris,
        PdksKayit.cikis
    ).filter(
        PdksKayit.personel_id == kimlik_no,
        PdksKayit.tarih.between(start_date, end_date)
    ).order_by(PdksKayit.tarih.desc()).all()

    return [
        {
            "tarih": r.tarih,
            "giris": r.giris.strftime("%H:%M") if r.giris else None,
            "cikis": r.cikis.strftime("%H:%M") if r.cikis else None
        } for r in result
    ]
