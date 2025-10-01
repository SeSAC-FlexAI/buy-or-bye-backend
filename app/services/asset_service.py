# app/services/asset_service.py
from sqlalchemy.orm import Session
from app.repositories import asset_repo
from app.schemas.asset import AssetCreate, AssetUpdate

def create_asset(db: Session, user_id: int, asset: AssetCreate):
    return asset_repo.create_asset(db, user_id, asset)

def get_assets(db: Session, user_id: int):
    return asset_repo.get_asset(db, user_id)

def get_asset_by_id(db: Session, asset_id: int):
    return asset_repo.get_asset_by_id(db, asset_id)

def update_asset(db: Session, asset_id: int, data: AssetUpdate):
    asset = asset_repo.get_asset_by_id(db, asset_id)
    if not asset:
        return None
    return asset_repo.update_asset(db, asset, data)

def delete_asset(db: Session, asset_id: int):
    asset = asset_repo.get_asset_by_id(db, asset_id)
    if not asset:
        return None
    asset_repo.delete_asset(db, asset)
    return True