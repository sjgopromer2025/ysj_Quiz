from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from app.routers import router as api_router  # 중앙 관리 라우터
from app.db.connection import engine, Base  # DB 연결
from app.utils.jwt_utils import decode_access_token
import logging


# SQLAlchemy 엔진 로그 수준 설정
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Lifespan을 사용하여 애플리케이션 수명 주기 정의
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행
    Base.metadata.create_all(bind=engine)
    yield  # Lifespan의 시작과 끝을 구분
    # 애플리케이션 종료 시 실행 (필요 시 추가 작업 가능)


app = FastAPI(docs_url="/documentation", redoc_url=None, lifespan=lifespan)


@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    """JWT를 검증하고 사용자 정보를 요청에 추가"""
    token = request.cookies.get("access_token")
    if token:
        user = decode_access_token(token)
        request.state.user = user
    else:
        request.state.user = None

    response = await call_next(request)
    return response


@app.middleware("http")
async def restrict_authenticated_users(request: Request, call_next):
    """로그인된 사용자가 특정 경로에 접근하지 못하도록 제한"""
    token = request.cookies.get("access_token")
    if token:
        user = decode_access_token(token)
        request.state.user = user
    else:
        request.state.user = None

    restricted_paths = ["/member/register", "/member/create"]
    if request.url.path in restricted_paths:
        if request.state.user:  # 로그인된 사용자라면
            return RedirectResponse(url="/", status_code=302)

    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
