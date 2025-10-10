# app/repositories/income_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate
from sqlalchemy import select

def _to_payload_dict(data) -> dict:
    """
    data 가 Pydantic 모델이면 .dict(exclude_unset=True),
    dict 면 그대로, None 이면 {} 로 변환.
    """
    if data is None:
        return {}
    if hasattr(data, "dict"):
        return data.dict(exclude_unset=True)
    if isinstance(data, dict):
        return data
    return {}
    

def get_by_user_id(db: Session, user_id: int) -> Income | None:
    return db.query(Income).filter(Income.user_id == user_id).first()


def upsert_for_user(db: Session, user_id: int, data=None) -> Income:
    payload = _to_payload_dict(data)

    row = get_by_user_id(db, user_id)
    if row:
        for k, v in payload.items():
            setattr(row, k, v)
        db.add(row)
    else:
        # # 새로 만들 때 date 없으면 오늘 날짜로 보정 (또는 payload에서 받은 날짜)
        # if "date" not in payload or payload["date"] is None:
        #     payload["date"] = Date.today()
        # row = Income(user_id=user_id, **payload)
       
        tx_date: Date = data.get("date") or Date.today()

        row = Income(
            user_id=user_id,
            date=tx_date,
            total_income=0.0,
            salary=0.0,
            investment_income=0.0,
            side_income=0.0,
            pin_money=0.0,
        )
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
