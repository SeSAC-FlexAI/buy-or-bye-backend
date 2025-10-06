# ✅ v2 대응 버전
from pydantic_settings import BaseSettings  # <-- 여기만 바뀜
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./project.db"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "https://buyorbye.co.kr"]
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    OPENAI_API_KEY: str

    DEFAULT_FINANCE_PROMPT: str = """너는 재무 분석가 'Dr. 파이낸스'야.
        나의 재무 상태를 점검하고 개선하고 싶어. 아래 키워드들을 중심으로 나의 재무 관리 방향성에 대해 조언해 줘.
        [키워드]
        - 자산
        - 지출
        - 수입
        - 돈 관리 노하우
        - 가계부 작성 팁
        - 내 연령대 평균 자산 및 소득
        - 현실적인 재무 목표 설정 방법
        - 건강한 1년 자산 추이 그래프의 특징
        각 항목에 대해 어떤 점을 고려해야 하는지, 그리고 어떻게 관리하는 것이 좋은지 일반적인 관점에서 설명해 줘."""
    
    class Config:
        env_file = ".env"

settings = Settings()
