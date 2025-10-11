# app/repositories/income_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate
from sqlalchemy import select
from datetime import date as Date

CATEGORY_TO_FIELD = {
    "월급": "salary",
    "투자수익": "investment_income",
    "부가수익": "side_income",
    "용돈": "pin_money",
    "대출": "loans",  # 유입(대출금 유입)을 수입에 적는 정책이라면 유지, 아니면 제거
}

EXCLUDE_FROM_SUM = {"id", "user_id", "date", "total_income"}

def _recompute_total_income(row: Income) -> None:
    total = 0.0
    for col in row.__table__.columns:
        name = col.name
        if name in EXCLUDE_FROM_SUM:
            continue
        val = getattr(row, name) or 0.0
        total += float(val)
    row.total_income = total

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

def apply_delta(db: Session, user_id: int, tx_date: Date, category: str, amount: float) -> Income:
    """
    - 해당 user의 Income 행을 upsert
    - category에 해당하는 세부 컬럼만 증감
    - total_income은 모든 세부항목 합으로 ‘자동 재계산’
    """
    row = upsert_for_user(db, user_id, {"date": tx_date})
    field = CATEGORY_TO_FIELD.get(category)
    if field is None:
        # 정의되지 않은 카테고리는 '부업/기타'로 몰아넣는 정책 (원하면 에러로 바꿔도 됨)
        field = "side_income"

    current = getattr(row, field) or 0.0
    setattr(row, field, float(current) + float(amount))

    _recompute_total_income(row)
    # 여기서는 commit 안 함 (service에서 트랜잭션 제어)
    return row

def delete_by_user(db: Session, user_id: int) -> bool:
    row = get_by_user_id(db, user_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True

