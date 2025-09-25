from sqlalchemy.orm import Session
from app.models.budget import Budget

class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: int, category: str, limit_amount: int) -> Budget:
        obj = Budget(owner_id=owner_id, category=category, limit_amount=limit_amount)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_by_owner(self, owner_id: int) -> list[Budget]:
        return self.db.query(Budget).filter(Budget.owner_id == owner_id).all()
