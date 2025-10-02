# app/repositories/asset_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate

def get_by_user_id(db: Session, user_id: int) -> Asset | None:
    return db.query(Asset).filter(Asset.user_id == user_id).first()

def upsert_for_user(db: Session, user_id: int, data: AssetCreate | AssetUpdate) -> Asset:
    row = get_by_user_id(db, user_id)
    if not row:
        row = Asset(user_id=user_id)
        db.add(row)
    payload = data.dict(exclude_unset=True)
    for k, v in payload.items():
        setattr(row, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(row)
    return row

def delete_by_user(db: Session, user_id: int) -> bool:
    row = get_by_user_id(db, user_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True

# (선택) 기존 id 기반 API를 유지하려면 소유권 검증 추가 버전도 제공
def get_asset_by_id_for_user(db: Session, user_id: int, asset_id: int) -> Asset | None:
    return (
        db.query(Asset)
        .filter(Asset.id == asset_id, Asset.user_id == user_id)
        .first()
    )

def update_asset_by_id_for_user(db: Session, user_id: int, asset_id: int, data: AssetUpdate) -> Asset | None:
    row = get_asset_by_id_for_user(db, user_id, asset_id)
    if not row:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row

def delete_asset_by_id_for_user(db: Session, user_id: int, asset_id: int) -> bool:
    row = get_asset_by_id_for_user(db, user_id, asset_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True
