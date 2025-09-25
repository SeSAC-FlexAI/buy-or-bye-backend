# app/schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional
from .models import UserLevel, TransactionType

class TransactionBase(BaseModel):
    date: date
    type: TransactionType
    amount: float
    category: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    consumption_mbti: Optional[str] = None
    financial_level: Optional[UserLevel] = None
    transactions: list[Transaction] = []

    class Config:
        orm_mode = True