from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # 각 하위 리소스에 대해 back_populates 이름과 맞춰주세요.
    account_books = relationship(
        "AccountBook",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    assets = relationship(
        "Asset",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    incomes = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    goals = relationship(
        "Goal",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # ✅ ChatbotSetting: 1:1(단수명)로 매칭
    chatbot_setting = relationship(
        "ChatbotSetting",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # ✅ ChatbotMessage: 1:N(복수명)로 추가
    chatbot_messages = relationship(
        "ChatbotMessage",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    error_reports = relationship(
        "ErrorReport",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # …추가로 user_id를 FK로 가지는 모델들 모두 같은 패턴으로 등록
    fpti_list = relationship("FPTI", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    fpa_list = relationship("FPA", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    fsd_setting = relationship("FSDSetting", back_populates="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    pattern_setting = relationship("PatternSetting", back_populates="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
