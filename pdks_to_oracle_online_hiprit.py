# -*- coding: utf-8 -*-
import os
import sys
import time
from datetime import datetime

import oracledb
from zk import ZK

# Yapılandırma
ORACLE_USER = "mgp"
ORACLE_PASSWORD = "mgp"
ORACLE_DSN = "192.168.0.253/tpsn"
ZK_IP = '192.168.0.234'
ZK_PORT = 4370


class HybridZKToOracle:
    def __init__(self):
        self.last_record_time = datetime.now()

    def connect_oracle(self):
        """Oracle veritabanına bağlantı kur"""
        try:
            self.ora_conn = oracledb.connect(
                user=ORACLE_USER,
                password=ORACLE_PASSWORD,
                dsn=ORACLE_DSN
            )
            return True
        except Exception as e:
            print(f"Oracle bağlantı hatası: {e}")
            return False

    def format_for_oracle(self, attendance):
        """Kaydı Oracle formatına dönüştür"""
        try:
            sicilno = str(attendance.user_id).zfill(4)
            tarih = attendance.timestamp

            # Oracle'a uygun tarih formatı
            tarih_oracle = f"TO_TIMESTAMP('{tarih.strftime('%d/%m/%Y %H:%M:%S')},000000','DD/MM/YYYY HH24:MI:SS,FF')"

            # Saat bilgileri
            saatnumber = tarih.hour * 60 + tarih.minute
            saat_str = f"{tarih.hour:02d}:{tarih.minute:02d}"
            saat_ondalik = round(tarih.hour + tarih.minute / 60.0, 2)
            saat_oracle = f"TO_TIMESTAMP('30/12/1899 {saat_str}:00,000000','DD/MM/YYYY HH24:MI:SS,FF')"

            return {
                'sicilno': sicilno,
                'tarih': tarih_oracle,
                'caltur_kodu': 2,
                'saatnumber': saatnumber,
                'saat': saat_oracle,
                'saatondalik': saat_ondalik,
                'saatstring': saat_str
            }
        except Exception as e:
            print(f"Kayıt formatlanırken hata: {e}")
            return None

    def insert_to_oracle(self, record_data):
        """Oracle'a kayıt ekle"""
        try:
            cursor = self.ora_conn.cursor()

            sql = f"""
            INSERT INTO MGP.PDKS_GP (
                SICILNO, TARIH, CALTURKODU, 
                SAATNUMBER, SAAT, SAATONDALIK, 
                SAATSTRING
            ) VALUES (
                '{record_data['sicilno']}', {record_data['tarih']}, {record_data['caltur_kodu']},
                {record_data['saatnumber']}, {record_data['saat']}, {record_data['saatondalik']},
                '{record_data['saatstring']}'
            )
            """

            cursor.execute(sql)
            self.ora_conn.commit()
            print(f"Kayıt eklendi: {record_data['sicilno']} - {record_data['saatstring']}")
            return True
        except Exception as e:
            print(f"Oracle'a kayıt eklenirken hata: {e}")
            self.ora_conn.rollback()
            return False

    def run_live_capture(self):
        """Canlı veri yakalama modu"""
        conn = None
        try:
            zk = ZK(ZK_IP, port=ZK_PORT, timeout=30)
            conn = zk.connect()
            print("Canlı veri yakalama başlatıldı...")

            for attendance in conn.live_capture():
                if attendance:
                    print(f"Yeni kayıt yakalandı: {attendance}")
                    formatted = self.format_for_oracle(attendance)
                    if formatted and self.insert_to_oracle(formatted):
                        self.last_record_time = datetime.now()

        except KeyboardInterrupt:
            print("\nCanlı yakalama sonlandırılıyor...")
        except Exception as e:
            print(f"Canlı yakalamada hata: {e}")
        finally:
            if conn:
                conn.disconnect()

    def run_periodic_check(self):
        """Periyodik kontrol modu"""
        while True:
            try:
                # Her 60 saniyede bir bağlantı kurup yeni kayıtları kontrol et
                zk = ZK(ZK_IP, port=ZK_PORT)
                with zk.connect() as conn:
                    attendances = conn.get_attendance()
                    new_records = [
                        a for a in attendances
                        if a.timestamp > self.last_record_time
                    ]

                    if new_records:
                        print(f"{len(new_records)} yeni kayıt bulundu")
                        for record in new_records:
                            formatted = self.format_for_oracle(record)
                            if formatted and self.insert_to_oracle(formatted):
                                self.last_record_time = record.timestamp

                time.sleep(60)

            except Exception as e:
                print(f"Periyodik kontrol sırasında hata: {e}")
                time.sleep(10)

    def run(self):
        """Hibrit çalışma modu"""
        if not self.connect_oracle():
            print("Oracle bağlantısı kurulamadı")
            return

        try:
            # Önce canlı yakalama denemesi yap
            self.run_live_capture()
        except Exception as e:
            print(f"Canlı yakalama başarısız, periyodik moda geçiliyor: {e}")
            self.run_periodic_check()
        finally:
            if hasattr(self, 'ora_conn'):
                self.ora_conn.close()


if __name__ == "__main__":
    # Çalışma dizini ayarları
    CWD = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.dirname(CWD)
    sys.path.append(ROOT_DIR)

    service = HybridZKToOracle()
    service.run()
