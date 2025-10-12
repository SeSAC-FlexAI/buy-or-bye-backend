# app/api/fpti.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_optional, get_current_user
from app.schemas.fpti import FptiCreate, FptiOut
from app.services import fpti_service

router = APIRouter(prefix="/api/fpti", tags=["fpti"])

@router.post("/posts", response_model=FptiOut, response_model_exclude={"result"})
def create_fpti(payload: FptiCreate,
                db: Session = Depends(get_db),
                user = Depends(get_current_user_optional)):
    row = fpti_service.create(db, user, payload)
    return row

@router.get("/me", response_model=FptiOut, response_model_exclude={"result"})
def get_my_fpti(db: Session = Depends(get_db),
                user = Depends(get_current_user)):
    row = fpti_service.get_me(db, user)
    if not row:
        raise HTTPException(status_code=404, detail="결과가 없습니다.")
    return row
