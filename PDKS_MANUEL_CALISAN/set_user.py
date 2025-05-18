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


def get_device_users(conn):
    """Cihazdaki kullanıcıları {user_id: user_obj} şeklinde döndürür"""
    try:
        users = conn.get_users()
        return {str(user.user_id): user for user in users} if users else {}
    except Exception as e:
        print(f"Cihaz kullanıcıları alınırken hata: {e}")
        return {}


def get_max_user_id(conn):
    """Cihazdaki maksimum user_id'yi bulur"""
    try:
        users = conn.get_users()
        if not users:
            return 1
        return max(int(user.user_id) for user in users if user.user_id is not None) + 1
    except Exception as e:
        print(f"Max user_id alınırken hata: {e}")
        return 1


def add_user_by_kimlik_no(conn, db_conn, kimlik_no):
    """Kimlik numarasına göre kullanıcı ekler"""
    cursor = None
    try:
        cursor = db_conn.cursor()

        # Veritabanından kullanıcı bilgilerini al
        cursor.execute("""
            SELECT adi, soyadi, pdks_kart_no, pdks_user_no
            FROM kisi 
            WHERE kimlik_no = :kimlik_no
        """, {'kimlik_no': kimlik_no})

        row = cursor.fetchone()

        if not row:
            print(f"Kimlik No: {kimlik_no} veritabanında bulunamadı")
            return False

        adi, soyadi, pdks_kart_no, pdks_user_no = row

        # Eğer pdks_user_no zaten varsa, cihazda olup olmadığını kontrol et
        if pdks_user_no is not None:
            device_users = get_device_users(conn)
            if str(pdks_user_no) in device_users:
                print(f"Bu kullanıcı zaten cihazda mevcut (ID: {pdks_user_no})")
                return False

        # Kart numarası kontrolü
        kart_no = str(pdks_kart_no) if pdks_kart_no is not None else "0"
        kart_no = ''.join(c for c in kart_no if c.isdigit()) or "0"

        # İsim formatlama
        formatted_name = format_isim(adi, soyadi)

        # Yeni user_id belirle (ya veritabanındaki pdks_user_no ya da yeni bir ID)
        new_user_id = pdks_user_no if pdks_user_no is not None else get_max_user_id(conn)

        # Kullanıcıyı cihaza ekleme
        conn.set_user(
            uid=int(new_user_id),
            name=formatted_name,
            privilege=const.USER_DEFAULT,
            card=kart_no,
            password='',
            user_id=str(new_user_id)
        )

        # Veritabanını güncelleme (eğer pdks_user_no yoksa)
        if pdks_user_no is None:
            cursor.execute("""
                UPDATE kisi 
                SET pdks_user_no = :user_id,
                    pdks_kart_no = :card_no
                WHERE kimlik_no = :kimlik_no
            """, {
                'user_id': new_user_id,
                'card_no': kart_no,
                'kimlik_no': kimlik_no
            })

        db_conn.commit()

        print(f"Kullanıcı başarıyla eklendi: ID:{new_user_id} | Ad:{formatted_name} | Kart:{kart_no}")
        return True

    except Exception as e:
        db_conn.rollback()
        print(f"Hata (Kimlik No: {kimlik_no}): {str(e)}")
        return False
    finally:
        if cursor:
            cursor.close()


