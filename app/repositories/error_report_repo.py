from typing import List
from sqlalchemy.orm import Session
from app.models.error_report import ErrorReport

def create(db: Session, user_id: int, message: str) -> ErrorReport:
    # ⚠️ 절대 db.add(payload) 하면 안 됨 (payload는 Pydantic, 매핑 안 됨)
    row = ErrorReport(user_id=user_id, message=message)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def list_by_user(db: Session, user_id: int, limit: int = 50, offset: int = 0) -> List[ErrorReport]:
    return (
        db.query(ErrorReport)
        .filter(ErrorReport.user_id == user_id)
        .order_by(ErrorReport.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
