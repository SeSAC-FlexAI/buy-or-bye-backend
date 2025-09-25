# ✅ v2 대응 버전
from pydantic_settings import BaseSettings  # <-- 여기만 바뀜
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./project.db"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
