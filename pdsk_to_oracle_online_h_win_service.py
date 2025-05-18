# -*- coding: utf-8 -*-
import logging
import os
import sys

import oracledb
from dotenv import load_dotenv
from zk import ZK, const

# Loglama yapılandırması
logging.basicConfig(
    filename="pdks_sync.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

# Ortam değişkenlerinden ayarları al
DEVICE_IP = os.getenv("DEVICE_IP", "192.168.0.234")
DEVICE_PORT = int(os.getenv("DEVICE_PORT", "4370"))
DB_USER = os.getenv("DB_USER", "mgp")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mgp")
DB_DSN = os.getenv("DB_DSN", "192.168.0.253/tpsn")

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)


def turkce_karakter_duzelt(text):
    tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}
    for char, replacement in tr_chars.items():
        text = text.replace(char, replacement)
    return text


def format_isim(adi, soyadi):
    adi = str(adi) if adi is not None else ""
    soyadi = str(soyadi) if soyadi is not None else ""

    adi = turkce_karakter_duzelt(adi).strip()
    soyadi = turkce_karakter_duzelt(soyadi).strip()

    formatted_adi = adi.capitalize() if adi else ""
    formatted_soyadi = soyadi.upper() if soyadi else ""

    return f"{formatted_adi} {formatted_soyadi}".strip() or "NO_NAME"


def get_max_user_id(conn):
    try:
        users = conn.get_users()
        if not users:
            return 1
        return max(int(user.user_id) for user in users if user.user_id is not None) + 1
    except Exception as e:
        logging.error(f"Max user_id alınırken hata: {e}")
        return 1


def sync_users(conn, db_conn):
    cursor = None
    try:
        cursor = db_conn.cursor()

        next_id = get_max_user_id(conn)
        logging.info(f"Yeni kullanıcılar için başlangıç ID: {next_id}")

        cursor.execute("""
            SELECT kimlik_no, adi, soyadi, pdks_kart_no 
            FROM kisi
        """)
        rows = cursor.fetchall()

        if not rows:
            logging.warning("Veritabanında kayıt bulunamadı")
            return

        for row in rows:
            try:
                kimlik_no, adi, soyadi, pdks_kart_no = row

                kart_no = str(pdks_kart_no) if pdks_kart_no is not None else "0"
                kart_no = ''.join(c for c in kart_no if c.isdigit()) or "0"

                formatted_name = format_isim(adi, soyadi)

                user_data = {
                    'uid': next_id,
                    'name': formatted_name,
                    'privilege': const.USER_DEFAULT,
                    'card': kart_no,
                    'password': '',
                    'user_id': str(next_id)
                }
                logging.info(f"Eklenen kullanıcı verisi: {user_data}")

                conn.set_user(**user_data)

                cursor.execute("""
                    UPDATE kisi 
                    SET pdks_user_no = :user_id,
                        pdks_kart_no = :card_no
                    WHERE kimlik_no = :kimlik_no
                """, {
                    'user_id': next_id,
                    'card_no': kart_no,
                    'kimlik_no': kimlik_no
                })

                db_conn.commit()

                logging.info(f"Başarıyla eklendi: ID:{next_id}, İsim:{formatted_name}, Kart:{kart_no}")
                next_id += 1

            except Exception as user_error:
                db_conn.rollback()
                logging.error(f"Hata (kimlik_no: {kimlik_no}): {str(user_error)}")
                continue

    except Exception as e:
        logging.error(f"Senkronizasyon hatası: {str(e)}")
        if db_conn:
            db_conn.rollback()
    finally:
        if cursor:
            cursor.close()


def run_app():
    conn = None
    db_conn = None
    try:
        zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=60)
        conn = zk.connect()
        logging.info("Terminal bağlantısı başarılı")

        db_conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        logging.info("Veritabanı bağlantısı başarılı")

        sync_users(conn, db_conn)

    except Exception as e:
        logging.error(f"Ana hata: {str(e)}")
    finally:
        if conn:
            conn.disconnect()
            logging.info("Terminal bağlantısı kapatıldı")
        if db_conn:
            db_conn.close()
            logging.info("Veritabanı bağlantısı kapatıldı")
