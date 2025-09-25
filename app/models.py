# app/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserLevel(str, enum.Enum):
    LEVEL1 = "알바 용돈러"
    LEVEL2 = "사회 초년러"
    LEVEL3 = "밸런스러"
    LEVEL4 = "플래너"
    LEVEL5 = "파이낸셜 프리"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # 소비 습관 MBTI 결과
    consumption_mbti = Column(String, index=True, nullable=True)
    
    # 재무 여정 레벨
    financial_level = Column(SQLAlchemyEnum(UserLevel), nullable=True)

    financial_info = relationship("FinancialInfo", back_populates="owner", uselist=False)
    transactions = relationship("Transaction", back_populates="owner")

class FinancialInfo(Base):
    __tablename__ = "financial_info"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    real_estate = Column(Float, default=0.0)
    loans = Column(Float, default=0.0)
    investments = Column(Float, default=0.0)
    deposits = Column(Float, default=0.0)
    monthly_income = Column(Float, default=0.0)
    fixed_expenses = Column(Float, default=0.0)
    
    owner = relationship("User", back_populates="financial_info")

class TransactionType(str, enum.Enum):
    INCOME = "수입"
    EXPENSE = "지출"
    TRANSFER = "이체"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    date = Column(Date)
    type = Column(SQLAlchemyEnum(TransactionType))
    amount = Column(Float)
    category = Column(String, index=True)
    description = Column(String, nullable=True)
    
    owner = relationship("User", back_populates="transactions")