from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.utils.template_loader import templates
from app.routers.quiz import quiz_router
from app.routers.member import member_router


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 각 모듈의 라우터를 등록
router.include_router(quiz_router.router)
router.include_router(member_router.router)
