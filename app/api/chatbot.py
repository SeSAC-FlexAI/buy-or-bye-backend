from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.init_db import get_db
from app.api.deps import get_current_user, get_current_user_optional
from app.schemas.chatbot import ChatbotRequestIn, ChatbotResponseOut, ChatbotSettingIn, ChatbotSettingOut
from app.services import chatbot_service

router = APIRouter(tags=["chatbot"])

@router.post("/request", response_model=ChatbotResponseOut)
def chatbot_request(
    payload: ChatbotRequestIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_optional),  # 게스트 허용
):
    return chatbot_service.ask(db, user, payload)

@router.get("/response/{message_id}", response_model=ChatbotResponseOut)
def chatbot_response(
    message_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_optional),  # 게스트 메시지는 누구나 조회, 사용자 메시지는 소유자만
):
    res = chatbot_service.get_response(db, user, message_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found or no permission")
    return res

@router.put("/setting", response_model=ChatbotSettingOut)
def chatbot_setting(
    payload: ChatbotSettingIn,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),  # 로그인 필요
):
    return chatbot_service.save_setting(db, user, payload)
