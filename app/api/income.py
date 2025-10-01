from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeOut
from app.services import income_service
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=IncomeOut)
def create_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return income_service.create_income(db, current_user.id, payload)

@router.get("/", response_model=List[IncomeOut])
def read_income(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    return income_service.get_income(db, user.id)

@router.get("/{income_id}", response_model=IncomeOut)
def read_income(income_id: int, db: Session = Depends(get_db)):
    account = income_service.get_income_by_id(db, income_id)
    if not account:
        raise HTTPException(status_code=404, detail="income not found")
    return account

@router.put("/{income_id}", response_model=IncomeOut)
def update_income(income_id: int, data: IncomeUpdate, db: Session = Depends(get_db)):
    updated = income_service.update_income(db, income_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="income not found")
    return updated

@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    ok = income_service.delete_income(db, income_id)
    if not ok:
        raise HTTPException(status_code=404, detail="income not found")
    return {"detail": "Income deleted successfully"}
