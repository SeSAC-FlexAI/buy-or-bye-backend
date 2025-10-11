# app/repositories/expense_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from sqlalchemy import select
from datetime import date as Date

CATEGORY_TO_FIELD = {
    "식비": "food",
    "쇼핑": "shopping",
    "교통/차량": "transportation",
    "집/관리비": "household_maintenance",
    "문화/여가": "culture_leisure",
    "생활용품": "household_goods",  # (구 cosmetic → household_goods 로 바꿨다고 하셨음)
    "카드대금": "card_payment_withdrawal",
    "투자수익": "investment_expense",
    "기타": "other",
    "대출": "loans",     
    
}

EXCLUDE_FROM_SUM = {"id", "user_id", "date", "total_expense"}

def _recompute_total_expense(row: Expense) -> None:
    total = 0.0
    for col in row.__table__.columns:
        name = col.name
        if name in EXCLUDE_FROM_SUM:
            continue
        val = getattr(row, name) or 0.0
        total += float(val)
    row.total_expense = total


def _to_payload_dict(data) -> dict:
    if data is None:
        return {}
    if hasattr(data, "dict"):
        return data.dict(exclude_unset=True)
    if isinstance(data, dict):
        return data
    return {}

def get_by_user_id(db: Session, user_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.user_id == user_id).first()

def upsert_for_user(db: Session, user_id: int, data=None) -> Expense:
    payload = _to_payload_dict(data)

    row = get_by_user_id(db, user_id)
    if row:
        for k, v in payload.items():
            setattr(row, k, v)
        db.add(row)
    else:
        # 새로 만들 때 date 없으면 오늘 날짜로 보정 (또는 payload에서 받은 날짜)
        # if "date" not in payload or payload["date"] is None:
        #     payload["date"] = Date.today()
        # row = Expense(user_id=user_id, **payload)
        tx_date: Date = data.get("date") or Date.today()

        row = Expense(
            user_id=user_id,
            date=tx_date,
            total_expense=0.0,
            food=0.0,
            shopping=0.0,
            transportation=0.0,
            housing_maintenance=0.0,
            culture_leisure=0.0,
            household_goods=0.0,
            other=0.0,
            loans=0.0,
            investment_expense=0.0,
            card_payment_withdrawal=0.0
        )

        db.add(row)

    db.commit()
    db.refresh(row)
    return row

def apply_delta(db: Session, user_id: int, tx_date: Date, category: str, amount: float) -> Expense:
    """
    - 해당 user의 Expense 행 upsert
    - category 컬럼만 증감
    - total_expense는 자동 합계
    """
    row = upsert_for_user(db, user_id, {"date": tx_date})
    field = CATEGORY_TO_FIELD.get(category)
    if field is None:
        field = "etc"

    current = getattr(row, field) or 0.0
    setattr(row, field, float(current) + float(amount))

    _recompute_total_expense(row)
    return row

def delete_by_user(db: Session, user_id: int) -> bool:
    row = get_by_user_id(db, user_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True
