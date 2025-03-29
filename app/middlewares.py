from fastapi import Request
from fastapi.responses import RedirectResponse
from app.utils.jwt_utils import decode_access_token


async def set_user_from_token(request: Request):
    """요청에서 JWT 토큰을 추출하고 사용자 정보를 설정"""
    token = request.cookies.get("access_token")
    if token:
        user = decode_access_token(token)
        request.state.user = user
    else:
        request.state.user = None


async def add_user_to_request(request: Request, call_next):
    """JWT를 검증하고 사용자 정보를 요청에 추가"""
    await set_user_from_token(request)
    response = await call_next(request)
    return response


async def restrict_non_authenticated_users(request: Request, call_next):
    """로그인하지 않은 사용자가 특정 경로에 접근하지 못하도록 제한"""
    await set_user_from_token(request)

    restricted_paths = [
        "/quiz/detail",
        "/quiz/list",
        "/quiz/submit",
        "/quiz/attempt",
    ]
    if any(request.url.path.startswith(path) for path in restricted_paths):
        user = request.state.user
        if not user:  # 로그인하지 않은 경우
            return RedirectResponse(url="/", status_code=302)

    response = await call_next(request)
    return response


async def restrict_authenticated_users(request: Request, call_next):
    """로그인된 사용자가 특정 경로에 접근하지 못하도록 제한"""
    await set_user_from_token(request)

    restricted_paths = ["/member/register", "/member/create"]
    if request.url.path in restricted_paths:
        if request.state.user:  # 로그인된 사용자라면
            return RedirectResponse(url="/", status_code=302)

    response = await call_next(request)
    return response


async def restrict_non_admin_users(request: Request, call_next):
    """관리자가 아닌 사용자가 수정, 삭제, 생성 관련 API에 접근하지 못하도록 제한"""
    restricted_paths = [
        "/quiz/create",
        "/quiz/create/question",
        "/quiz/update",
        "/quiz/delete",
    ]
    await set_user_from_token(request)

    if any(request.url.path.startswith(path) for path in restricted_paths):
        user = request.state.user
        if not user or user.get("user_type") != "admin":  # 관리자가 아닌 경우
            return RedirectResponse(url="/", status_code=302)

    response = await call_next(request)
    return response
