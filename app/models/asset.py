from sqlalchemy import Column, Integer, ForeignKey, Date, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    total_assets = Column(Integer, nullable=False)
    real_estate = Column(Integer, default=0)
    loans = Column(Integer, default=0)
    deposits_cash = Column(Integer, default=0)
    other_assets = Column(Integer, default=0)

    user = relationship("User", back_populates="assets")