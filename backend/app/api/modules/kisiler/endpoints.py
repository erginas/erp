from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.api.modules.kisiler import crud
from app.api.modules.kisiler.models import Kisi
from app.api.modules.kisiler.schemas import KisiCreate, KisiUpdate, KisiRead

router = APIRouter(
    prefix="/kisiler",
    tags=["Kisiler"],
    responses={404: {"description": "Kisi not found"}}
)


# 🚀 Kişi oluşturma
@router.post("/", response_model=KisiRead, status_code=status.HTTP_201_CREATED)
def create_kisi(
        kisi_in: KisiCreate,
        session: SessionDep,
) -> Kisi:
    kisi = crud.create_kisi(session=session, kisi_in=kisi_in)
    return kisi


# 🚀 Tüm kişileri listeleme
@router.get("/", response_model=List[KisiRead], status_code=status.HTTP_200_OK)
def list_kisiler(
        skip: int = 0,
        limit: int = None,
        is_aktive: Optional[int] = None,
        kimlik_no: Optional[int] = None,
        adi: Optional[str] = None,
        soyadi: Optional[str] = None,
        cep_tel: Optional[str] = None,
        session: SessionDep = SessionDep,
) -> List[Kisi]:
    kisiler = crud.list_kisiler(
        session=session,
        skip=skip,
        limit=limit,
        is_active=is_aktive,
        kimlik_no=kimlik_no,
        adi=adi,
        soyadi=soyadi,
        cep_tel=cep_tel,
    )
    return kisiler


# 🚀 Kimlik No ile kişiyi getirme
@router.get("/{kimlik_no}", response_model=KisiRead, status_code=status.HTTP_200_OK)
def get_kisi_by_id(
        kimlik_no: int,
        session: SessionDep,
) -> Kisi:
    kisi = crud.get_kisi_by_id(session=session, kimlik_no=kimlik_no)
    if not kisi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kisi with ID {kimlik_no} not found",
        )
    return kisi


# 🚀 Kimlik No ile kişiyi güncelleme
@router.patch("/{kimlik_no}", response_model=KisiRead, status_code=status.HTTP_200_OK)
def update_kisi(
        kimlik_no: int,
        kisi_in: KisiUpdate,
        session: SessionDep,
) -> Kisi:
    kisi = crud.update_kisi(session=session, kimlik_no=kimlik_no, kisi_in=kisi_in)
    if not kisi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kisi with ID {kimlik_no} not found",
        )
    return kisi


# 🚀 Kimlik No ile kişiyi soft delete yapma
@router.delete("/{kimlik_no}", response_model=KisiRead, status_code=status.HTTP_200_OK)
def delete_kisi(
        kimlik_no: int,
        session: SessionDep,
) -> Kisi:
    kisi = crud.delete_kisi(session=session, kimlik_no=kimlik_no)
    if not kisi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kisi with ID {kimlik_no} not found",
        )
    return kisi
