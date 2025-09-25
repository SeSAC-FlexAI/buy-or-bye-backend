# app/schemas/budget.py
from pydantic import BaseModel, ConfigDict

class BudgetBase(BaseModel):
    category: str
    limit_amount: int

class BudgetCreate(BudgetBase):
    owner_id: int

class BudgetRead(BudgetBase):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
