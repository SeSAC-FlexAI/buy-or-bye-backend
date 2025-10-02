# app/schemas/expense.py
from pydantic import BaseModel, ConfigDict
from datetime import date as Date
from typing import Optional

class ExpenseBase(BaseModel):
    date: Date
    total_expense: int
    food: int | None = 0
    shopping: int | None = 0
    transportation: int | None = 0
    housing_maintenance: int | None = 0
    culture_leisure: int | None = 0
    household_goods: int | None = 0  # ✅ 변경
    other: int | None = 0

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    date: Optional[Date] = None
    total_expense: Optional[int] = None
    food: Optional[int] = None
    shopping: Optional[int] = None
    transportation: Optional[int] = None
    housing_maintenance: Optional[int] = None
    culture_leisure: Optional[int] = None
    household_goods: Optional[int] = None  # ✅ 변경
    other: Optional[int] = None

class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
