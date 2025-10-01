from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def create_asset(db: Session, user_id: int, data: AssetCreate):
    asset = Asset(user_id=user_id, **data.dict())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

def get_asset(db: Session, user_id: int):
    return db.query(Asset).filter(Asset.user_id == user_id).all()

def get_asset_by_id(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()

def update_asset(db: Session, asset: Asset, data: AssetUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    return asset

def delete_account(db: Session, asset: Asset):
    db.delete(asset)
    db.commit()
