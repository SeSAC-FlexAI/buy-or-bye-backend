from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class AccountBook(Base):
    __tablename__ = "account_books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255))
    amount = Column(Float, nullable=False)

    user = relationship("User", backref="account_books")