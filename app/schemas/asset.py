from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class AssetBase(BaseModel):
    date: date
    total_assets: int
    real_estate: int | None = 0
    loans: int | None = 0
    deposits_cash: int | None = 0
    other_assets: int | None = 0

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    total_assets: Optional[int] = None
    real_estate: Optional[int] = None
    loans: Optional[int] = None
    deposits_cash: Optional[int] = None
    other_assets: Optional[int] = None

class AssetOut(AssetBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)  # <= v2 방식