from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.fsd import FsdHomeOut, FsdSettingIn, FsdSettingOut
from app.services import fsd_service

router = APIRouter(tags=["fsd"])

@router.get("/home", response_model=FsdHomeOut)
def fsd_home(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return fsd_service.get_home(db, user.id, year, month)

@router.put("/setting", response_model=FsdSettingOut)
def fsd_setting(
    payload: FsdSettingIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return fsd_service.upsert_setting(db, user.id, payload)
