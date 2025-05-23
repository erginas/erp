# -*- coding: utf-16 -*-
from datetime import datetime

import firebirdsql
import oracledb

# Firebird bağlantısı
fb_conn = firebirdsql.connect(
    host='192.168.1.139',
    database="data",
    user='sysdba',
    password='masterkey'
    
)
fb_cursor = fb_conn.cursor()

# Oracle bağlantısı
ora_conn = oracledb.connect(user="mgp", password="mgp", dsn="192.168.0.253/tpsn")
ora_cursor = ora_conn.cursor()

# Firebird'den verileri çek
fb_cursor.execute("""
    SELECT SICILNO, BARKOD, SOYADI, ADI, DEPARTMANKODU, SIRKETKODU, GIRISTARIHI, CIKISTARIHI, SSK,
           KOD1, KOD2, POSTAKODU, DEPARTMANTARIHI, POSTATARIHI, ADRES, TELEFON1, TELEFON2, SERVISKODU,
           BABAADI, ANAADI, DOGUMYERI, DOGUMTARIHI, MEDENIHALI, KANGRUBU, DINI, IL, ILCE, MAHALLE, KOY,
           CILTNO, SAYFANO, KUTUKSIRA, NUFUSIDARESI, VERNEDENI, CUZDANSIRA, ALAN01, ALAN02, ALAN03, ALAN04,
           ALAN05, ALAN06, ALAN07, ALAN08, ALAN09, ALAN10, ALAN11, ALAN12, ALAN13, ALAN14, ALAN15, ALAN16,
           ALAN17, ALAN18, ALAN19, ALAN20, REFKEY, FOTOGRAF, SIRKETTARIHI, YEDEKPOSTA, BARKODTARIHI,
           FAZLAMESAI, DAHILITEL, TCKIMLIKNO, VERGINO, CUZDANSERINO, CUZDANNO, GCDURUM, GOREVI, YETKI,
           OZELKOD1, OZELKOD2, BASLAMATARIHI, BITISTARIHI, GUNDONUMSAAT, YMKGCDURUM, MASYERKODU, MASYERTARIHI,
           ADRESBIL, GECISYETKI, GECISYETKIGRUP, GRUPKODU, GRUPKODUTARIHI, PDKSTERM, ACCESSTERM, TURNIKETERM,
           YEMEKHANETERM, PDKSGCDURUM, TURNGCDURUM, BARKOD2, SICILNO2, ID, ID2, PDKSTERM2, ACCESSTERM2,
           TURNIKETERM2, YEMEKHANETERM2
    FROM PERSONEL
""")

rows = fb_cursor.fetchall()

# Verileri Oracle'a aktar
for row in rows:
    converted_row = list(row)

    # Tarih alanlarını dönüştür (gerekirse)
    for idx in [6, 7, 12, 13, 57, 59, 71, 72]:
        if isinstance(converted_row[idx], str):
            try:
                converted_row[idx] = datetime.strptime(converted_row[idx], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                converted_row[idx] = None

    ora_cursor.execute("""
        INSERT INTO MGP.PDKS_PERSONEL (
            SICILNO, BARKOD, SOYADI, ADI, DEPARTMANKODU, SIRKETKODU, GIRISTARIHI, CIKISTARIHI, SSK,
            KOD1, KOD2, POSTAKODU, DEPARTMANTARIHI, POSTATARIHI, ADRES, TELEFON1, TELEFON2, SERVISKODU,
            BABAADI, ANAADI, DOGUMYERI, DOGUMTARIHI, MEDENIHALI, KANGRUBU, DINI, IL, ILCE, MAHALLE, KOY,
            CILTNO, SAYFANO, KUTUKSIRA, NUFUSIDARESI, VERNEDENI, CUZDANSIRA, ALAN01, ALAN02, ALAN03, ALAN04,
            ALAN05, ALAN06, ALAN07, ALAN08, ALAN09, ALAN10, ALAN11, ALAN12, ALAN13, ALAN14, ALAN15, ALAN16,
            ALAN17, ALAN18, ALAN19, ALAN20, REFKEY, FOTOGRAF, SIRKETTARIHI, YEDEKPOSTA, BARKODTARIHI,
            FAZLAMESAI, DAHILITEL, TCKIMLIKNO, VERGINO, CUZDANSERINO, CUZDANNO, GCDURUM, GOREVI, YETKI,
            OZELKOD1, OZELKOD2, BASLAMATARIHI, BITISTARIHI, GUNDONUMSAAT, YMKGCDURUM, MASYERKODU, MASYERTARIHI,
            ADRESBIL, GECISYETKI, GECISYETKIGRUP, GRUPKODU, GRUPKODUTARIHI, PDKSTERM, ACCESSTERM, TURNIKETERM,
            YEMEKHANETERM, PDKSGCDURUM, TURNGCDURUM, BARKOD2, SICILNO2, ID, ID2, PDKSTERM2, ACCESSTERM2,
            TURNIKETERM2, YEMEKHANETERM2
        ) VALUES (
            :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20,
            :21, :22, :23, :24, :25, :26, :27, :28, :29, :30, :31, :32, :33, :34, :35, :36, :37, :38,
            :39, :40, :41, :42, :43, :44, :45, :46, :47, :48, :49, :50, :51, :52, :53, :54, :55, :56,
            :57, :58, :59, :60, :61, :62, :63, :64, :65, :66, :67, :68, :69, :70, :71, :72, :73, :74,
            :75, :76, :77, :78, :79, :80, :81, :82, :83, :84, :85, :86, :87, :88, :89, :90, :91, :92, :93, :94, :95, :96
        )
    """, converted_row)

ora_conn.commit()
ora_cursor.close()
ora_conn.close()
fb_cursor.close()
fb_conn.close()

print("✅ Veri aktarımı tamamlandı.")
