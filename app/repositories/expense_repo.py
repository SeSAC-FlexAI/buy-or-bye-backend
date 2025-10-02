# app/repositories/expense_repo.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

def get_by_user_id(db: Session, user_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.user_id == user_id).first()

def upsert_for_user(db: Session, user_id: int, data: ExpenseCreate | ExpenseUpdate) -> Expense:
    row = get_by_user_id(db, user_id)
    if not row:
        row = Expense(user_id=user_id)
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
