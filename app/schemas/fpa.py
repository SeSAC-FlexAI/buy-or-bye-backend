# app/schemas/fpa.py
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional, Any

class FpaCreate(BaseModel):
    snapshot_date: date
    assets_total: float
    debts_total: float
    detail: Optional[Any] = None

    @field_validator("assets_total", "debts_total")
    @classmethod
    def non_negative(cls, v): 
        if v < 0: raise ValueError("must be >= 0")
        return v

class FpaOut(BaseModel):
    id: int
    user_id: int
    snapshot_date: date
    assets_total: float
    debts_total: float
    net_worth: float
    detail: Optional[Any] = None
    
    model_config = ConfigDict(from_attributes=True)
