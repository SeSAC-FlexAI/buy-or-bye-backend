# buy-or-bye-backend
# A. 실행 절차
# 1)
 -> C:\flexai 경로에서 git clone -> C:\flexai\buy-or-bye-backend
# 2) 가상환경 생성
python -m venv .venv
# 3) 가상환경 활성화
 -> .\.venv\Scripts\Activate.ps1
# 4) pip upgrade
 -> python.exe -m pip install --upgrade pip
# 5) 설치
pip install -r requirements.txt
# 6) DB 테이블/시드
python -m app.db.init_db
# 7) 서버 실행
uvicorn app.main:app --reload
# 8) API 문서 (테스트)
http://127.0.0.1:8000/docs
