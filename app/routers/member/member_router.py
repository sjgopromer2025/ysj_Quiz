from fastapi import Depends, Path, HTTPException, APIRouter, File, UploadFile, Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.utils.template_loader import templates, get_template_path
from app.services import MemberService


router = APIRouter(prefix="/member", tags=["Member"])


base_path = "member"


# 의존성으로 MemberService를 주입
def get_member_service() -> MemberService:
    return MemberService()


# 회원가입
@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    template_path = get_template_path("register", "register")
    return templates.TemplateResponse(template_path, {"request": request})


@router.post("/create", response_class=HTMLResponse)
async def member_create(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    # email: str = Form(...),
    user_type: str = Form(...),
    master_key: str = Form(None),  # 관리자가 아닌 경우 입력 안 해도 됨
    member_service: MemberService = Depends(get_member_service),
):

    result = member_service.create_member(
        username=username,
        password=password,
        # email=email,
        user_type=user_type,
        master_key=master_key,
    )

    # 회원가입이 성공하면 index.html 반환
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "회원가입 성공!"}
    )