def sync_users(conn, db_conn, selected_ids=None):
    """
    Kullanıcıları senkronize eder
    :param selected_ids: Güncellenecek spesifik ID'ler (None ise tümü)
    """
    cursor = None
    try:
        cursor = db_conn.cursor()

        # 1. Cihazdaki kullanıcıları al (user_id string olarak)
        device_users = get_device_users(conn)
        print(f"Cihazda {len(device_users)} kullanıcı bulundu")

        # 2. Veritabanından ilgili kayıtları al
        sql = """
            SELECT kimlik_no, adi, soyadi, pdks_kart_no, pdks_user_no 
            FROM kisi 
            WHERE pdks_user_no IS NOT NULL
        """
        params = []

        if selected_ids:
            sql += " AND pdks_user_no IN ({})".format(",".join([":" + str(i) for i in range(len(selected_ids))]))
            params = [str(id) for id in selected_ids]  # ID'leri string olarak gönder

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        if not rows:
            print("Güncellenecek kayıt bulunamadı")
            return

        updated_count = 0
        not_found_ids = []

        # 3. Her kayıt için işlem yap
        for row in rows:
            try:
                kimlik_no, adi, soyadi, pdks_kart_no, pdks_user_no = row
                str_pdks_user_no = str(pdks_user_no)  # Veritabanındaki ID'yi stringe çevir

                # Cihazda bu kullanıcı var mı kontrol et
                if str_pdks_user_no not in device_users:
                    not_found_ids.append(str_pdks_user_no)
                    continue

                # Kart numarası kontrolü
                kart_no = str(pdks_kart_no) if pdks_kart_no is not None else "0"
                kart_no = ''.join(c for c in kart_no if c.isdigit()) or "0"

                # İsim formatlama
                formatted_name = format_isim(adi, soyadi)

                # Mevcut kullanıcı bilgilerini al
                current_user = device_users[str_pdks_user_no]

                # Değişiklik kontrolü
                needs_update = (
                        current_user.name != formatted_name or
                        str(current_user.card) != kart_no or
                        current_user.privilege != const.USER_DEFAULT
                )

                if not needs_update:
                    continue

                # Kullanıcıyı güncelle
                conn.set_user(
                    uid=int(pdks_user_no),  # uid integer olmalı
                    name=formatted_name,
                    privilege=const.USER_DEFAULT,
                    card=kart_no,
                    password='',
                    user_id=str(pdks_user_no)  # user_id string olmalı
                )

                print(f"Güncellendi: ID:{pdks_user_no} | Ad:{formatted_name} | Kart:{kart_no}")
                updated_count += 1

            except Exception as user_error:
                print(f"Hata (ID:{pdks_user_no}): {str(user_error)}")
                continue

        print(f"\nToplam {updated_count} kullanıcı güncellendi")
        if not_found_ids:
            print(f"Cihazda bulunamayan ID'ler: {', '.join(not_found_ids)}")
            print("Bu ID'ler veritabanında kayıtlı ama cihazda yok. Önce ekleme yapılmalı.")

    except Exception as e:
        print(f"Senkronizasyon hatası: {str(e)}")
    finally:
        if cursor:
            cursor.close()


def show_menu():
    """Kullanıcı menüsünü gösterir"""
    print("\n" + "=" * 50)
    print("1 - Tüm Kullanıcıları Senkronize Et")
    print("2 - Seçili Kullanıcıları Senkronize Et")
    print("3 - Eksik Kullanıcıları Listele")
    print("4 - Kimlik No ile Kullanıcı Ekle")
    print("5 - Çıkış")
    return input("Seçiminiz (1-5): ").strip()


def get_selected_ids():
    """Kullanıcıdan ID listesi alır"""
    ids = input("Güncellenecek ID'leri virgülle ayırarak girin (Örnek: 101,205,308): ")
    return [int(id.strip()) for id in ids.split(",") if id.strip().isdigit()]


def get_kimlik_no():
    """Kullanıcıdan kimlik no alır"""
    return input("Eklemek istediğiniz kullanıcının kimlik numarasını girin: ").strip()


def list_missing_users(conn, db_conn):
    """Cihazda olmayan kullanıcıları listeler"""
    # ... (önceki list_missing_users fonksiyonunun aynısı) ...


if __name__ == "__main__":
    conn = None
    db_conn = None
    try:
        # Bağlantıları kur
        zk = ZK('192.168.0.234', port=4370, timeout=60)
        conn = zk.connect()
        print("Terminal bağlantısı başarılı")

        db_conn = oracledb.connect(user="mgp", password="mgp", dsn="192.168.0.253/tpsn")
        print("Veritabanı bağlantısı başarılı")

        # Menü döngüsü
        while True:
            choice = show_menu()

            if choice == "1":
                print("\nTüm kullanıcılar senkronize ediliyor...")
                sync_users(conn, db_conn)
            elif choice == "2":
                selected_ids = get_selected_ids()
                if selected_ids:
                    print(f"\nSeçilen ID'ler senkronize ediliyor: {selected_ids}")
                    sync_users(conn, db_conn, selected_ids)
                else:
                    print("Geçersiz ID girişi!")
            elif choice == "3":
                list_missing_users(conn, db_conn)
            elif choice == "4":
                kimlik_no = get_kimlik_no()
                if kimlik_no.isdigit():
                    print(f"\nKimlik No: {kimlik_no} için kullanıcı ekleniyor...")
                    add_user_by_kimlik_no(conn, db_conn, int(kimlik_no))
                else:
                    print("Geçersiz kimlik numarası!")
            elif choice == "5":
                print("Çıkış yapılıyor...")
                break
            else:
                print("Geçersiz seçim!")

    except Exception as e:
        print(f"Ana hata: {str(e)}")
    finally:
        if conn:
            conn.disconnect()
            print("Terminal bağlantısı kapatıldı")
        if db_conn:
            db_conn.close()
            print("Veritabanı bağlantısı kapatıldı")
