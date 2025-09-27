import json
from typing import Optional
from sqlalchemy.orm import Session
from app.models.fpa import FPA
from app.schemas.fpa import FpaCreate

def _to_json_str(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False)

def _from_json_str(s):
    if s is None:
        return None
    try:
        return json.loads(s)
    except Exception:
        return s  # 문자열 그대로

def create(db: Session, user_id: int, payload: FpaCreate) -> FPA:
    row = FPA(
        user_id=user_id,
        snapshot_date=payload.snapshot_date,
        assets_total=payload.assets_total,
        debts_total=payload.debts_total,
        net_worth=payload.assets_total - payload.debts_total,
        detail_json=_to_json_str(payload.detail),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_by_id(db: Session, _id: int) -> Optional[FPA]:
    return db.query(FPA).filter(FPA.id == _id).first()

def delete(db: Session, row: FPA) -> None:
    db.delete(row)
    db.commit()
