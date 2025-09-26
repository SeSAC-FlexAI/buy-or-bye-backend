# buy-or-bye-backend
a)
#C:\flexai 경로에서 git clone -> C:\flexai\buy-or-bye-backend
b) 가상환경 생성
python -m venv .venv
c) 가상환경 활성화
.\.venv\Scripts\Activate.ps1
d) pip upgrade
python.exe -m pip install --upgrade pip
#4 절차
# 1) 설치
pip install -r requirements.txt

# 2) DB 테이블/시드
python -m app.db.init_db

# 3) 실행
uvicorn app.main:app --reload

# 4) API 문서 (테스트)
http://127.0.0.1:8000/docs
