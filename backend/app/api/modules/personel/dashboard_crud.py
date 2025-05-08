# from datetime import date, timedelta
# from typing import Dict, List, Optional
# from pydantic import BaseModel
# from sqlmodel import Session, select, func, and_
# from sqlalchemy import case
#
# from app.core.moduls.models import PntsKod
# from .models import Personel, OrganizasyonBirimi, PersonelIzin
#
# ## Pydantic Models for Response
# class PersonelBase(BaseModel):
#     id: int
#     adi: str
#     soyadi: str
#
# class BirimPersonelStats(BaseModel):
#     aktif: int
#     ayrilan: int
#
# class KanGrubuDagilimi(BaseModel):
#     kan_grubu: str
#     sayi: int
#
# class IzinDonenler(BaseModel):
#     bugun: List[PersonelBase]
#     yarin: List[PersonelBase]
#     haftaya: List[PersonelBase]
#
# class Hatirlatma(BaseModel):
#     tur: str
#     id: int
#     ad: str
#     soyad: str
#
# class DashboardResponse(BaseModel):
#     toplam_personel: int
#     aktif_personel: int
#     ayrilan_personel: int
#     birim_personel_sayisi: Dict[str, BirimPersonelStats]
#     dogum_gunu_olanlar: List[PersonelBase]
#     hatirlatmalar: List[Hatirlatma]
#     izinden_donenler: IzinDonenler
#     kan_grubu_dagilimi: List[KanGrubuDagilimi]
#
# def get_dashboard_data(db: Session) -> DashboardResponse:
#     """Optimized dashboard data retrieval with SQLModel and Pydantic v2"""
#     today = date.today()
#     tomorrow = today + timedelta(days=1)
#     next_week = today + timedelta(days=7)
#
#     # Corrected case statement syntax
#     personel_stats = db.exec(
#         select(
#             func.count().label("toplam"),
#             func.sum(case((Personel.cikis_tarihi.is_(None), 1), else_=0)).label("aktif"),
#             func.sum(case((Personel.cikis_tarihi.is_not(None), 1), else_=0)).label("ayrilan")
#         )
#     ).one()
#
#     # Get all organizational units in one query and create mapping
#     birim_ad_map = {
#         b.birim_no: b.adi
#         for b in db.exec(
#             select(OrganizasyonBirimi.birim_no, OrganizasyonBirimi.adi)
#         ).all()
#     }
#
#     # Combined query for department-based statistics with corrected case syntax
#     birim_personel_sayisi = db.exec(
#         select(
#             Personel.birim_id,
#             func.sum(case((Personel.cikis_tarihi.is_(None), 1), else_=0)).label("aktif"),
#             func.sum(case((Personel.cikis_tarihi.is_not(None), 1), else_=0)).label("ayrilan")
#         ).group_by(Personel.birim_id)
#     ).all()
#
#     # Process department data with mapping
#     birim_personel_sayisi_dict = {
#         birim_ad_map.get(b.birim_id, f"Birim {b.birim_id}"): BirimPersonelStats(
#             aktif=b.aktif or 0,
#             ayrilan=b.ayrilan or 0
#         )
#         for b in birim_personel_sayisi
#     }
#
#     # Birthday query with only needed columns
#     dogum_gunu_olanlar = [
#         PersonelBase(
#             id=p.id,
#             adi=p.adi,
#             soyadi=p.soyadi
#         )
#         for p in db.exec(
#             select(Personel).where(
#                 func.to_char(Personel.dogum_tarihi, 'MM-DD') == today.strftime('%m-%d')
#             )
#         ).all()
#     ]
#
#     # Retirement candidates with only needed columns
#     emeklilik_tarihi = today - timedelta(days=29 * 365)
#     emeklilik_adaylari = [
#         Hatirlatma(
#             tur="Emeklilik",
#             id=p.id,
#             ad=p.adi,
#             soyad=p.soyadi
#         )
#         for p in db.exec(
#             select(Personel).where(
#                 Personel.memuriyete_giris_tarihi <= emeklilik_tarihi
#             )
#         ).all()
#     ]
#
#     # Single query for all returning leave cases
#     izin_donenler = db.exec(
#         select(PersonelIzin.donus_tarihi, Personel)
#         .join(Personel, Personel.id == PersonelIzin.personel_id)
#         .where(PersonelIzin.donus_tarihi.in_([today, tomorrow, next_week]))
#     ).all()
#
#     # Process returning leave data
#     def filter_izin_donenler(target_date: date) -> List[PersonelBase]:
#         return [
#             PersonelBase(
#                 id=p.id,
#                 adi=p.adi,
#                 soyadi=p.soyadi
#             )
#             for tarih, p in izin_donenler
#             if tarih == target_date
#         ]
#
#     # Blood type distribution optimized
#     kan_grubu_dagilimi = [
#         KanGrubuDagilimi(
#             kan_grubu=adi,
#             sayi=sayi or 0
#         )
#         for _, adi, sayi in db.exec(
#             select(
#                 PntsKod.kodu,
#                 PntsKod.adi,
#                 func.count(Personel.id).label("sayi")
#             ).join(Personel, Personel.kan_grubu_id == PntsKod.kodu)
#             .where(and_(
#                 PntsKod.turu == "KANGRUBU",
#                 Personel.cikis_tarihi.is_(None)
#             ))
#             .group_by(PntsKod.kodu, PntsKod.adi)
#         ).all()
#     ]
#
#     return DashboardResponse(
#         toplam_personel=personel_stats.toplam or 0,
#         aktif_personel=personel_stats.aktif or 0,
#         ayrilan_personel=personel_stats.ayrilan or 0,
#         birim_personel_sayisi=birim_personel_sayisi_dict,
#         dogum_gunu_olanlar=dogum_gunu_olanlar,
#         hatirlatmalar=emeklilik_adaylari,
#         izinden_donenler=IzinDonenler(
#             bugun=filter_izin_donenler(today),
#             yarin=filter_izin_donenler(tomorrow),
#             haftaya=filter_izin_donenler(next_week)
#         ),
#         kan_grubu_dagilimi=kan_grubu_dagilimi
#     )



