# -*- coding: utf-8 -*-
import os
import sys

import oracledb
from zk import ZK

# Oracle bağlantı bilgileri
ORACLE_USER = "mgp"
ORACLE_PASSWORD = "mgp"
ORACLE_DSN = "192.168.0.253/tpsn"

# ZK cihazı bağlantı bilgileri
ZK_IP = '192.168.0.234'
ZK_PORT = 4370


def get_zk_attendance_data():
    """ZK cihazından yoklama verilerini al"""
    conn = None
    zk = ZK(ZK_IP, port=ZK_PORT)
    try:
        conn = zk.connect()
        print("ZK cihazına bağlanıldı")

        # Son 1 günün yoklama kayıtlarını al
        attendances = conn.get_attendance()
        return attendances

    except Exception as e:
        print(f"ZK cihazından veri alınırken hata oluştu: {e}")
        return []
    finally:
        if conn:
            conn.disconnect()


def insert_to_oracle(attendance_data):
    """Oracle veritabanına verileri ekle"""
    ora_conn = None
    try:
        ora_conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        ora_cursor = ora_conn.cursor()

        inserted_count = 0

        for record in attendance_data:
            try:
                # ZK kaydını Oracle tablo yapısına uygun hale getir
                sicilno = str(record.user_id).zfill(4)  # 4 haneli sicil no
                tarih = record.timestamp

                # Tarih formatını Oracle'a uygun hale getir (DD/MM/YYYY)
                tarih_str = tarih.strftime('%d/%m/%Y %H:%M:%S') if tarih else None
                tarih_oracle = f"TO_TIMESTAMP('{tarih_str},000000','DD/MM/YYYY HH24:MI:SS,FF')" if tarih else 'NULL'

                caltur_kodu = 2  # Örnekte 2 olarak görünüyor

                # Saat bilgilerini hazırla
                if tarih:
                    saatnumber = tarih.hour * 60 + tarih.minute  # Dakika cinsinden
                    saat_str = f"{tarih.hour:02d}:{tarih.minute:02d}"
                    saat_ondalik = tarih.hour + tarih.minute / 60.0
                    saat_oracle = f"TO_TIMESTAMP('30/12/1899 {saat_str}:00,000000','DD/MM/YYYY HH24:MI:SS,FF')"
                else:
                    saatnumber = None
                    saat_str = None
                    saat_ondalik = None
                    saat_oracle = 'NULL'

                # Oracle'a insert işlemi (doğrudan SQL stringi olarak)
                sql = f"""
                INSERT INTO MGP.PDKS_GP (
                    SICILNO, TARIH, CALTURKODU, 
                    SAATNUMBER, SAAT, SAATONDALIK, 
                    SAATSTRING
                ) VALUES (
                    '{sicilno}', {tarih_oracle}, {caltur_kodu},
                    {saatnumber or 'NULL'}, {saat_oracle}, {saat_ondalik or 'NULL'},
                    {'NULL' if not saat_str else f"'{saat_str}'"}
                )
                """

                ora_cursor.execute(sql)
                inserted_count += 1

            except Exception as e:
                print(f"Kayıt işlenirken hata oluştu (Sicil No: {record.user_id}): {e}")
                continue

        ora_conn.commit()
        print(f"✅ {inserted_count} kayıt Oracle'a başarıyla eklendi.")

    except Exception as e:
        print(f"Oracle'a veri eklenirken hata oluştu: {e}")
    finally:
        if ora_conn:
            ora_conn.close()


def main():
    # Çalışma dizini ayarları
    CWD = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.dirname(CWD)
    sys.path.append(ROOT_DIR)

    # ZK cihazından verileri al
    attendance_data = get_zk_attendance_data()

    if not attendance_data:
        print("ZK cihazından veri alınamadı veya kayıt bulunamadı.")
        return

    print(f"ZK cihazından {len(attendance_data)} kayıt alındı.")

    # Oracle'a verileri yaz
    insert_to_oracle(attendance_data)


if __name__ == "__main__":
    main()
