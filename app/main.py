# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# API 엔드포인트 예시 (사용자 생성)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # 비밀번호 해싱 등 실제 로직 필요
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=user.password + "_hashed" # 실제로는 해싱 라이브러리 사용
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/")
def read_root():
    return {"message": "서울시 청년 소비 습관 형성 프로젝트 API"}