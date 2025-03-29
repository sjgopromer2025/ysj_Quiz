from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import router as api_router  # 중앙 관리 라우터
from app.db.connetion import engine, Base  # DB 연결

import logging

# SQLAlchemy 로거 비활성화
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Lifespan을 사용하여 애플리케이션 수명 주기 정의
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행
    Base.metadata.create_all(bind=engine)
    yield  # Lifespan의 시작과 끝을 구분
    # 애플리케이션 종료 시 실행 (필요 시 추가 작업 가능)


app = FastAPI(docs_url="/documentation", redoc_url=None, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
