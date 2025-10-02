# app/api/income.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeOut
from app.services import income_service
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=IncomeOut | None)
def read_my_income(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return income_service.get_my_income(db, user.id)

@router.post("/me", response_model=IncomeOut, status_code=status.HTTP_201_CREATED)
def create_or_replace_my_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return income_service.upsert_my_income(db, user.id, payload)

@router.put("/me", response_model=IncomeOut)
def update_my_income(
    payload: IncomeUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return income_service.upsert_my_income(db, user.id, payload)

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_income(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    ok = income_service.delete_my_income(db, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="income not found")
    return {"success": True}
