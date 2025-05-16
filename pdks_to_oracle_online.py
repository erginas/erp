# -*- coding: utf-8 -*-
import os
import sys
import time
from datetime import datetime, timedelta

import oracledb
from zk import ZK

# Yapılandırma
ORACLE_USER = "mgp"
ORACLE_PASSWORD = "mgp"
ORACLE_DSN = "192.168.0.253/tpsn"
ZK_IP = '192.168.0.234'
ZK_PORT = 4370
CHECK_INTERVAL = 60  # Saniye cinsinden kontrol aralığı


class RealTimeZKToOracle:
    def __init__(self):
        self.last_check_time = datetime.now() - timedelta(minutes=5)

    def connect_oracle(self):
        """Oracle veritabanına bağlantı kur"""
        try:
            print("Oracle veritabanına bağlanılıyor...")
            self.ora_conn = oracledb.connect(
                user=ORACLE_USER,
                password=ORACLE_PASSWORD,
                dsn=ORACLE_DSN,
                # encoding="UTF-8"
            )
            print("Oracle veritabanına bağlanıldı")
            return True
        except Exception as e:
            print(f"Oracle bağlantı hatası: {str(e)}")
            return False

    def connect_zk(self):
        """ZK cihazına bağlantı kur"""
        try:
            print(f"ZK cihazına bağlanılıyor: {ZK_IP}:{ZK_PORT}")
            self.zk = ZK(ZK_IP, port=ZK_PORT, timeout=30)
            self.zk_conn = self.zk.connect()
            print("ZK cihazına bağlanıldı")
            return True
        except Exception as e:
            print(f"ZK bağlantı hatası: {str(e)}")
            return False

    def get_new_attendance(self):
        """Son kontrolden bu yana yeni kayıtları al"""
        try:
            start_time = self.last_check_time - timedelta(seconds=CHECK_INTERVAL * 2)
            print(f"Son kontrol: {self.last_check_time}, Kayıtlar aranıyor...")

            attendances = self.zk_conn.get_attendance()
            new_records = [
                rec for rec in attendances
                if rec.timestamp > self.last_check_time
            ]

            print(f"{len(new_records)} yeni kayıt bulundu")
            return new_records
        except Exception as e:
            print(f"Yoklama verisi alınırken hata: {str(e)}")
            return []

    def format_for_oracle(self, record):
        """Kaydı Oracle formatına dönüştür"""
        try:
            sicilno = str(record.user_id).zfill(4)
            tarih = record.timestamp

            tarih_str = tarih.strftime('%d/%m/%Y %H:%M:%S')
            tarih_oracle = f"TO_TIMESTAMP('{tarih_str},000000','DD/MM/YYYY HH24:MI:SS,FF')"

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
            print(f"Kayıt formatlanırken hata: {str(e)}")
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
            print(f"Kayıt başarıyla eklendi: {record_data['sicilno']}")
            return True
        except Exception as e:
            print(f"Oracle'a kayıt eklenirken hata: {str(e)}")
            self.ora_conn.rollback()
            return False

    def run(self):
        """Ana çalışma döngüsü"""
        print("Real-time veri aktarımı başlatılıyor...")

        while True:
            try:
                # Bağlantıları kontrol et
                if not hasattr(self, 'ora_conn') or not self.connect_oracle():
                    print("10 saniye bekleniyor...")
                    time.sleep(10)
                    continue

                if not hasattr(self, 'zk_conn') or not self.connect_zk():
                    print("10 saniye bekleniyor...")
                    time.sleep(10)
                    continue

                # Yeni kayıtları al
                new_records = self.get_new_attendance()

                if new_records:
                    for record in new_records:
                        formatted = self.format_for_oracle(record)
                        if formatted and self.insert_to_oracle(formatted):
                            print(f"Kayıt işlendi: {record.user_id} - {record.timestamp}")

                # Son kontrol zamanını güncelle
                self.last_check_time = datetime.now()

                print(f"{CHECK_INTERVAL} saniye bekleniyor...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                print("\nProgram sonlandırılıyor...")
                break
            except Exception as e:
                print(f"Beklenmeyen hata: {str(e)}")
                time.sleep(10)

        # Bağlantıları kapat
        if hasattr(self, 'zk_conn'):
            self.zk_conn.disconnect()
        if hasattr(self, 'ora_conn'):
            self.ora_conn.close()


if __name__ == "__main__":
    # Çalışma dizini ayarları
    CWD = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = os.path.dirname(CWD)
    sys.path.append(ROOT_DIR)

    print("Bağlantı testleri yapılıyor...")
    service = RealTimeZKToOracle()

    # Önce bağlantıları test et
    if service.connect_zk() and service.connect_oracle():
        print("Tüm bağlantılar başarılı, servis başlatılıyor...")
        service.run()
    else:
        print("Bağlantı kurulamadı, servis başlatılamıyor")
        print("Lütfen ayarları ve bağlantıları kontrol edin")
        print(f"Oracle DSN: {ORACLE_DSN}")
        print(f"ZK Cihaz IP: {ZK_IP}:{ZK_PORT}")
