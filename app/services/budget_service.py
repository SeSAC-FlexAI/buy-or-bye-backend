from sqlalchemy.orm import Session
from app.repositories.budget_repo import BudgetRepository
from app.schemas.budget import BudgetCreate

def create_budget(db: Session, payload: BudgetCreate):
    repo = BudgetRepository(db)
    return repo.create(owner_id=payload.owner_id, category=payload.category, limit_amount=payload.limit_amount)

def list_my_budgets(db: Session, owner_id: int):
    repo = BudgetRepository(db)
    return repo.list_by_owner(owner_id)
