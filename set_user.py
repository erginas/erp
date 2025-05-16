# -*- coding: utf-8 -*-
import os
import sys

import oracledb
from zk import ZK, const

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)


def turkce_karakter_duzelt(text):
    """Türkçe karakterleri İngilizce karşılıklarına çevirir"""
    if text is None:
        return ""
    tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}
    for char, replacement in tr_chars.items():
        text = text.replace(char, replacement)
    return text


def format_isim(adi, soyadi):
    """İsim formatlama"""
    adi = str(adi) if adi is not None else ""
    soyadi = str(soyadi) if soyadi is not None else ""

    adi = turkce_karakter_duzelt(adi).strip()
    soyadi = turkce_karakter_duzelt(soyadi).strip()

    formatted_adi = adi.capitalize() if adi else ""
    formatted_soyadi = soyadi.upper() if soyadi else ""

    return f"{formatted_adi} {formatted_soyadi}".strip() or "NO_NAME"


def get_max_user_id(conn):
    """Cihazdaki maksimum user_id'yi bulur ve 1 artırır"""
    try:
        users = conn.get_users()
        if not users:
            return 1  # Hiç kullanıcı yoksa 1'den başla

        max_id = max(int(user.user_id) for user in users if user.user_id and str(user.user_id).isdigit())
        return max_id + 1
    except Exception as e:
        print(f"Max user_id alınırken hata: {e}")
        return 1  # Hata durumunda 1'den başla


def sync_users(conn, db_connection):
    """Kullanıcıları veritabanından terminal cihazına senkronize eder"""
    try:
        cursor = db_connection.cursor()

        # 1. Önce cihazdaki maksimum user_id'yi bul
        next_user_id = get_max_user_id(conn)
        print(f"Yeni kullanıcılar için başlangıç ID: {next_user_id}")

        # 2. Veritabanından kullanıcıları çek
        cursor.execute("""
            SELECT adi, soyadi, pdks_kart_no 
            FROM kisi 
            WHERE kimlik_no = 49
            ORDER BY pdks_user_no
        """)
        rows = cursor.fetchall()

        if not rows:
            print("Veritabanında kayıt bulunamadı")
            return

        # 3. Her kullanıcıyı teker teker ekle
        for row in rows:
            try:
                adi, soyadi, pdks_kart_no = row

                # Kart numarası kontrolü
                kart_no = str(pdks_kart_no) if pdks_kart_no else "0"
                kart_no = ''.join(c for c in kart_no if c.isdigit()) or "0"

                # İsim formatlama
                formatted_name = format_isim(adi, soyadi)

                # Kullanıcıyı ekleme
                conn.set_user(
                    uid=str(next_user_id),
                    name=str(formatted_name),
                    privilege=str(const.USER_DEFAULT),
                    card=str(kart_no),
                    password=str(''),
                    user_id=str(next_user_id))

                print(f"Eklendi: ID:{next_user_id}, İsim:{formatted_name}, Kart:{kart_no}")

                # Bir sonraki kullanıcı için ID'yi artır
                next_user_id += 1

            except Exception as user_error:
                print(f"Hata (satır: {row}): {str(user_error)}")
                continue

    except Exception as e:
        print(f"Senkronizasyon hatası: {str(e)}")
    finally:
        cursor.close()


if __name__ == "__main__":
    conn = None
    db_conn = None
    try:
        # ZK Terminal bağlantısı
        zk = ZK('192.168.0.234', port=4370, timeout=30)
        conn = zk.connect()
        print("Terminal bağlantısı başarılı")

        # Oracle veritabanı bağlantısı
        db_conn = oracledb.connect(user="mgp", password="mgp", dsn="192.168.0.253/tpsn")
        print("Veritabanı bağlantısı başarılı")

        # Senkronizasyonu başlat
        sync_users(conn, db_conn)

    except Exception as e:
        print(f"Ana hata: {str(e)}")
    finally:
        if conn:
            conn.disconnect()
            print("Terminal bağlantısı kapatıldı")
        if db_conn:
            db_conn.close()
            print("Veritabanı bağlantısı kapatıldı")
