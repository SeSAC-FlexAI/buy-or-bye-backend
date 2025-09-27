from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories import chatbot_repo
from app.schemas.chatbot import ChatbotRequestIn, ChatbotSettingIn, ChatbotSettingOut, ChatbotResponseOut

def _mock_answer(question: str, system_prompt: Optional[str], temperature: Optional[float], top_p: Optional[float]) -> str:
    # 간단한 목업: 설정값을 반영해 텍스트 생성 흉내
    prefix = (system_prompt.strip() + "\n\n") if system_prompt else ""
    tail = ""
    if temperature is not None: tail += f"(temp={temperature}) "
    if top_p is not None:       tail += f"(top_p={top_p})"
    return f"{prefix}질문 요약: {question[:120]} ...\n\n이건 목업 응답입니다. {tail}".strip()

def ask(db: Session, current_user: Optional[User], payload: ChatbotRequestIn) -> ChatbotResponseOut:
    uid = current_user.id if current_user else None
    setting = chatbot_repo.get_setting(db, uid) if uid else None

    ans = _mock_answer(
        payload.question,
        setting.system_prompt if setting else None,
        setting.temperature if setting else None,
        setting.top_p if setting else None,
    )

    row = chatbot_repo.create_message(db, uid, payload.question, ans)
    return ChatbotResponseOut(
        message_id=row.message_id,
        question=row.question,
        answer=row.answer,
        created_at=row.created_at,
    )

def get_response(db: Session, current_user: Optional[User], message_id: str) -> Optional[ChatbotResponseOut]:
    row = chatbot_repo.get_message_by_message_id(db, message_id)
    if not row:
        return None
    # 소유권: 사용자 메시지면 본인만. 게스트 메시지는 모두 조회 가능.
    if row.user_id and (not current_user or current_user.id != row.user_id):
        return None
    return ChatbotResponseOut(
        message_id=row.message_id,
        question=row.question,
        answer=row.answer,
        created_at=row.created_at,
    )

def save_setting(db: Session, current_user: User, payload: ChatbotSettingIn) -> ChatbotSettingOut:
    data = payload.model_dump(exclude_unset=True)
    row = chatbot_repo.upsert_setting(db, current_user.id, data)
    return ChatbotSettingOut.model_validate(row)
