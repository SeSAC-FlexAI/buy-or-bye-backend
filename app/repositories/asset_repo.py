# app/repositories/asset_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.asset import Asset
from app.schemas.asset import AssetUpdate
from sqlalchemy import select

def get_by_user_id(db: Session, user_id: int) -> Asset | None:
    return db.query(Asset).filter(Asset.user_id == user_id).first()

def _to_payload_dict(data) -> dict:
    """
    data가 Pydantic 모델이면 .dict(exclude_unset=True),
    dict면 그대로, None이면 {}로 변환.
    """
    if data is None:
        return {}
    if hasattr(data, "dict"):
        return data.dict(exclude_unset=True)
    if isinstance(data, dict):
        return data
    # 그 외 타입 방어
    return {}    

def upsert_for_user(db: Session, user_id: int, data=None) -> Asset:
    payload = _to_payload_dict(data)

    row = db.execute(
        select(Asset).where(Asset.user_id == user_id)
    ).scalar_one_or_none()

    if row:
        for k, v in payload.items():
            setattr(row, k, v)
        db.add(row)
    else:
        # 새로 만들 때 date 없으면 오늘 날짜로 보정 (또는 payload에서 받은 날짜)
        if "date" not in payload or payload["date"] is None:
            payload["date"] = Date.today()
        row = Asset(user_id=user_id, **payload)
        db.add(row)

    db.commit()
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
