# app/services/expense_service.py
from sqlalchemy.orm import Session
from app.repositories import expense_repo 
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

def create_expense(db: Session, user_id: int, expense: ExpenseCreate):
    return expense_repo.create_expense(db, user_id, expense)

def get_expense(db: Session, user_id: int):
    return expense_repo.get_expense(db, user_id)

def get_expense_by_id(db: Session, expense_id: int):
    return expense_repo.get_expense_by_id(db, expense_id)

def update_expense(db: Session, expense_id: int, data: ExpenseUpdate):
    expense = expense_repo.get_expense_by_id(db, expense_id)
    if not expense:
        return None
    return expense_repo.update_expense(db, expense, data)

def delete_expense(db: Session, expense_id: int):
    expense = expense_repo.get_expense_by_id(db, expense_id)
    if not expense:
        return None
    expense_repo.delete_expense(db, expense)
    return True