from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ChatbotSettingIn(BaseModel):
    system_prompt: Optional[str] = None
    temperature:   Optional[float] = Field(default=None, ge=0, le=2)
    top_p:         Optional[float] = Field(default=None, ge=0, le=1)

class ChatbotSettingOut(ChatbotSettingIn):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class ChatbotRequestIn(BaseModel):
    question: str

class ChatbotResponseOut(BaseModel):
    message_id: str
    question: str
    answer: str
    created_at: datetime
