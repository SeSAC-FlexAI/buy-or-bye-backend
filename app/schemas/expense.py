from pydantic import BaseModel, ConfigDict, Field
from datetime import date as Date
from typing import Optional

class ExpenseBase(BaseModel):
    date: Date = Field(..., description="집계 일자 (YYYY-MM-DD)")
    total_expense: int = Field(..., description="총지출 합계")
    food: int | None = Field(0, description="식비")
    shopping: int | None = Field(0, description="쇼핑")
    transportation: int | None = Field(0, description="교통")
    housing_maintenance: int | None = Field(0, description="주거/관리비")
    culture_leisure: int | None = Field(0, description="문화/여가")
    household_goods: int | None = Field(0, description="생활용품")
    other: int | None = Field(0, description="기타")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-02",
                "total_expense": 182000,
                "food": 35000,
                "shopping": 20000,
                "transportation": 15000,
                "housing_maintenance": 80000,
                "culture_leisure": 20000,
                "household_goods": 7000,
                "other": 5000
            }
        }
    )

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    date: Optional[Date] = Field(None, description="집계 일자")
    total_expense: Optional[int] = Field(None, description="총지출 합계")
    food: Optional[int] = Field(None, description="식비")
    shopping: Optional[int] = Field(None, description="쇼핑")
    transportation: Optional[int] = Field(None, description="교통")
    housing_maintenance: Optional[int] = Field(None, description="주거/관리비")
    culture_leisure: Optional[int] = Field(None, description="문화/여가")
    household_goods: Optional[int] = Field(None, description="생활용품")
    other: Optional[int] = Field(None, description="기타")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_expense": 190000,
                "transportation": 22000
            }
        }
    )

class ExpenseOut(ExpenseBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 5,
                "user_id": 1,
                "date": "2025-10-02",
                "total_expense": 182000,
                "food": 35000,
                "shopping": 20000,
                "transportation": 15000,
                "housing_maintenance": 80000,
                "culture_leisure": 20000,
                "household_goods": 7000,
                "other": 5000
            }
        }
    )
