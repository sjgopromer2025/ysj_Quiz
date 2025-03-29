# poetry 관련 명령어

# poetry cache clear --all pypi

# poetry install

#fastapi강제종료
netstat -ano | findstr :8000
taskkill /PID 1234 /F

라이브러리 설치

#웹 관련
fastapi: 웹 프레임워크
uvicorn : FastAPI를 실행할 서버
python-multipart : Form 데이터 처리를 위한 라이브러리

#데이터베이스 관련
psycopg2 : PostgreSQL 연결을 위한 라이브러리
sqlalchemy : ORM을 이용해 데이터베이스와 연동하기 위한 라이브러리
databases : 비동기식 데이터베이스 연결을 위한 라이브러리
pydantic : 모델 검증 및 데이터 직렬화를 위한 라이브러리
