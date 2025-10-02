# app/services/expense_service.py
from sqlalchemy.orm import Session
from app.repositories import expense_repo
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

def get_my_expense(db: Session, user_id: int):
    return expense_repo.get_by_user_id(db, user_id)

def upsert_my_expense(db: Session, user_id: int, payload: ExpenseCreate | ExpenseUpdate):
    return expense_repo.upsert_for_user(db, user_id, payload)

def delete_my_expense(db: Session, user_id: int) -> bool:
    return expense_repo.delete_by_user(db, user_id)
