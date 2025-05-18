# services.py
import logging
from datetime import time, datetime

import oracledb
from zk import ZK, const

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PDKSService")

# Ortam değişkenleri ile bağlantı bilgileri
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


def run_periodic_check():
    """Periyodik olarak cihazdan yeni devam kayıtlarını çeker ve veritabanına yazar"""
    while True:
        conn = None
        db_conn = None
        cursor = None
        try:
            # 1. Cihaza bağlan
            zk = ZK(DEVICE_IP, port=int(DEVICE_PORT))
            conn = zk.connect()
            print("Cihaza bağlanıldı")

            # 2. Veritabanı bağlantısı
            db_conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
            cursor = db_conn.cursor()

            # 3. Son işlenmiş zamanı al
            last_time = get_last_attendance_time_from_db()
            print(f"Son işlenmiş zaman: {last_time}")

            # 4. Katılım kayıtlarını al
            attendances = conn.get_attendance()
            if not attendances:
                print("Yeni kayıt bulunamadı")
                continue

            new_records = [a for a in attendances if a.timestamp > last_time]
            print(f"{len(new_records)} yeni kayıt bulundu")

            # 5. Kullanıcıları al (user_map için)
            user_map = {str(u.user_id): {'name': u.name, 'card': str(u.card)} for u in conn.get_users()}

            # 6. Yeni kayıtları işle
            for record in new_records:
                formatted = format_for_oracle(record, user_map, last_time)
                if formatted and insert_to_oracle(formatted, db_conn):
                    # İşlenmiş son tarihi güncelle
                    last_time = max(last_time, record.timestamp)

            db_conn.commit()

        except Exception as e:
            print(f"Periyodik kontrol sırasında hata: {e}")
            if db_conn:
                db_conn.rollback()
        finally:
            if conn:
                conn.disconnect()
            if cursor:
                cursor.close()
            if db_conn:
                db_conn.close()

        time.sleep(60)  # Her 60 saniyede bir kontrol et


def format_for_oracle(attendance, user_map, last_time):
    """Kaydı Oracle formatına dönüştür"""
    try:
        sicilno = str(attendance.user_id).zfill(4)
        tarih = attendance.timestamp

        # Sadece son işlenmiş zamandan sonra olan kayıtları işle
        if tarih <= last_time:
            return None

        # Saat bilgileri
        saatnumber = tarih.hour * 60 + tarih.minute
        saat_str = f"{tarih.hour:02d}:{tarih.minute:02d}"
        saat_ondalik = round(tarih.hour + tarih.minute / 60.0, 2)
        olay_tipi = int(attendance.status)  # 0=Giriş, 1=Çıkış
        processed = 'Y'

        # Kullanıcı bilgileri
        user_info = user_map.get(str(attendance.user_id), {})
        card_number = user_info.get('card', '')
        user_name = user_info.get('name', 'Bilinmiyor')

        return {
            'PDKS_USER_NO': sicilno,
            'TARIH': tarih.strftime("%d/%m/%Y %H:%M:%S"),
            'CAL_TUR_KODU': 2,  # Sabit kalabilir
            'SAATNUMBER': saatnumber,
            'SAAT': tarih.strftime("%H:%M:%S"),
            'SAATONDALIK': saat_ondalik,
            'SAATSTRING': saat_str,
            'CARD_NUMBER': card_number,
            'USER_NAME': user_name,
            'OLAY_TIPI': olay_tipi,
            'PROCESSED': processed
        }

    except Exception as e:
        print(f"Kayıt formatlanırken hata: {e}")
        return None


