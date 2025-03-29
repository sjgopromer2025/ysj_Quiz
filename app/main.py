from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routers import router as api_router  # 중앙 관리 라우터

app = FastAPI(docs_url="/documentation", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
