# app/api/expense.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut
from app.services import expense_service
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=ExpenseOut | None)
def read_my_expense(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return expense_service.get_my_expense(db, user.id)

@router.post("/me", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_or_replace_my_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return expense_service.upsert_my_expense(db, user.id, payload)

@router.put("/me", response_model=ExpenseOut)
def update_my_expense(
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return expense_service.upsert_my_expense(db, user.id, payload)

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_expense(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    ok = expense_service.delete_my_expense(db, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="expense not found")
    return {"success": True}
