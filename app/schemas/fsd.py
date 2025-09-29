from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List
from datetime import date

class FsdSettingIn(BaseModel):
    goal_name: Optional[str] = None
    target_amount: Optional[float] = None
    target_date: Optional[date] = None
    monthly_saving: Optional[float] = None

class FsdSettingOut(FsdSettingIn):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class CategorySummary(BaseModel):
    category: str
    amount: float

class FpaBrief(BaseModel):
    snapshot_date: Optional[date] = None
    net_worth: Optional[float] = None

class FsdHomeOut(BaseModel):
    year: int
    month: int
    income_total: float
    expense_total: float
    balance: float
    top_categories: List[CategorySummary]
    latest_fpa: FpaBrief
    goal_progress: Optional[float] = None  # 0~1 (None이면 계산 불가)
    setting: Optional[FsdSettingOut] = None
