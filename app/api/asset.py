from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.asset import AssetCreate, AssetUpdate, AssetOut
from app.services import asset_service
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=AssetOut)
def create_asset(
    payload: AssetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return asset_service.create_asset(db, current_user.id, payload)

@router.get("/", response_model=List[AssetOut])
def read_assets(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return asset_service.get_assets(db, user.id)

@router.get("/{asset_id}", response_model=AssetOut)
def read_asset(asset_id: int, db: Session = Depends(get_db)):
    account = asset_service.get_asset_by_id(db, asset_id)
    if not account:
        raise HTTPException(status_code=404, detail="asset not found")
    return account

@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, data: AssetUpdate, db: Session = Depends(get_db)):
    updated = asset_service.update_asset(db, asset_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="asset not found")
    return updated

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    ok = asset_service.delete_asset(db, asset_id)
    if not ok:
        raise HTTPException(status_code=404, detail="asset not found")
    return {"detail": "Asset deleted successfully"}
