from pydantic import BaseModel, ConfigDict, Field
from datetime import date as Date
from typing import Optional

class AssetBase(BaseModel):
    date: Date = Field(..., description="측정 일자 (YYYY-MM-DD)")
    total_assets: float = Field(..., description="총자산 (부채 반영)")
    real_estate: float = Field(0, description="부동산")
    loans: float = Field(0, description="부채(대출)")
    deposits_cash: float = Field(0, description="현금/예금")
    other_assets: float = Field(0, description="기타자산")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-02",
                "total_assets": 125000000.0,
                "real_estate": 90000000.0,
                "loans": 30000000.0,
                "deposits_cash": 12000000.0,
                "other_assets": 3000000.0,
            }
        }
    )

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    date: Optional[Date] = Field(None, description="측정 일자")
    total_assets: Optional[float] = Field(None, description="총자산")
    real_estate: Optional[float] = Field(None, description="부동산")
    loans: Optional[float] = Field(None, description="부채(대출)")
    deposits_cash: Optional[float] = Field(None, description="현금/예금")
    other_assets: Optional[float] = Field(None, description="기타자산")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_assets": 126000000.0,
                "deposits_cash": 13000000.0
            }
        }
    )

class AssetOut(AssetBase):
    id: int
    user_id: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 10,
                "user_id": 1,
                "date": "2025-10-02",
                "total_assets": 125000000.0,
                "real_estate": 90000000.0,
                "loans": 30000000.0,
                "deposits_cash": 12000000.0,
                "other_assets": 3000000.0,
            }
        }
    )
