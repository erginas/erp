from datetime import date, timedelta

from sqlmodel import Session, select, func

from app.core.moduls.models import PntsKod
from .models import Personel, OrganizasyonBirimi, PersonelIzin


def get_dashboard_data(db: Session):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)

    toplam_personel = db.exec(select(func.count()).select_from(Personel)).one()
    aktif_personel = db.exec(select(func.count()).select_from(Personel).where(Personel.cikis_tarihi == None)).one()
    ayrilan_personel = db.exec(select(func.count()).select_from(Personel).where(Personel.cikis_tarihi != None)).one()

    # Birim adı haritalama
    birim_ad_map = {
        b.birim_no: b.adi for b in db.exec(select(OrganizasyonBirimi.birim_no, OrganizasyonBirimi.adi)).all()
    }

    birim_ids = db.exec(select(Personel.birim_id).distinct()).all()
    birim_personel_sayisi = {}

    for (birim_id) in birim_ids:
        aktif = db.exec(
            select(func.count()).select_from(Personel)
            .where(Personel.birim_id == birim_id, Personel.cikis_tarihi == None)
        ).one()
        ayrilan = db.exec(
            select(func.count()).select_from(Personel)
            .where(Personel.birim_id == birim_id, Personel.cikis_tarihi != None)
        ).one()

        birim_adi = birim_ad_map.get(birim_id, f"Birim {birim_id}")
        birim_personel_sayisi[birim_adi] = {
            "aktif": aktif,
            "ayrilan": ayrilan
        }

    dogum_gunu_olanlar = db.exec(
        select(Personel).where(
            func.extract("month", Personel.dogum_tarihi) == today.month,
            func.extract("day", Personel.dogum_tarihi) == today.day
        )
    ).all()

    emeklilik_adaylari = db.exec(
        select(Personel).where(
            func.extract("year", today) - func.extract("year", Personel.memuriyete_giris_tarihi) >= 29
        )
    ).all()

    bugun_donenler = db.exec(
        select(Personel)
        .select_from(Personel)
        .join(PersonelIzin, Personel.id == PersonelIzin.personel_id)
        .where(PersonelIzin.donus_tarihi == today)
    ).all()

    yarin_donenler = db.exec(
        select(Personel)
        .select_from(Personel)
        .join(PersonelIzin, Personel.id == PersonelIzin.personel_id)
        .where(PersonelIzin.donus_tarihi == tomorrow)
    ).all()

    haftaya_donenler = db.exec(
        select(Personel)
        .select_from(Personel)
        .join(PersonelIzin, Personel.id == PersonelIzin.personel_id)
        .where(PersonelIzin.donus_tarihi == next_week)
    ).all()

    # Kan grubu dağılımı
    kan_grubu_dagilimi = []
    kan_gruplari = db.exec(
        select(PntsKod.kodu, PntsKod.adi).where(PntsKod.turu == "KANGRUBU")
    ).all()
    for kodu, adi in kan_gruplari:
        sayi = db.exec(
            select(func.count()).select_from(Personel)
            .where(Personel.kan_grubu_id == kodu, Personel.cikis_tarihi == None)
        ).one()
        kan_grubu_dagilimi.append({"kan_grubu": adi, "sayi": sayi})

    return {
        "toplam_personel": toplam_personel,
        "aktif_personel": aktif_personel,
        "ayrilan_personel": ayrilan_personel,
        "birim_personel_sayisi": birim_personel_sayisi,
        "dogum_gunu_olanlar": dogum_gunu_olanlar,
        "hatirlatmalar": [{"tur": "Emeklilik", "id": p.id, "ad": p.adi, "soyad": p.soyadi} for p in emeklilik_adaylari],
        "izinden_donenler": {
            "bugun": [{"id": p.id, "adi": p.adi, "soyadi": p.soyadi} for p in bugun_donenler],
            "yarin": [{"id": p.id, "adi": p.adi, "soyadi": p.soyadi} for p in yarin_donenler],
            "haftaya": [{"id": p.id, "adi": p.adi, "soyadi": p.soyadi} for p in haftaya_donenler]
        },
        "kan_grubu_dagilimi": kan_grubu_dagilimi
    }
