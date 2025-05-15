from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.modules.kisiler.dashboard.crud import get_dashboard_data
from app.core.db import get_session

router = APIRouter(prefix="/dashboard/kisi",
                   tags=["Dashboard"],
                   responses={404: {"description": "Kisi not found"}})


@router.get("/")
def get_dashboard(db: Session = Depends(get_session)):
    return get_dashboard_data(db)
