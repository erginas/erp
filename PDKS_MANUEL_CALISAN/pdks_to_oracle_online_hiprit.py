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
        self.user_map = {}  # Kullanıcı bilgilerini saklamak için

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

            # Kullanıcı bilgilerini al
            user_info = self.user_map.get(attendance.user_id, {})
            card_number = user_info.get('card', '')
            user_name = user_info.get('name', 'Bilinmiyor')

            return {
                'PDKS_USER_NO': sicilno,
                'tarih': tarih_oracle,
                'caltur_kodu': 2,
                'saatnumber': saatnumber,
                'saat': saat_oracle,
                'saatondalik': saat_ondalik,
                'saatstring': saat_str,
                'CARD_NUMBER': card_number,
                'USER_NAME': user_name
            }
        except Exception as e:
            print(f"Kayıt formatlanırken hata: {e}")
            return None

    def insert_to_oracle(self, record_data):
        """Oracle'a kayıt ekle"""
        try:
            # cursor = self.ora_conn.cursor()
            sql = ""
            # sql = f"""
            # INSERT INTO MGP.PDKS_GP (
            #     PDKS_USER_NO, TARIH, CALTURKODU,
            #     SAATNUMBER, SAAT, SAATONDALIK,
            #     SAATSTRING, PDKS_KART_NO, USER_NAME
            # ) VALUES (
            #     '{record_data['PDKS_USER_NO']}',
            #     {record_data['tarih']},
            #     {record_data['caltur_kodu']},
            #     {record_data['saatnumber']},
            #     {record_data['saat']},
            #     {record_data['saatondalik']},
            #     '{record_data['saatstring']}',
            #     '{record_data['CARD_NUMBER']}',
            #     '{record_data['USER_NAME']}'
            # )
            # """

            # cursor.execute(sql)
            # self.ora_conn.commit()
            print(
                f"Kayıt eklendi: {record_data['PDKS_USER_NO']} - {record_data['USER_NAME']} - {record_data['saatstring']} - Kart: {record_data['CARD_NUMBER']}")
            return True
        except Exception as e:
            print(f"Oracle'a kayıt eklenirken hata: {e}")
            self.ora_conn.rollback()
            return False

    def load_users_from_device(self, conn):
        """Terminal cihazından kullanıcı bilgilerini yükle"""
        try:
            users = conn.get_users()
            self.user_map.clear()  # Önceki verileri temizle

            for user in users:
                self.user_map[user.user_id] = {
                    'uid': user.uid,
                    'name': user.name,
                    'privilege': user.privilege,
                    'card': user.card,
                    'group_id': user.group_id
                }
                print(f"Kullanıcı yüklendi: {user.user_id} - {user.name} - Kart No: {user.card}")

            print(f"Toplam {len(self.user_map)} kullanıcı yüklendi.")
            return True
        except Exception as e:
            print(f"Kullanıcı bilgileri yüklenirken hata: {e}")
            return False

    def run_live_capture(self):
        """Canlı veri yakalama modu"""
        conn = None
        try:
            zk = ZK(ZK_IP, port=ZK_PORT, timeout=30)
            conn = zk.connect()
            print("Canlı veri yakalama başlatıldı...")

            # Kullanıcı bilgilerini yükle
            self.load_users_from_device(conn)

            # Canlı veri yakalama
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
                    # Her seferinde kullanıcı bilgilerini güncelle
                    self.load_users_from_device(conn)

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
