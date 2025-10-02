# app/services/income_service.py
from sqlalchemy.orm import Session
from app.repositories import income_repo 
from app.schemas.income import IncomeCreate, IncomeUpdate

def get_my_income(db: Session, user_id: int):
    return income_repo.get_by_user_id(db, user_id)

def upsert_my_income(db: Session, user_id: int, payload: IncomeCreate | IncomeUpdate):
    return income_repo.upsert_for_user(db, user_id, payload)

def delete_my_income(db: Session, user_id: int) -> bool:
    return income_repo.delete_by_user(db, user_id)
