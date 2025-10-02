from typing import Optional
from sqlalchemy.orm import Session
import openai
from app.models.user import User
from app.repositories import chatbot_repo
from app.schemas.chatbot import ChatbotRequestIn, ChatbotSettingIn, ChatbotSettingOut, ChatbotResponseOut
from app.core.config import settings  

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _get_openai_response(question: str, system_prompt: Optional[str], temperature: Optional[float], top_p: Optional[float]) -> str:
    # 프론트엔드 코드와 유사하게 시스템 프롬프트 설정
    # 설정값이 없으면 기본 프롬프트를 사용합니다.
    final_system_prompt = system_prompt or settings.DEFAULT_FINANCE_PROMPT
    
    messages = [
        {"role": "system", "content": final_system_prompt},
        {"role": "user", "content": question}
    ]

    try:
        # OpenAI API 호출
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500,
            # 사용자 설정값 우선, 없으면 기본값 사용
            temperature=temperature if temperature is not None else 0.7,
            top_p=top_p if top_p is not None else 1.0,
        )
        return completion.choices[0].message.content or "죄송합니다, 응답을 생성할 수 없습니다."
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "죄송합니다, 현재 서비스에 일시적인 문제가 있습니다. 잠시 후 다시 시도해주세요."

def _mock_answer(question: str, system_prompt: Optional[str], temperature: Optional[float], top_p: Optional[float]) -> str:
    # 간단한 목업: 설정값을 반영해 텍스트 생성 흉내
    prefix = (system_prompt.strip() + "\n\n") if system_prompt else ""
    tail = ""
    if temperature is not None: tail += f"(temp={temperature}) "
    if top_p is not None:       tail += f"(top_p={top_p})"
    return f"{prefix}질문 요약: {question[:120]} ...\n\n이건 목업 응답입니다. {tail}".strip()

async def ask(db: Session, current_user: Optional[User], payload: ChatbotRequestIn) -> ChatbotResponseOut:
    uid = current_user.id if current_user else None
    setting = chatbot_repo.get_setting(db, uid) if uid else None

    ans = await _get_openai_response(
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
