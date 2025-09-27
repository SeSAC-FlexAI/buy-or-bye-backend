from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List
from datetime import date

class PatternSettingIn(BaseModel):
    monthly_budget: Optional[float] = None
    rules: Optional[dict] = None  # {"키워드": "카테고리", ...}

class PatternSettingOut(PatternSettingIn):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryAgg(BaseModel):
    category: str
    amount: float         # 지출이면 양수(절대값), 수입은 양수
    ratio: float          # 0~1 (카테고리 금액 / 해당 그룹 합계)

class DayPoint(BaseModel):
    d: date
    income: float
    expense: float        # 양수(절대값)

class PatternOut(BaseModel):
    year: int
    month: int
    income_total: float
    expense_total: float       # 양수(절대값)
    top_categories: List[CategoryAgg]
    categories: List[CategoryAgg]
    daily_series: List[DayPoint]
    monthly_budget: Optional[float] = None
