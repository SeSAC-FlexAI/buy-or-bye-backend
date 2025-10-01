from typing import List
from sqlalchemy.orm import Session
from app.schemas.error_report import ErrorReportCreate, ErrorReportOut
from app.repositories import error_report_repo

def create(db: Session, payload: ErrorReportCreate) -> ErrorReportOut:
    row = error_report_repo.create(db, payload.user_id, payload.message)
    return ErrorReportOut.model_validate(row)


def list_by_user(db: Session, user_id: int, limit: int, offset: int) -> List[ErrorReportOut]:
    rows = error_report_repo.list_by_user(db, user_id, limit, offset)
    return [ErrorReportOut.model_validate(r) for r in rows]


