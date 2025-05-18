# Ortam değişkenleri ile bağlantı bilgileri
from datetime import datetime

import oracledb
from zk import ZK

DEVICE_IP = "192.168.0.234"
DEVICE_PORT = 4370
DB_USER = "mgp"
DB_PASSWORD = "mgp"
DB_DSN = "192.168.0.253/tpsn"


def get_zk_connection():
    """ZK cihazına bağlanır"""
    zk = ZK(DEVICE_IP, port=DEVICE_PORT, timeout=60)
    return zk.connect()


def get_db_connection():
    """Oracle veritabanına bağlanır"""
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)


def turkce_karakter_duzelt(text):
    tr_chars = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}
    for char, replacement in tr_chars.items():
        text = text.replace(char, replacement)
    return text


def format_isim(adi, soyadi):
    adi = str(adi) if adi is not None else ""
    soyadi = str(soyadi) if soyadi is not None else ""

    formatted_adi = turkce_karakter_duzelt(adi).strip().capitalize()
    formatted_soyadi = turkce_karakter_duzelt(soyadi).strip().upper()

    return f"{formatted_adi} {formatted_soyadi}".strip() or "NO_NAME"


def get_last_attendance_time_from_db():
    """Veritabanından en son işlenmiş zaman damgasını alır"""
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(TARIH) FROM MGP.PDKS_GP WHERE PROCESSED = 'Y'")
        result = cursor.fetchone()[0]
        conn.close()
        return result or datetime(2024, 1, 1)
    except Exception as e:
        print(f"Son işlem zamanı alınırken hata: {e}")
        return datetime(2024, 1, 1)
