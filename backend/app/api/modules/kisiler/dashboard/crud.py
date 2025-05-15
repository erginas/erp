## Response Modelleri
import json
from datetime import date
from typing import Dict, List

from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session


class KisiBase(BaseModel):
    id: int
    adi: str
    soyadi: str


class BirimStats(BaseModel):
    aktif: int
    ayrilan: int


class DashboardResponse(BaseModel):
    toplam_kisi: int
    aktif_kisi: int
    ayrilan_kisi: int
    birimler: Dict[str, BirimStats]
    dogum_gunu_olanlar: List[KisiBase]
    izin_donenler: Dict[str, List[KisiBase]]


def get_dashboard_data(db: Session) -> DashboardResponse:
    today = date.today()
    # emeklilik_siniri = today - timedelta(days=29 * 365)

    # TEK OPTİMİZE SORGUMUZ
    query = text("""
   WITH
  p_data AS (
    SELECT /*+ PARALLEL(p,4) */
      p.id,
      p.adi,
      p.soyadi,
      p.BIRIM_NO,
      p.KAN_GRUBU,
      p.ISTEN_CIKIS_T ,
      p.dogum_tarihi,
      p.ISE_GIRIS_TARIHI
    FROM kisi p
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
      SUM(CASE WHEN ISTEN_CIKIS_T IS NULL THEN 1 ELSE 0 END)  AS aktif,
      SUM(CASE WHEN ISTEN_CIKIS_T IS NOT NULL THEN 1 ELSE 0 END) AS ayrilan
    FROM p_data
  ),
  birim_stats AS (
    SELECT
      b.adi AS birim_adi,
      SUM(CASE WHEN p.ISTEN_CIKIS_T IS NULL THEN 1 ELSE 0 END)     AS aktif,
      SUM(CASE WHEN p.ISTEN_CIKIS_T IS NOT NULL THEN 1 ELSE 0 END) AS ayrilan
    FROM p_data p
    LEFT JOIN organizasyon_birimi b
      ON p.birim_no = b.birim_no
    GROUP BY b.adi
  )
SELECT
  -- A) Toplam, aktif, ayrılan personel
  ps.toplam           AS toplam_kisi,
  ps.aktif            AS aktif_kisi,
  ps.ayrilan          AS ayrilan_kisi,
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
    WHERE TO_CHAR(d.dogum_tarihi,'MM-DD') = TO_CHAR(:today,'MM-DD') and d.ISTEN_CIKIS_T is null
  ) AS dogum_gunu_olanlar,
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
  ) AS izin_donenler
FROM personel_stats ps
    """)

    result = db.execute(query, {
        'today': today
    }).one()

    # — parse JSON strings into Python objects —
    birimler = json.loads(result.birimler or "{}")
    dogum_gunu = json.loads(result.dogum_gunu_olanlar or "[]")
    izin = json.loads(result.izin_donenler or "{}")

    # JSON verilerini Python dict'e çevirme
    return DashboardResponse(
        toplam_kisi=result.toplam_kisi,
        aktif_kisi=result.aktif_kisi,
        ayrilan_kisi=result.ayrilan_kisi,
        birimler={k: BirimStats(**v) for k, v in birimler.items()},
        dogum_gunu_olanlar=[KisiBase(**p) for p in dogum_gunu],
        izin_donenler={
            key: [KisiBase(**p) for p in lst]
            for key, lst in izin.items()
        },
    )