def insert_to_oracle(record_data, db_conn):
    """Oracle'a kayıt ekle"""
    cursor = None
    try:
        cursor = db_conn.cursor()

        # SQL: TO_TIMESTAMP kullanımı olmadan doğrudan Python'dan TIMESTAMP gönder
        sql = """
             INSERT INTO MGP.PDKS_GP (
                 PDKS_USER_NO, TARIH, CALTURKODU,
                 SAATNUMBER, SAAT, SAATONDALIK,
                 SAATSTRING, PDKS_KART_NO, USER_NAME, OLAY_TIPI, PROCESSED
             ) VALUES (
                 :PDKS_USER_NO, :TARIH, :CAL_TUR_KODU,
                 :SAATNUMBER, :SAAT, :SAATONDALIK,
                 :SAATSTRING, :CARD_NUMBER, :USER_NAME, :OLAY_TIPI, :PROCESSED
             )
             """

        cursor.execute(sql, {
            'PDKS_USER_NO': record_data['PDKS_USER_NO'],
            'TARIH': record_data['TARIH'],
            'CAL_TUR_KODU': record_data['CAL_TUR_KODU'],
            'SAATNUMBER': record_data['SAATNUMBER'],
            'SAAT': record_data['SAAT'],
            'SAATONDALIK': record_data['SAATONDALIK'],
            'SAATSTRING': record_data['SAATSTRING'],
            'CARD_NUMBER': record_data['CARD_NUMBER'],
            'USER_NAME': record_data['USER_NAME'],
            'OLAY_TIPI': record_data['OLAY_TIPI'],
            'PROCESSED': record_data['PROCESSED']
        })

        db_conn.commit()
        print(
            f"Kayıt eklendi: {record_data['PDKS_USER_NO']} - {record_data['USER_NAME']} - {record_data['SAATSTRING']}")
        return True

    except Exception as e:
        db_conn.rollback()
        print(f"Oracle'a kayıt eklenirken hata: {e}")
        return False
    finally:
        if cursor:
            cursor.close()


def sync_attendance_data(conn, db_conn):
    """
    Cihazdan giriş-çıkış kayıtlarını çeker ve veritabanına yazar
    :param conn: ZK bağlantısı
    :param db_conn: Oracle veritabanı bağlantısı
    :return: Sonuç mesajı (başarılı/eksik kayıt sayısı)
    """
    try:
        cursor = db_conn.cursor()

        # 1. Son işlenmiş zamanı al
        cursor.execute("SELECT MAX(TARIH) FROM MGP.PDKS_GP WHERE PROCESSED = 'Y'")
        result = cursor.fetchone()
        last_time = result[0] or datetime(2024, 1, 1)

        # 2. Cihazdan tüm devam kayıtlarını al
        attendances = conn.get_attendance()
        if not attendances:
            return {"status": "success", "message": "Cihazda kayıt bulunamadı"}

        # 3. Yalnızca yeni olanları filtrele
        new_records = [a for a in attendances if a.timestamp > last_time]
        print(f"{len(new_records)} yeni kayıt bulundu")

        if not new_records:
            return {"status": "success", "message": "İşlenecek yeni kayıt yok"}

        # 4. Kullanıcı haritasını al
        user_map = {str(u.user_id): {'name': u.name, 'card': str(u.card)} for u in conn.get_users()}

        # 5. Kayıtları işle ve veritabanına ekle
        inserted_count = 0
        for record in new_records:
            formatted = format_for_oracle(record, user_map, last_time)
            if formatted and insert_to_oracle(formatted, db_conn):
                inserted_count += 1
                last_time = max(last_time, record.timestamp)

        return {
            "status": "success",
            "inserted": inserted_count,
            "message": f"{inserted_count} yeni kayıt başarıyla eklendi"
        }

    except Exception as e:
        db_conn.rollback()
        return {"status": "error", "message": f"Senkronizasyon hatası: {str(e)}"}
    finally:
        if cursor:
            cursor.close()


def get_device_users(conn):
    try:
        users = conn.get_users()
        return {str(user.user_id): user for user in users} if users else {}
    except Exception as e:
        logger.error(f"Cihaz kullanıcıları alınırken hata: {e}")
        return {}


def safe_int(value, default=0):
    """Güvenli int dönüşümü"""
    try:
        return int(value)
    except (ValueError, TypeError, OverflowError):
        return default


