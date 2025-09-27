import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models.chatbot import ChatbotSetting, ChatbotMessage

# ── Setting
def get_setting(db: Session, user_id: int) -> Optional[ChatbotSetting]:
    return db.query(ChatbotSetting).filter(ChatbotSetting.user_id == user_id).first()

def upsert_setting(db: Session, user_id: int, data: dict) -> ChatbotSetting:
    row = get_setting(db, user_id)
    if not row:
        row = ChatbotSetting(user_id=user_id)
        db.add(row)
    for k, v in data.items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row

# ── Message
def create_message(db: Session, user_id: Optional[int], question: str, answer: str) -> ChatbotMessage:
    mid = uuid.uuid4().hex
    row = ChatbotMessage(
        user_id=user_id,
        message_id=mid,
        question=question,
        answer=answer,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_message_by_message_id(db: Session, message_id: str) -> Optional[ChatbotMessage]:
    return db.query(ChatbotMessage).filter(ChatbotMessage.message_id == message_id).first()
