# app/repositories/goal_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate

def get_one(
    db: Session, user_id: int, goal_type: str, period: str, year: int,
    month: Optional[int], category: Optional[str]
) -> Optional[Goal]:
    q = db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.goal_type == goal_type,
        Goal.period == period,
        Goal.year == year,
        Goal.month.is_(month) if month is None else Goal.month == month,
        Goal.category.is_(category) if category is None else Goal.category == category,
    )
    return q.first()

def list_goals(
    db: Session, user_id: int,
    goal_type: Optional[str] = None, period: Optional[str] = None,
    year: Optional[int] = None, month: Optional[int] = None, category: Optional[str] = None
) -> List[Goal]:
    q = db.query(Goal).filter(Goal.user_id == user_id)
    if goal_type: q = q.filter(Goal.goal_type == goal_type)
    if period:    q = q.filter(Goal.period == period)
    if year:      q = q.filter(Goal.year == year)
    if month is not None: q = q.filter(Goal.month == month)
    if category is not None: q = q.filter(Goal.category == category)
    return q.order_by(Goal.year.desc(), Goal.month.desc().nullsfirst()).all()

def upsert(
    db: Session, user_id: int, payload: GoalCreate | GoalUpdate
) -> Goal:
    data = payload.model_dump(exclude_unset=True)
    key = {k: data.get(k) for k in ["goal_type", "period", "year", "month", "category"]}
    row = get_one(db, user_id, **key) if all(k in data for k in key) else None

    if not row:
        row = Goal(user_id=user_id, **key)  # 키 필수 항목 있어야 함
        db.add(row)

    # 값 반영
    for k, v in data.items():
        if k not in ("goal_type", "period", "year", "month", "category") or getattr(row, k, None) is None:
            setattr(row, k, v)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(row)
    return row

def delete_one(
    db: Session, user_id: int, goal_type: str, period: str, year: int,
    month: Optional[int], category: Optional[str]
) -> bool:
    row = get_one(db, user_id, goal_type, period, year, month, category)
    if not row: return False
    db.delete(row)
    db.commit()
    return True
