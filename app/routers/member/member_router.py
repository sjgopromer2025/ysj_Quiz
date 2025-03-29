from fastapi import (
    Depends,
    Path,
    HTTPException,
    APIRouter,
    File,
    UploadFile,
    Form,
    Body,
)
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.services import MemberService
from app.db.connection import get_db
from sqlalchemy.orm import Session

from app.utils.template_loader import templates, get_template_path
from app.utils.jwt_utils import create_access_token

from app.schemas.member import MemberCreate, MemberResponse

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


# 멤버 생성
@router.post("/create", response_class=MemberResponse)
async def member_create(
    request: Request,
    member_data: MemberCreate = Depends(MemberCreate.as_form),
    member_service: MemberService = Depends(get_member_service),
    db: Session = Depends(get_db),
):
    # 유효성 검사 및 회원 생성 로직
    result = member_service.create_member(
        request=request,
        username=member_data.username,
        password=member_data.password,
        user_type=member_data.user_type,
        master_key=member_data.master_key,
        db=db,
    )

    if "template" in result:
        # 에러가 있는 경우 템플릿 렌더링
        return templates.TemplateResponse(result["template"], result["context"])

    # 성공 메시지 반환
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "회원가입 성공!"}
    )


# 로그인
@router.post("/login", response_class=JSONResponse)
async def login(
    request: Request,
    data: dict = Body(...),  # JSON 데이터를 받음
    member_service: MemberService = Depends(get_member_service),
    db: Session = Depends(get_db),
):
    username = data.get("username")
    password = data.get("password")

    result = member_service.login_member(
        username=username,
        password=password,
        db=db,
    )

    # JWT 생성
    token = create_access_token(
        {
            "username": result["user"]["username"],
            "user_type": result["user"]["user_type"],
        }
    )

    response = JSONResponse(
        status_code=200,
        content={
            "message": result["message"],
            "user": result["user"],
        },
    )
    # JWT 쿠키 설정
    response.set_cookie(
        key="access_token", value=token, httponly=True, secure=True, samesite="Strict"
    )

    return response


# 로그아웃
@router.delete("/logout", response_class=JSONResponse)
async def logout(request: Request):
    # 응답 객체 생성
    response = JSONResponse(
        content={"message": "로그아웃되었습니다."},
        status_code=200,
    )

    # access_token 쿠키 삭제
    response.delete_cookie(key="access_token", secure=True, samesite="Strict")

    return response
