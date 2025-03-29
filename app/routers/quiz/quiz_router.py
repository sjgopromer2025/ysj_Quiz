from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi.responses import HTMLResponse
from app.schemas.quiz import QuizCreate, QuizResponse
from app.services.quiz.quiz_service import QuizService
from app.db.connection import get_db
from app.utils.template_loader import templates, get_template_path

router = APIRouter(prefix="/quiz", tags=["Quiz"])

base_path = "quiz"


# 퀴즈 리스트 (HTML 렌더링)
@router.get("/list", response_class=HTMLResponse)
async def quiz_list(request: Request):
    template_path = get_template_path(base_path, "quiz_list")
    return templates.TemplateResponse(template_path, {"request": request})


# 퀴즈 생성 (HTML 렌더링)
@router.get("/create", response_class=HTMLResponse)
async def quiz_create_page(request: Request):
    template_path = get_template_path(base_path, "quiz_create")
    return templates.TemplateResponse(template_path, {"request": request})


# # 퀴즈 삭제 (HTML 렌더링)
# @router.delete("/delete/{quiz_id}", response_class=HTMLResponse)
# async def quiz_delete(request: Request, quiz_id: int = Path(...)):
#     template_path = get_template_path(base_path, "quiz_delete")
#     return templates.TemplateResponse(template_path, {"request": request})


# # 퀴즈 수정 (HTML 렌더링)
# @router.put("/update/{quiz_id}", response_class=HTMLResponse)
# async def quiz_update(request: Request, quiz_id: int = Path(...)):
#     template_path = get_template_path(base_path, "quiz_update")
#     return templates.TemplateResponse(template_path, {"request": request})


# 퀴즈 생성 API
@router.post("/create", response_model=QuizResponse)
async def quiz_create(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    

):
    """퀴즈 생성 API"""
    quiz_service = QuizService()
    new_quiz = quiz_service.create_quiz(quiz_data, db)
    return new_quiz


# # 퀴즈 목록 조회 API
# @router.get("/quizzes", response_model=List[QuizResponse])
# async def get_quizzes(
#     page: int = Query(1, ge=1),
#     page_size: int = Query(10, ge=1, le=100),
#     db: Session = Depends(get_db),
# ):
#     """퀴즈 목록 조회 API"""
#     quiz_service = QuizService()
#     quizzes = quiz_service.get_quizzes(page, page_size, db)
#     return quizzes


# # 퀴즈 상세 조회 API
# @router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
# async def get_quiz_detail(
#     quiz_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     """퀴즈 상세 조회 API"""
#     quiz_service = QuizService()
#     try:
#         quiz = quiz_service.get_quiz_detail(quiz_id, db)
#         return quiz
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))


# # 퀴즈 응시 API
# @router.post("/quizzes/{quiz_id}/attempt", response_model=QuizResponse)
# async def attempt_quiz(
#     quiz_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     """퀴즈 응시 API"""
#     quiz_service = QuizService()
#     try:
#         quiz = quiz_service.attempt_quiz(quiz_id, db)
#         return quiz
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