def get_device_users_safe(conn):
    """Dökümanda çalışan kodun FastAPI uyumlu versiyonu"""
    try:
        users = conn.get_users()
        if not users:
            return {"users": []}

        result = []
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'

            result.append({
                'uid': user.uid,
                'name': user.name,
                'privilege': privilege,
                'password': user.password,
                'group_id': user.group_id,
                'user_id': user.user_id,
                'card': getattr(user, 'card', '')  # Bazı cihazlarda card özelliği olmayabilir
            })

        return {"users": result}

    except Exception as e:
        logger.error(f"Cihaz kullanıcıları alınırken hata: {e}")
        return {"error": str(e)}


def get_max_user_id(conn):
    try:
        users = conn.get_users()
        if not users:
            return 1
        return max(int(user.user_id) for user in users if user.user_id is not None) + 1
    except Exception as e:
        logger.error(f"Max user_id hatası: {e}")
        return 1


def add_or_update_user(conn, db_conn, kimlik_no):
    """
    Veritabanından kişi bilgisi alır ve cihazda günceller veya ekler
    """
    cursor = None
    try:
        cursor = db_conn.cursor()

        # 1. Veritabanından kullanıcıyı çek
        cursor.execute("""
            SELECT kimlik_no, adi, soyadi, pdks_kart_no, pdks_user_no 
            FROM kisi 
            WHERE kimlik_no = :kimlik_no
        """, {"kimlik_no": kimlik_no})
        row = cursor.fetchone()

        if not row:
            return {"status": "error", "message": f"{kimlik_no} numaralı kayıt bulunamadı"}

        kimlik_no, adi, soyadi, pdks_kart_no, pdks_user_no = row

        # 2. Cihazdaki kullanıcılar
        device_users = get_device_users(conn)
        str_pdks_user_no = str(pdks_user_no)

        # 3. Mevcut kullanıcı var mı?
        current_user = device_users.get(str_pdks_user_no)

        # 4. İsim ve kart formatlama
        formatted_name = format_isim(adi, soyadi)
        kart_no = ''.join(c for c in str(pdks_kart_no) if c.isdigit()) or "0"

        # 5. Yeni UID (cihazda yoksa otomatik oluştur)
        next_id = pdks_user_no or get_max_user_id(conn)

        # 6. Kullanıcıyı ekle veya güncelle
        conn.set_user(
            uid=int(next_id),
            name=formatted_name,
            privilege=const.USER_DEFAULT,
            card=kart_no,
            password='',
            user_id=str(next_id)
        )

        # 7. Eğer pdks_user_no yoksa, veritabanına yaz
        if not pdks_user_no:
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
            message = f"Yeni kullanıcı eklendi: ID:{next_id}"
        else:
            message = f"Kullanıcı güncellendi: ID:{next_id}"

        return {"status": "success", "message": message}

    except Exception as e:
        db_conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        if cursor:
            cursor.close()


def delete_user_from_device(conn, user_id):
    """
    Cihazdan belirtilen user_id'ye sahip kullanıcıyı siler
    :param conn: ZK bağlantısı
    :param user_id: silinecek kullanıcı ID'si (string olmalı)
    :return: Sonuç mesajı
    """
    try:
        # Cihazda bu kullanıcı var mı?
        users = conn.get_users()
        if not users:
            return {"status": "error", "message": "Cihazda kullanıcı bulunamadı"}

        # user_id ile eşleşen kullanıcıyı bul
        target_user = next((u for u in users if str(u.user_id) == str(user_id)), None)

        if not target_user:
            return {"status": "error", "message": f"{user_id} numaralı kullanıcı cihazda bulunamadı"}

        # Gerçek silme işlemi
        conn.delete_user(uid=target_user.uid, user_id=str(user_id))
        return {"status": "success", "message": f"Kullanıcı başarıyla silindi: {user_id}"}

    except Exception as e:
        return {"status": "error", "message": f"Hata: {str(e)}"}
