from sqlalchemy.orm import Session
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate

def create_income(db: Session, user_id: int, data: IncomeCreate):
    income = Income(user_id=user_id, **data.dict())
    db.add(income)
    db.commit()
    db.refresh(income)
    return income

def get_income(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).all()

def get_income_by_id(db: Session, income_id: int):
    return db.query(Income).filter(Income.id == income_id).first()

def update_income(db: Session, income: Income, data: IncomeUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(income, key, value)
    db.commit()
    db.refresh(income)
    return income

def delete_account(db: Session, income: Income):
    db.delete(income)
    db.commit()
