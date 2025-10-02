from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import Optional, Literal
from datetime import date

GoalType = Literal["ASSET", "INCOME", "EXPENSE"]
Period = Literal["MONTHLY", "YEARLY"]

class GoalBase(BaseModel):
    goal_type: GoalType = Field(..., description="목표 유형 (ASSET/INCOME/EXPENSE)")
    period: Period = Field(..., description="집계 주기 (MONTHLY/YEARLY)")
    year: int = Field(..., description="대상 연도")
    month: Optional[int] = Field(None, description="대상 월 (MONTHLY일 때 1~12)")
    category: Optional[str] = Field(None, description="세부 카테고리(선택)")
    target_amount: int = Field(..., description="목표 금액")

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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "goal_type": "EXPENSE",
                "period": "MONTHLY",
                "year": 2025,
                "month": 10,
                "category": "식비",
                "target_amount": 300000
            }
        }
    )

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    goal_type: Optional[GoalType] = Field(None, description="목표 유형")
    period: Optional[Period] = Field(None, description="집계 주기")
    year: Optional[int] = Field(None, description="연도")
    month: Optional[int] = Field(None, description="월 (MONTHLY면 1~12)")
    category: Optional[str] = Field(None, description="카테고리")
    target_amount: Optional[int] = Field(None, description="목표 금액")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "target_amount": 280000
            }
        }
    )

class GoalOut(GoalBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 7,
                "user_id": 1,
                "goal_type": "EXPENSE",
                "period": "MONTHLY",
                "year": 2025,
                "month": 10,
                "category": "식비",
                "target_amount": 300000
            }
        }
    )
