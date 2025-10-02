# app/repositories/income_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate

def get_by_user_id(db: Session, user_id: int) -> Income | None:
    return db.query(Income).filter(Income.user_id == user_id).first()

def upsert_for_user(db: Session, user_id: int, data: IncomeCreate | IncomeUpdate) -> Income:
    row = get_by_user_id(db, user_id)
    if not row:
        row = Income(user_id=user_id)
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
