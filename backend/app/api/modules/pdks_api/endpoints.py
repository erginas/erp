# main.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.api.modules.pdks_api.services import get_zk_connection, \
    get_device_users_safe, logger, get_db_connection, add_or_update_user, sync_attendance_data, delete_user_from_device

# from services import add_new_user, sync_users, list_missing_users

router = APIRouter(prefix="/pdks", tags=["Personel Devam Kontrol"])


class SyncRequest(BaseModel):
    ids: list[int]


@router.get("/")
def read_root():
    return {"message": "PDKS API Servisine Hoş Geldiniz!"}


# endpoints.py
@router.get("/device-users")
def api_list_device_users():
    """
    Cihazdaki tüm kullanıcıları listeler (Dökümandaki örnekle uyumlu)
    """
    conn = None
    try:
        conn = get_zk_connection()
        conn.disable_device()  # Dökümanda yapıldığı gibi

        response = get_device_users_safe(conn)

        conn.test_voice()  # Dökümanda yapıldığı gibi
        return response

    except Exception as e:
        logger.error(f"Hata: {str(e)}", exc_info=True)
        return {"error": str(e)}
    finally:
        if conn:
            try:
                conn.enable_device()  # Dökümanda yapıldığı gibi
                conn.disconnect()
            except Exception as e:
                logger.error(f"Bağlantı kapatma hatası: {str(e)}")


@router.post("/update-user/{kimlik_no}")
def api_add_or_update_user(kimlik_no: int):
    """
    Belirtilen `kimlik_no`'ya göre kullanıcıyı cihaza ekler veya günceller
    """
    conn = None
    db_conn = None
    try:
        conn = get_zk_connection()
        conn.disable_device()  # Cihazı kilitle

        db_conn = get_db_connection()
        result = add_or_update_user(conn, db_conn, kimlik_no)

        conn.test_voice()  # Sesli uyarı (isteğe bağlı)
        return result

    except Exception as e:
        logger.error(f"Hata oluştu: {str(e)}", exc_info=True)
        return {"error": str(e)}
    finally:
        if conn:
            try:
                conn.enable_device()
                conn.disconnect()
            except Exception as e:
                logger.error(f"Bağlantı kapatılırken hata: {str(e)}")


@router.post("/sync-attendance")
def manual_sync_attendance():
    """
    Cihazdan giriş-çıkış kayıtlarını manuel olarak senkronize eder
    """
    conn = None
    db_conn = None
    try:
        # 1. Cihaza bağlan
        conn = get_zk_connection()
        conn.disable_device()  # Opsiyonel: Cihazı kilitliyoruz
        print("Cihaza bağlanıldı")

        # 2. Veritabanına bağlan
        db_conn = get_db_connection()
        print("Veritabanına bağlanıldı")

        # 3. Senkronizasyon başlat
        result = sync_attendance_data(conn, db_conn)

        # 4. Cihazı aç
        conn.test_voice(index=1)  # Sesli onay
        conn.enable_device()

        return result

    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.disconnect()
        if db_conn:
            db_conn.close()


@router.delete("/delete-user/{user_id}")
def api_delete_user(user_id: str):
    """
    Cihazdan kullanıcıyı siler (user_id ile)
    """
    conn = None
    try:
        conn = get_zk_connection()
        conn.disable_device()  # Cihazı kilitleyelim

        result = delete_user_from_device(conn, user_id)

        conn.enable_device()
        conn.test_voice(index=3)  # Sesli onay
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.disconnect()
