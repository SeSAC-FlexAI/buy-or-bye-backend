# app/schemas/asset.py
from pydantic import BaseModel, ConfigDict
from datetime import date as Date
from typing import Optional

class AssetBase(BaseModel):
    date: Date
    total_assets: float
    real_estate: float = 0
    loans: float = 0
    deposits_cash: float = 0
    other_assets: float = 0

class AssetCreate(AssetBase): ...
class AssetUpdate(BaseModel):
    date: Optional[Date] = None
    total_assets: Optional[float] = None
    real_estate: Optional[float] = None
    loans: Optional[float] = None
    deposits_cash: Optional[float] = None
    other_assets: Optional[float] = None

class AssetOut(AssetBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
