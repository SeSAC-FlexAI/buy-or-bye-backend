# app/services/fpti_service.py
from sqlalchemy.orm import Session
from app.schemas.fpti import FptiCreate, FptiUpdate  # Update는 더 이상 안쓰면 제거 가능
from app.repositories.fpti_repo import fpti_repo
from app.models.user import User

def create(db: Session, user: User | None, payload: FptiCreate):
    user_id = user.id if user else None
    # 게스트 정책이 없다면 user는 필수로 가정
    return fpti_repo.upsert_by_user(db, user_id, payload)

def get_me(db: Session, user: User):
    return fpti_repo.get_by_user_id(db, user.id)
