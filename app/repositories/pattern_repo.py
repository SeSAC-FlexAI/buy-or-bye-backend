import json
from typing import Optional, Dict, List, Tuple
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, literal

from app.models.pattern import PatternSetting
from app.models.account import AccountBook

def _to_json_str(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False)

def _from_json_str(s):
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None

# ── Setting
def get_setting(db: Session, user_id: int) -> Optional[PatternSetting]:
    return db.query(PatternSetting).filter(PatternSetting.user_id == user_id).first()

def upsert_setting(db: Session, user_id: int, monthly_budget: Optional[float], rules: Optional[Dict[str, str]]) -> PatternSetting:
    row = get_setting(db, user_id)
    if not row:
        row = PatternSetting(user_id=user_id)
        db.add(row)
    row.monthly_budget = monthly_budget
    row.rules_json = _to_json_str(rules)
    db.commit()
    db.refresh(row)
    return row

# ── Raw rows for the month (SQLite 호환: strftime 사용)
def get_month_rows(db: Session, user_id: int, year: int, month: int) -> List[Tuple[date, str, Optional[str], float]]:
    """
    return list of (date, category, description, amount)
    """
    rows = (
        db.query(
            AccountBook.date,
            AccountBook.category,
            AccountBook.description,
            AccountBook.amount,
        )
        .filter(
            AccountBook.user_id == user_id,
            func.strftime('%Y', AccountBook.date) == literal(f"{year:04d}"),
            func.strftime('%m', AccountBook.date) == literal(f"{month:02d}"),
        )
        .all()
    )
    return rows
