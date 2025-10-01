# app/services/income_service.py
from sqlalchemy.orm import Session
from app.repositories import income_repo 
from app.schemas.income import IncomeCreate, IncomeUpdate

def create_income(db: Session, user_id: int, income: IncomeCreate):
    return income_repo.create_income(db, user_id, income)

def get_income(db: Session, user_id: int):
    return income_repo.get_income(db, user_id)

def get_income_by_id(db: Session, income_id: int):
    return income_repo.get_income_by_id(db, income_id)

def update_income(db: Session, income_id: int, data: IncomeUpdate):
    income = income_repo.get_income_by_id(db, income_id)
    if not income:
        return None
    return income_repo.update_income(db, income, data)

def delete_income(db: Session, income_id: int):
    income = income_repo.get_income_by_id(db, income_id)
    if not income:
        return None
    income_repo.delete_income(db, income)
    return True