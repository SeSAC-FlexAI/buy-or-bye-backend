from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut
from app.services import expense_service
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=ExpenseOut)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return expense_service.create_expense(db, current_user.id, payload)

@router.get("/", response_model=List[ExpenseOut])
def read_expense(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return expense_service.get_expense(db, user.id)

@router.get("/{expense_id}", response_model=ExpenseOut)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    account = expense_service.get_expense_by_id(db, expense_id)
    if not account:
        raise HTTPException(status_code=404, detail="expense not found")
    return account

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, data: ExpenseUpdate, db: Session = Depends(get_db)):
    updated = expense_service.update_expense(db, expense_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="expense not found")
    return updated

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    ok = expense_service.delete_expense(db, expense_id)
    if not ok:
        raise HTTPException(status_code=404, detail="expense not found")
    return {"detail": "Expense deleted successfully"}
