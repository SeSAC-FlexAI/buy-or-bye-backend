from pydantic import BaseModel, ConfigDict, Field
from datetime import date as Date
from typing import Optional

class IncomeBase(BaseModel):
    date: Date = Field(..., description="집계 일자 (YYYY-MM-DD)")
    total_income: int = Field(..., description="총수입 합계")
    salary: int | None = Field(0, description="급여")
    investment_income: int | None = Field(0, description="투자수입")
    side_income: int | None = Field(0, description="부수입")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-02",
                "total_income": 3500000,
                "salary": 3000000,
                "investment_income": 300000,
                "side_income": 200000
            }
        }
    )

class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    date: Optional[Date] = Field(None, description="집계 일자")
    total_income: Optional[int] = Field(None, description="총수입 합계")
    salary: Optional[int] = Field(None, description="급여")
    investment_income: Optional[int] = Field(None, description="투자수입")
    side_income: Optional[int] = Field(None, description="부수입")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_income": 3600000,
                "side_income": 250000
            }
        }
    )

class IncomeOut(IncomeBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 4,
                "user_id": 1,
                "date": "2025-10-02",
                "total_income": 3500000,
                "salary": 3000000,
                "investment_income": 300000,
                "side_income": 200000
            }
        }
    )
