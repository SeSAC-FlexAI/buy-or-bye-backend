# app/schemas/goal.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import date

GoalType = Literal["ASSET", "INCOME", "EXPENSE"]
Period = Literal["MONTHLY", "YEARLY"]

class GoalBase(BaseModel):
    goal_type: GoalType
    period: Period
    year: int
    month: Optional[int] = None
    category: Optional[str] = None
    target_amount: int

    @field_validator("month")
    @classmethod
    def validate_month(cls, v, info):
        period = info.data.get("period")
        if period == "MONTHLY":
            if v is None or not (1 <= v <= 12):
                raise ValueError("month must be 1..12 for MONTHLY goals")
        if period == "YEARLY":
            if v is not None:
                raise ValueError("month must be None for YEARLY goals")
        return v

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    # 키(범위)를 고정하고 금액만 수정하는 용도라면 target_amount만 Optional로 받아도 됨
    # 확장성을 위해 동일 필드 지원 (exclude_unset로 부분 업데이트)
    goal_type: Optional[GoalType] = None
    period: Optional[Period] = None
    year: Optional[int] = None
    month: Optional[int] = None
    category: Optional[str] = None
    target_amount: Optional[int] = None

class GoalOut(GoalBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