from datetime import date, timedelta
from typing import Dict, List
from pydantic import BaseModel
from sqlmodel import Session, select, func, and_
from sqlalchemy import case, text
import json


## Response Modelleri
class PersonelBase(BaseModel):
    id: int
    adi: str
    soyadi: str


class BirimStats(BaseModel):
    aktif: int
    ayrilan: int


class DashboardResponse(BaseModel):
    toplam_personel: int
    aktif_personel: int
    ayrilan_personel: int
    birimler: Dict[str, BirimStats]
    dogum_gunu_olanlar: List[PersonelBase]
    emeklilik_adaylari: List[PersonelBase]
    izin_donenler: Dict[str, List[PersonelBase]]
    kan_grubu_dagilimi: Dict[str, int]


def get_dashboard_data(db: Session) -> DashboardResponse:
    today = date.today()
    emeklilik_siniri = today - timedelta(days=29 * 365)

    # TEK OPTİMİZE SORGUMUZ
    query = text("""
   WITH
  p_data AS (
    SELECT /*+ PARALLEL(p,4) */
      p.id,
      p.adi,
      p.soyadi,
      p.birim_id,
      p.kan_grubu_id,
      p.cikis_tarihi,
      p.dogum_tarihi,
      p.memuriyete_giris_tarihi
    FROM personel p
  ),
  i_data AS (
    SELECT /*+ PARALLEL(pi,4) */
      pi.personel_id,
      pi.donus_tarihi
    FROM personel_izin pi
    WHERE pi.donus_tarihi  BETWEEN :today 
        AND :today + INTERVAL '7' DAY
  ),
  personel_stats AS (
    SELECT
      COUNT(*)                                              AS toplam,
      SUM(CASE WHEN cikis_tarihi IS NULL THEN 1 ELSE 0 END)  AS aktif,
      SUM(CASE WHEN cikis_tarihi IS NOT NULL THEN 1 ELSE 0 END) AS ayrilan
    FROM p_data
  ),
  birim_stats AS (
    SELECT
      b.adi AS birim_adi,
      SUM(CASE WHEN p.cikis_tarihi IS NULL THEN 1 ELSE 0 END)     AS aktif,
      SUM(CASE WHEN p.cikis_tarihi IS NOT NULL THEN 1 ELSE 0 END) AS ayrilan
    FROM p_data p
    LEFT JOIN organizasyon_birimi b
      ON p.birim_id = b.birim_no
    GROUP BY b.adi
  ),
  kan_grubu AS (
    SELECT
      k.adi   AS kan_grubu,
      COUNT(*) AS sayi
    FROM p_data p
    JOIN pnts_kod k
      ON p.kan_grubu_id = k.kodu
     AND k.turu = 'KANGRUBU'
    WHERE p.cikis_tarihi IS NULL
    GROUP BY k.adi
  )
SELECT
  -- A) Toplam, aktif, ayrılan personel
  ps.toplam           AS toplam_personel,
  ps.aktif            AS aktif_personel,
  ps.ayrilan          AS ayrilan_personel,
  -- B) Birim dağılımı JSON
  (
    SELECT
      '{'
      || NVL(
           LISTAGG(
             '"'||bs.birim_adi||'":{"aktif":'||bs.aktif||',"ayrilan":'||bs.ayrilan||'}'
           , ',') 
           WITHIN GROUP (ORDER BY bs.birim_adi)
         , ''
         )
      || '}'
    FROM birim_stats bs
  ) AS birimler,
  -- C) Bugün doğum günü olanlar
  (
    SELECT
      '['
      || NVL(
           LISTAGG(
             '{"id":'||d.id
             ||',"adi":"'    ||REPLACE(d.adi,'"','\"')
             ||'","soyadi":"'||REPLACE(d.soyadi,'"','\"')
             ||'"}'
           , ',')
           WITHIN GROUP (ORDER BY d.id)
         , ''
         )
      || ']'
    FROM p_data d
    WHERE TO_CHAR(d.dogum_tarihi,'MM-DD') = TO_CHAR(:today,'MM-DD') and d.cikis_tarihi is null
  ) AS dogum_gunu_olanlar,
  -- D) Emeklilik adayları
  (
    SELECT
      '['
      || NVL(
           LISTAGG(
             '{"id":'||e.id
             ||',"adi":"'    ||REPLACE(e.adi,'"','\"')
             ||'","soyadi":"'||REPLACE(e.soyadi,'"','\"')
             ||'"}'
           , ',')
           WITHIN GROUP (ORDER BY e.id)
         , ''
         )
      || ']'
    FROM p_data e
    WHERE e.memuriyete_giris_tarihi <= :emeklilik_siniri
  ) AS emeklilik_adaylari,
  -- E) İzin dönenler: BUGÜN, YARIN, HAFTAYA
  (
    SELECT
      '{'
      || '"bugun":'
      || NVL(
           (
             SELECT
               '['
               || NVL(
                    LISTAGG(
                      '{"id":'||p.id
                      ||',"adi":"'    ||REPLACE(p.adi,'"','\"')
                      ||'","soyadi":"'||REPLACE(p.soyadi,'"','\"')
                      ||'"}'
                    , ',')
                    WITHIN GROUP (ORDER BY p.id)
                  , ''
                  )
               || ']'
             FROM p_data p
             JOIN i_data i ON p.id = i.personel_id
             WHERE i.donus_tarihi = :today
           ),
           '[]'
         )
      || ',"yarin":'
      || NVL(
           (
             SELECT
               '['
               || NVL(
                    LISTAGG(
                      '{"id":'||p.id
                      ||',"adi":"'    ||REPLACE(p.adi,'"','\"')
                      ||'","soyadi":"'||REPLACE(p.soyadi,'"','\"')
                      ||'"}'
                    , ',')
                    WITHIN GROUP (ORDER BY p.id)
                  , ''
                  )
               || ']'
             FROM p_data p
             JOIN i_data i ON p.id = i.personel_id
             WHERE i.donus_tarihi = :today + 1
           ),
           '[]'
         )
      || ',"haftaya":'
      || NVL(
           (
             SELECT
               '['
               || NVL(
                    LISTAGG(
                      '{"id":'||p.id
                      ||',"adi":"'    ||REPLACE(p.adi,'"','\"')
                      ||'","soyadi":"'||REPLACE(p.soyadi,'"','\"')
                      ||'"}'
                    , ',')
                    WITHIN GROUP (ORDER BY p.id)
                  , ''
                  )
               || ']'
             FROM p_data p
             JOIN i_data i ON p.id = i.personel_id
             WHERE i.donus_tarihi BETWEEN :today + 2 AND :today + 7
           ),
           '[]'
         )
      || '}'
    FROM dual
  ) AS izin_donenler,
  -- F) Kan grubu dağılımı JSON
  (
    SELECT
      '{'
      || NVL(
           LISTAGG(
             '"'||kg.kan_grubu||'":'||kg.sayi
           , ',')
           WITHIN GROUP (ORDER BY kg.kan_grubu)
         , ''
         )
      || '}'
    FROM kan_grubu kg
  ) AS kan_grubu_dagilimi
FROM personel_stats ps
    """)

    result = db.execute(query, {
        'today': today,
        'emeklilik_siniri': emeklilik_siniri
    }).one()

    # — parse JSON strings into Python objects —
    birimler = json.loads(result.birimler or "{}")
    dogum_gunu = json.loads(result.dogum_gunu_olanlar or "[]")
    emeklilik = json.loads(result.emeklilik_adaylari or "[]")
    izin = json.loads(result.izin_donenler or "{}")
    kan_grubu = json.loads(result.kan_grubu_dagilimi or "{}")

    # JSON verilerini Python dict'e çevirme
    return DashboardResponse(
        toplam_personel=result.toplam_personel,
        aktif_personel=result.aktif_personel,
        ayrilan_personel=result.ayrilan_personel,
        birimler={k: BirimStats(**v) for k, v in birimler.items()},
        dogum_gunu_olanlar=[PersonelBase(**p) for p in dogum_gunu],
        emeklilik_adaylari=[PersonelBase(**p) for p in emeklilik],
        izin_donenler={
            key: [PersonelBase(**p) for p in lst]
            for key, lst in izin.items()
        },
        kan_grubu_dagilimi=kan_grubu
    )