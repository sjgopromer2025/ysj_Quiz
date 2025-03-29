from fastapi import Depends, Path, HTTPException, APIRouter, File, UploadFile, Form
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.utils.template_loader import templates, get_template_path


router = APIRouter(prefix="/quiz", tags=["Quiz"])


base_path = "quiz"


# 퀴즈 리스트
@router.get("/list", response_class=HTMLResponse)
async def quiz_list(request: Request):
    template_path = get_template_path(base_path, "quiz_list")
    return templates.TemplateResponse(template_path, {"request": request})


# 퀴즈 생성
@router.get("/create", response_class=HTMLResponse)
async def quiz_create(request: Request):
    template_path = get_template_path(base_path, "quiz_create")
    return templates.TemplateResponse(template_path, {"request": request})


# 퀴즈 삭제
@router.delete("/delete/{quiz_id}", response_class=HTMLResponse)
async def quiz_delete(request: Request, quiz_id: int = Path(...)):
    template_path = get_template_path(base_path, "quiz_delete")
    return templates.TemplateResponse(template_path, {"request": request})


# 퀴즈 수정
@router.put("/update/{quiz_id}", response_class=HTMLResponse)
async def quiz_update(request: Request, quiz_id: int = Path(...)):
    template_path = get_template_path(base_path, "quiz_update")
    return templates.TemplateResponse(template_path, {"request": request})
