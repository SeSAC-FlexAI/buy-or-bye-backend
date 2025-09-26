from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.user_service import authenticate

router = APIRouter()

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    token = authenticate(db, email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": token, "token_type": "bearer"}
