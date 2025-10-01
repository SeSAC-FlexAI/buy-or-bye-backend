from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class AccountBook(Base):
    __tablename__ = "account_books"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)  # 수입:+ / 지출:-
    method = Column(String(50), nullable=True)  # ✅ 추가 (결제수단 등)

    user = relationship("User", back_populates="account_books")
