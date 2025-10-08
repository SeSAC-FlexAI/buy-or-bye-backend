from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Literal

GoalType = Literal["ASSET", "INCOME", "EXPENSE"]
Period = Literal["MONTHLY", "YEARLY"]

class GoalBase(BaseModel):
    goal_type: GoalType = Field(..., description="목표 유형 (ASSET/INCOME/EXPENSE)")
    period: Period = Field(..., description="집계 주기 (MONTHLY/YEARLY)")
    year: int = Field(..., ge=1900, description="연도 (예: 2025)")
    month: Optional[int] = Field(None, ge=1, le=12, description="월 (MONTHLY일 때 필수 / YEARLY일 때는 None)")
    category: Optional[str] = Field(None, description="카테고리 (ASSET은 보통 None, INCOME/EXPENSE는 카테고리 단위 목표 권장)")
    target_amount: int = Field(..., ge=0, description="목표 금액")

    @field_validator("month")
    @classmethod
    def validate_month(cls, v, info):
        period = info.data.get("period")
        if period == "MONTHLY" and v is None:
            raise ValueError("MONTHLY 목표는 month가 필요합니다 (1..12).")
        if period == "YEARLY" and v is not None:
            raise ValueError("YEARLY 목표는 month가 없어야 합니다.")
        return v

class GoalCreate(GoalBase):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "goal_type": "EXPENSE",
            "period": "MONTHLY",
            "year": 2025,
            "month": 10,
            "category": "식비",
            "target_amount": 300000
        }
    })

class GoalUpdate(BaseModel):
    target_amount: Optional[int] = Field(None, ge=0, description="목표 금액")
    model_config = ConfigDict(json_schema_extra={
        "example": {"target_amount": 280000}
    })

class GoalOut(GoalBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
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
    })
