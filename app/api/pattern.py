from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.init_db import get_db
from app.api.deps import get_current_user
from app.schemas.pattern import PatternOut, PatternSettingIn, PatternSettingOut
from app.services import pattern_service

router = APIRouter(tags=["pattern"])

@router.get("", response_model=PatternOut)
def get_pattern(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    top: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return pattern_service.get_pattern(db, user.id, year, month, top)

@router.post("/setting", response_model=PatternSettingOut)
def upsert_setting(
    payload: PatternSettingIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return pattern_service.save_setting(db, user.id, payload)
