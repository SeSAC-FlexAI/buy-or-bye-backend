from typing import Optional
from sqlalchemy.orm import Session
import openai
from app.models.user import User
from app.repositories import chatbot_repo
from app.schemas.chatbot import ChatbotRequestIn, ChatbotSettingIn, ChatbotSettingOut, ChatbotResponseOut
from app.core.config import settings  
from pinecone import Pinecone
import os

client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)  # 설정에서 인덱스명 가져오기

async def _search_pinecone(question: str, top_k: int = 5) -> str:
    """Pinecone에서 관련 정책 정보를 검색"""
    try:
        # Pinecone에서 텍스트로 검색 (integrated embedding 사용)
        results = index.search(
            namespace="policy",  # 정책 관련 네임스페이스
            query={
                "inputs": {"text": question},
                "top_k": top_k
            },
            fields=["text", "title", "category"]  # 반환할 필드
        )
        
        # 검색 결과를 컨텍스트로 조합
        context_parts = []
        for hit in results.get('result', {}).get('hits', []):
            fields = hit.get('fields', {})
            title = fields.get('title', '')
            text = fields.get('text', '')
            if title and text:
                context_parts.append(f"제목: {title}\n내용: {text}")
        
        return "\n\n".join(context_parts) if context_parts else "관련 정책 정보를 찾을 수 없습니다."
        
    except Exception as e:
        print(f"Pinecone search error: {e}")
        return "정책 정보 검색 중 오류가 발생했습니다."

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

async def ask(db: Session, current_user: Optional[User], payload: ChatbotRequestIn) -> ChatbotResponseOut:
    uid = current_user.id if current_user else None
    setting = chatbot_repo.get_setting(db, uid) if uid else None

    # 기존 _get_openai_response 대신 새로운 함수 사용
    ans = await _get_response_with_context(
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


async def _get_response_with_context(question: str, system_prompt: Optional[str], temperature: Optional[float], top_p: Optional[float]) -> str:
    """질문에 '정책' 키워드가 포함되면 Pinecone 검색, 아니면 일반 OpenAI 응답"""
    
    # '정책' 키워드 검사 (대소문자 무관)
    if '정책' in question.lower():
        # Pinecone에서 관련 정책 정보 검색
        policy_context = await _search_pinecone(question)
        
        # 정책 정보를 포함한 시스템 프롬프트 생성
        policy_system_prompt = f"""
당신은 서울시 청년 재무 관리 전문 상담사입니다. 
1. 친구처럼 친근하게 답변해주세요.
2. 다음 정책 정보를 바탕으로 사용자의 질문에 답변해주세요.
정책 정보:
{policy_context}
위 정보를 바탕으로 정확하고 도움이 되는 답변을 제공해주세요.
"""
        messages = [
            {"role": "system", "content": policy_system_prompt},
            {"role": "user", "content": question}
        ]
    else:
        # 일반적인 OpenAI 응답
        final_system_prompt = system_prompt or settings.DEFAULT_FINANCE_PROMPT
        messages = [
            {"role": "system", "content": final_system_prompt},
            {"role": "user", "content": question}
        ]

    try:
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500,
            temperature=temperature if temperature is not None else 0.7,
            top_p=top_p if top_p is not None else 1.0,
        )
        return completion.choices[0].message.content or "죄송합니다, 응답을 생성할 수 없습니다."
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "죄송합니다, 현재 서비스에 일시적인 문제가 있습니다. 잠시 후 다시 시도해주세요."


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
