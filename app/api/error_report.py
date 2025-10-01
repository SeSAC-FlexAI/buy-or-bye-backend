from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.init_db import get_db
from app.schemas.error_report import ErrorReportCreate, ErrorReportOut
from app.services import error_report_service

router = APIRouter(tags=["error-report"])

# 오류 저장 (요청 바디에 user_id, message)
@router.post("", response_model=ErrorReportOut)
def create_error_report(
    payload: ErrorReportCreate,
    db: Session = Depends(get_db),
):
    return error_report_service.create(db, payload)

# 사용자별 오류 목록 조회
@router.get("/{user_id}", response_model=List[ErrorReportOut])
def list_error_reports(
    user_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return error_report_service.list_by_user(db, user_id, limit, offset)
