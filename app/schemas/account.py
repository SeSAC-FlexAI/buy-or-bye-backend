from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class AccountBase(BaseModel):
    date: date
    category: str
    description: Optional[str] = None
    amount: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None

class AccountOut(AccountBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)  # <= v2 방식
