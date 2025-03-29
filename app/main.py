from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routers import router as api_router  # 중앙 관리 라우터
from app.db.connection import engine, Base  # DB 연결
from app.middlewares import (
    add_user_to_request,
    restrict_non_authenticated_users,
    restrict_authenticated_users,
    restrict_non_admin_users,
)
import logging
import secrets  # 안전한 비밀 키 생성을 위한 모듈
import os  # 환경 변수에서 비밀 키 가져오기 위한 모듈


# SQLAlchemy 엔진 로그 수준 설정
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Lifespan을 사용하여 애플리케이션 수명 주기 정의
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행
    Base.metadata.create_all(bind=engine)
    yield  # Lifespan의 시작과 끝을 구분
    # 애플리케이션 종료 시 실행 (필요 시 추가 작업 가능)


app = FastAPI(docs_url="/documentation", redoc_url=None, lifespan=lifespan)

# 미들웨어 등록
app.middleware("http")(add_user_to_request)
app.middleware("http")(restrict_non_authenticated_users)
app.middleware("http")(restrict_authenticated_users)
app.middleware("http")(restrict_non_admin_users)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 환경 변수에서 비밀 키 가져오기 (없으면 기본값 사용)
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

# SessionMiddleware 추가
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="quiz_session",  # 세션 쿠키 이름 설정 (선택 사항)
)

app.include_router(api_router)
