# buy-or-bye-backend
#0
#C:\flexai 경로에서 git clone -> C:\flexai\buy-or-bye-backend
#1 가상환경 생성
python -m venv .venv
#2 가상환경 활성화
.\.venv\Scripts\Activate.ps1
#3 pip upgrade
python.exe -m pip install --upgrade pip
#4 절차
# 1) 설치
pip install -r requirements.txt

# 2) DB 테이블/시드
python -m app.db.init_db

# 3) 실행
uvicorn app.main:app --reload
