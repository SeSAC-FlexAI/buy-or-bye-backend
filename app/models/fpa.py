from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class FPA(Base):
    __tablename__ = "fpa"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    snapshot_date = Column(Date, nullable=False)   # 스냅샷 기준일
    assets_total = Column(Float, nullable=False, default=0)
    debts_total  = Column(Float, nullable=False, default=0)
    net_worth    = Column(Float, nullable=False, default=0)  # = assets_total - debts_total

    # 세부 항목(자산/부채 breakdown)을 JSON 문자열로 보관 (선택)
    detail_json  = Column(Text, nullable=True)

    user = relationship("User", back_populates="fpa_list")
