# app/api/asset.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut
from app.services import asset_service
from app.api.deps import get_current_user

router = APIRouter()

# ---------- /me (대시보드 단건) ----------
@router.get("/me", response_model=AssetOut | None)
def read_my_asset(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return asset_service.get_my_asset(db, user.id)

@router.post("/me", response_model=AssetOut, status_code=status.HTTP_201_CREATED)
def create_or_replace_my_asset(
    payload: AssetCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return asset_service.upsert_my_asset(db, user.id, payload)

@router.put("/me", response_model=AssetOut)
def update_my_asset(
    payload: AssetUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return asset_service.upsert_my_asset(db, user.id, payload)

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_asset(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    ok = asset_service.delete_my_asset(db, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="asset not found")
    return {"success": True}