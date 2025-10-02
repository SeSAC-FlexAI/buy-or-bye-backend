# app/models/account.py (예시)
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class AccountBook(Base):
    __tablename__ = "account_books"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # ★ 핵심
        nullable=False,
        index=True,
    )
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    amount = Column(Float, nullable=False)
    method = Column(String)

    user = relationship("User", back_populates="account_books")  # ★ 이름 매칭
