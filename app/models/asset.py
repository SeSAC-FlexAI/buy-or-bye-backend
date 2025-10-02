# app/models/asset.py
from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("user_id", name="uq_assets_user"),)  # ✅ 사용자당 1건 보장

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)

    total_assets = Column(Integer, nullable=False)
    real_estate = Column(Integer, default=0)
    loans = Column(Integer, default=0)
    deposits_cash = Column(Integer, default=0)
    other_assets = Column(Integer, default=0)

    user = relationship("User", back_populates="assets")
