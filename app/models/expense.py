from sqlalchemy import Column, Integer, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    total_expense = Column(Integer, nullable=False)
    food = Column(Integer, default=0)
    shopping = Column(Integer, default=0)
    transportation = Column(Integer, default=0)
    housing_maintenance = Column(Integer, default=0)
    culture_leisure = Column(Integer, default=0)
    cosmetics = Column(Integer, default=0)
    other = Column(Integer, default=0)

    user = relationship("User", back_populates="expense")