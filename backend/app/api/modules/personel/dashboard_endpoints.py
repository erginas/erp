from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_session
from .dashboard_crud import get_dashboard_data

router = APIRouter(prefix="/dashboard/personel",
                   tags=["Dashboard"],
                   responses={404: {"description": "Kisi not found"}})


@router.get("/")
def get_dashboard(db: Session = Depends(get_session)):
    return get_dashboard_data(db)
