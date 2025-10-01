from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import date
from app.models.fsd import FSDSetting
from app.models.account import AccountBook
from app.models.fpa import FPA

# ── Setting
def get_setting(db: Session, user_id: int) -> Optional[FSDSetting]:
    return db.query(FSDSetting).filter(FSDSetting.user_id == user_id).first()

def upsert_setting(db: Session, user_id: int, data: dict) -> FSDSetting:
    row = get_setting(db, user_id)
    if not row:
        row = FSDSetting(user_id=user_id)
        db.add(row)
    for k, v in data.items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row

# ── Latest FPA
def get_latest_fpa(db: Session, user_id: int) -> Tuple[Optional[date], Optional[float]]:
    row = (
        db.query(FPA.snapshot_date, FPA.net_worth)
        .filter(FPA.user_id == user_id)
        .order_by(FPA.snapshot_date.desc(), FPA.id.desc())
        .first()
    )
    return (row[0], row[1]) if row else (None, None)

# ── Monthly aggregates
def get_month_income_expense(db: Session, user_id: int, year: int, month: int) -> Tuple[float, float]:
    # 규칙: amount > 0 ⇒ 수입, amount < 0 ⇒ 지출 (데이터가 모두 양수면 카테고리로 분기하도록 추후 확장)
    q = (
        db.query(
            func.sum(
                case((AccountBook.amount > 0, AccountBook.amount), else_=0.0)
            ).label("income"),
            func.sum(
                case((AccountBook.amount < 0, AccountBook.amount), else_=0.0)
            ).label("expense"),
        )
         .filter(
             AccountBook.user_id == user_id,
             extract("year", AccountBook.date) == year,
             extract("month", AccountBook.date) == month,
         )
     )
    income, expense = q.first()
    return float(income or 0.0), float(abs(expense or 0.0))

def get_top_categories(db: Session, user_id: int, year: int, month: int, limit: int = 5) -> List[Tuple[str, float]]:
    # 절대값 기준 지출 상위 카테고리 TOP N
    rows = (
        db.query(AccountBook.category, func.sum(AccountBook.amount).label("sum_amt"))
        .filter(
            AccountBook.user_id == user_id,
            extract("year", AccountBook.date) == year,
            extract("month", AccountBook.date) == month,
            AccountBook.amount < 0,  # 지출만
        )
        .group_by(AccountBook.category)
        .order_by(func.abs(func.sum(AccountBook.amount)).desc())
        .limit(limit)
        .all()
    )
    return [(r[0], float(abs(r[1] or 0.0))) for r in rows]
