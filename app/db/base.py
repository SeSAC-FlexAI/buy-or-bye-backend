# app/db/base.py
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# ✅ 모델 매핑 등록용 임포트만
from app.models.user import User            # noqa: F401
from app.models.account import AccountBook  # noqa: F401
from app.models.asset import Asset          # noqa: F401
from app.models.fpti import FPTI            # noqa: F401
from app.models.fpa import FPA              # noqa: F401
from app.models.fsd import FSDSetting       # noqa: F401
from app.models.chatbot import ChatbotSetting, ChatbotMessage  # noqa: F401 