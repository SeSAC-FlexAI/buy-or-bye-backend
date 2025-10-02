from sqlalchemy import Column, Integer, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    total_income = Column(Integer, nullable=False)
    salary = Column(Integer, default=0)
    investment_income = Column(Integer, default=0)
    side_income = Column(Integer, default=0)

    user = relationship("User", back_populates="income")