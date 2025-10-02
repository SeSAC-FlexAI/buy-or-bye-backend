from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class ExpenseBase(BaseModel):
    date: date
    total_expense: int
    food: int | None = 0
    shopping: int | None = 0
    transportation: int | None = 0
    housing_maintenance: int | None = 0
    culture_leisure: int | None = 0
    household_goods: int | None = 0
    other: int | None = 0

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    total_expense: Optional[int] = None
    food: Optional[int] = None
    shopping: Optional[int] = None
    transportation: Optional[int] = None
    housing_maintenance: Optional[int] = None
    culture_leisure: Optional[int] = None
    household_goods: Optional[int] = None
    other: Optional[int] = None

class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)  # <= v2 방식