from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.budget import BudgetCreate, BudgetRead
from app.services.budget_service import create_budget, list_my_budgets

router = APIRouter()

@router.post("/", response_model=BudgetRead)
def create_my_budget(payload: BudgetCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return create_budget(db, payload)

@router.get("/me", response_model=list[BudgetRead])
def get_my_budgets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_my_budgets(db, owner_id=user.id)
