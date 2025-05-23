## Response Modelleri
from datetime import date, timedelta
from typing import Dict, List

from pydantic import BaseModel, json
from sqlalchemy import text
from sqlmodel import Session


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
