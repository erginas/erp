from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.modules.personel.izin.crud import create_personel_izin, get_personel_izin, get_personel_izin_list, \
    update_personel_izin, delete_personel_izin, create_personel_izin_detay, get_personel_izin_detay, \
    get_personel_izin_detay_list, update_personel_izin_detay, delete_personel_izin_detay, create_personel_izin_iptal, \
    get_personel_izin_iptal, get_personel_izin_iptal_list, update_personel_izin_iptal, delete_personel_izin_iptal, \
    create_personel_izin_turu, get_personel_izin_turu, get_personel_izin_turu_list, update_personel_izin_turu, \
    delete_personel_izin_turu, create_personel_unvan, get_personel_unvan, get_personel_unvan_list, \
    update_personel_unvan, delete_personel_unvan, create_tatil_gunleri, get_tatil_gunleri, get_tatil_gunleri_list, \
    update_tatil_gunleri, delete_tatil_gunleri
from app.api.modules.personel.izin.schemas import PersonelIzinRead, PersonelIzinCreate, PersonelIzinUpdate, \
    PersonelIzinDetayRead, PersonelIzinDetayCreate, PersonelIzinDetayUpdate, PersonelIzinIptalRead, \
    PersonelIzinIptalCreate, PersonelIzinIptalUpdate, PersonelIzinTuruRead, PersonelIzinTuruCreate, \
    PersonelIzinTuruUpdate, PersonelUnvanRead, PersonelUnvanCreate, PersonelUnvanUpdate, TatilGunleriRead, \
    TatilGunleriCreate, TatilGunleriUpdate

router = APIRouter(prefix="/personel-izin", tags=["PersonelIzin"])


@router.post("/", response_model=PersonelIzinRead)
def create_personel_izin_endpoint(personel_izin: PersonelIzinCreate, db: Session = Depends(get_db)):
    return create_personel_izin(db, personel_izin)


@router.get("/{personel_izin_id}", response_model=PersonelIzinRead)
def read_personel_izin_endpoint(personel_izin_id: int, db: Session = Depends(get_db)):
    db_personel_izin = get_personel_izin(db, personel_izin_id)
    if db_personel_izin is None:
        raise HTTPException(status_code=404, detail="PersonelIzin not found")
    return db_personel_izin


@router.get("/", response_model=list[PersonelIzinRead])
def read_personel_izin_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_izin_list(db, skip, limit)


@router.put("/{personel_izin_id}", response_model=PersonelIzinRead)
def update_personel_izin_endpoint(personel_izin_id: int, personel_izin: PersonelIzinUpdate,
                                  db: Session = Depends(get_db)):
    db_personel_izin = update_personel_izin(db, personel_izin_id, personel_izin)
    if db_personel_izin is None:
        raise HTTPException(status_code=404, detail="PersonelIzin not found")
    return db_personel_izin


