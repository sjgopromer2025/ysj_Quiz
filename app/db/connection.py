import os
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DATABASE_URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 동기식 연결 설정 (SQLAlchemy)
engine = create_engine(DATABASE_URL, echo=False)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DB 세션을 의존성으로 제공하는 함수
def get_db():
    db = session()  # 세션 생성
    try:
        yield db  # 세션을 의존성으로 반환
    finally:
        db.close()  # 세션 종료
