# app/schemas/income.py (선택 사항)
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class IncomeBase(BaseModel):
    date: date
    total_income: int
    salary: int | None = 0
    investment_income: int | None = 0
    side_income: int | None = 0

class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    date: Optional[date] = None           # ✅ (선택) 부분 업데이트 허용
    total_income: Optional[int] = None
    salary: Optional[int] = None
    investment_income: Optional[int] = None
    side_income: Optional[int] = None

class IncomeOut(IncomeBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