@router.delete("/{personel_izin_id}")
def delete_personel_izin_endpoint(personel_izin_id: int, db: Session = Depends(get_db)):
    result = delete_personel_izin(db, personel_izin_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelIzin not found")
    return result


## Detay Endpoints

@router.post("/", response_model=PersonelIzinDetayRead)
def create_personel_izin_detay_endpoint(personel_izin_detay: PersonelIzinDetayCreate, db: Session = Depends(get_db)):
    return create_personel_izin_detay(db, personel_izin_detay)


@router.get("/{tarihi}/{personel_id}/{turu}/{izin_turu_id}", response_model=PersonelIzinDetayRead)
def read_personel_izin_detay_endpoint(tarihi: date, personel_id: int, turu: int, izin_turu_id: int,
                                      db: Session = Depends(get_db)):
    db_personel_izin_detay = get_personel_izin_detay(db, tarihi, personel_id, turu, izin_turu_id)
    if db_personel_izin_detay is None:
        raise HTTPException(status_code=404, detail="PersonelIzinDetay not found")
    return db_personel_izin_detay


@router.get("/", response_model=list[PersonelIzinDetayRead])
def read_personel_izin_detay_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_izin_detay_list(db, skip, limit)


@router.put("/{tarihi}/{personel_id}/{turu}/{izin_turu_id}", response_model=PersonelIzinDetayRead)
def update_personel_izin_detay_endpoint(tarihi: date, personel_id: int, turu: int, izin_turu_id: int,
                                        personel_izin_detay: PersonelIzinDetayUpdate, db: Session = Depends(get_db)):
    db_personel_izin_detay = update_personel_izin_detay(db, tarihi, personel_id, turu, izin_turu_id,
                                                        personel_izin_detay)
    if db_personel_izin_detay is None:
        raise HTTPException(status_code=404, detail="PersonelIzinDetay not found")
    return db_personel_izin_detay


@router.delete("/{tarihi}/{personel_id}/{turu}/{izin_turu_id}")
def delete_personel_izin_detay_endpoint(tarihi: date, personel_id: int, turu: int, izin_turu_id: int,
                                        db: Session = Depends(get_db)):
    result = delete_personel_izin_detay(db, tarihi, personel_id, turu, izin_turu_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelIzinDetay not found")
    return result


# izin iptal

@router.post("/", response_model=PersonelIzinIptalRead)
def create_personel_izin_iptal_endpoint(iptal: PersonelIzinIptalCreate, db: Session = Depends(get_db)):
    return create_personel_izin_iptal(db, iptal)


@router.get("/{iptal_id}", response_model=PersonelIzinIptalRead)
def read_personel_izin_iptal_endpoint(iptal_id: int, db: Session = Depends(get_db)):
    db_iptal = get_personel_izin_iptal(db, iptal_id)
    if db_iptal is None:
        raise HTTPException(status_code=404, detail="PersonelIzinIptal not found")
    return db_iptal


@router.get("/", response_model=list[PersonelIzinIptalRead])
def read_personel_izin_iptal_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_izin_iptal_list(db, skip, limit)


@router.put("/{iptal_id}", response_model=PersonelIzinIptalRead)
def update_personel_izin_iptal_endpoint(iptal_id: int, iptal: PersonelIzinIptalUpdate, db: Session = Depends(get_db)):
    db_iptal = update_personel_izin_iptal(db, iptal_id, iptal)
    if db_iptal is None:
        raise HTTPException(status_code=404, detail="PersonelIzinIptal not found")
    return db_iptal


@router.delete("/{iptal_id}")
def delete_personel_izin_iptal_endpoint(iptal_id: int, db: Session = Depends(get_db)):
    result = delete_personel_izin_iptal(db, iptal_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelIzinIptal not found")
    return result


# izin türü
@router.post("/", response_model=PersonelIzinTuruRead)
def create_personel_izin_turu_endpoint(izin_turu: PersonelIzinTuruCreate, db: Session = Depends(get_db)):
    return create_personel_izin_turu(db, izin_turu)


@router.get("/{izin_turu_id}", response_model=PersonelIzinTuruRead)
def read_personel_izin_turu_endpoint(izin_turu_id: int, db: Session = Depends(get_db)):
    db_izin_turu = get_personel_izin_turu(db, izin_turu_id)
    if db_izin_turu is None:
        raise HTTPException(status_code=404, detail="PersonelIzinTuru not found")
    return db_izin_turu


@router.get("/", response_model=list[PersonelIzinTuruRead])
def read_personel_izin_turu_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_izin_turu_list(db, skip, limit)


@router.put("/{izin_turu_id}", response_model=PersonelIzinTuruRead)
def update_personel_izin_turu_endpoint(izin_turu_id: int, izin_turu: PersonelIzinTuruUpdate,
                                       db: Session = Depends(get_db)):
    db_izin_turu = update_personel_izin_turu(db, izin_turu_id, izin_turu)
    if db_izin_turu is None:
        raise HTTPException(status_code=404, detail="PersonelIzinTuru not found")
    return db_izin_turu


@router.delete("/{izin_turu_id}")
def delete_personel_izin_turu_endpoint(izin_turu_id: int, db: Session = Depends(get_db)):
    result = delete_personel_izin_turu(db, izin_turu_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelIzinTuru not found")
    return result


# personel unvan

@router.post("/", response_model=PersonelUnvanRead)
def create_personel_unvan_endpoint(unvan: PersonelUnvanCreate, db: Session = Depends(get_db)):
    return create_personel_unvan(db, unvan)


@router.get("/{unvan_id}", response_model=PersonelUnvanRead)
def read_personel_unvan_endpoint(unvan_id: int, db: Session = Depends(get_db)):
    db_unvan = get_personel_unvan(db, unvan_id)
    if db_unvan is None:
        raise HTTPException(status_code=404, detail="PersonelUnvan not found")
    return db_unvan


@router.get("/", response_model=list[PersonelUnvanRead])
def read_personel_unvan_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_personel_unvan_list(db, skip, limit)


@router.put("/{unvan_id}", response_model=PersonelUnvanRead)
def update_personel_unvan_endpoint(unvan_id: int, unvan: PersonelUnvanUpdate, db: Session = Depends(get_db)):
    db_unvan = update_personel_unvan(db, unvan_id, unvan)
    if db_unvan is None:
        raise HTTPException(status_code=404, detail="PersonelUnvan not found")
    return db_unvan


@router.delete("/{unvan_id}")
def delete_personel_unvan_endpoint(unvan_id: int, db: Session = Depends(get_db)):
    result = delete_personel_unvan(db, unvan_id)
    if result is None:
        raise HTTPException(status_code=404, detail="PersonelUnvan not found")
    return result


# tatil günelri

@router.post("/", response_model=TatilGunleriRead)
def create_tatil_gunleri_endpoint(tatil_gunleri: TatilGunleriCreate, db: Session = Depends(get_db)):
    return create_tatil_gunleri(db, tatil_gunleri)


@router.get("/{ilk_tarih}/{adi}", response_model=TatilGunleriRead)
def read_tatil_gunleri_endpoint(ilk_tarih: date, adi: str, db: Session = Depends(get_db)):
    db_tatil_gunleri = get_tatil_gunleri(db, ilk_tarih, adi)
    if db_tatil_gunleri is None:
        raise HTTPException(status_code=404, detail="TatilGunleri not found")
    return db_tatil_gunleri


@router.get("/", response_model=list[TatilGunleriRead])
def read_tatil_gunleri_list_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tatil_gunleri_list(db, skip, limit)


@router.put("/{ilk_tarih}/{adi}", response_model=TatilGunleriRead)
def update_tatil_gunleri_endpoint(ilk_tarih: date, adi: str, tatil_gunleri: TatilGunleriUpdate,
                                  db: Session = Depends(get_db)):
    db_tatil_gunleri = update_tatil_gunleri(db, ilk_tarih, adi, tatil_gunleri)
    if db_tatil_gunleri is None:
        raise HTTPException(status_code=404, detail="TatilGunleri not found")
    return db_tatil_gunleri


@router.delete("/{ilk_tarih}/{adi}")
def delete_tatil_gunleri_endpoint(ilk_tarih: date, adi: str, db: Session = Depends(get_db)):
    result = delete_tatil_gunleri(db, ilk_tarih, adi)
    if result is None:
        raise HTTPException(status_code=404, detail="TatilGunleri not found")
    return result
