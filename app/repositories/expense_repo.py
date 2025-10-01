from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

def create_expense(db: Session, user_id: int, data: ExpenseCreate):
    expense = Expense(user_id=user_id, **data.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expense(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()

def get_expense_by_id(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def update_expense(db: Session, expense: Expense, data: ExpenseUpdate):
    for key, value in data.dict(exclude_unset=True).items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense

def delete_account(db: Session, expense: Expense):
    db.delete(expense)
    db.commit()
