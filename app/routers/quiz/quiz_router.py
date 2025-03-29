from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse
from app.schemas.quiz import QuizCreate, QuizResponse, QuestionCreate, QuestionResponse
from app.schemas.quiz import QuizUpdate, QuestionUpdate  # Import necessary schemas
from app.services.quiz.quiz_service import QuizService
from app.db.connection import get_db
from app.utils.template_loader import templates, get_template_path

router = APIRouter(prefix="/quiz", tags=["Quiz"])

base_path = "quiz"


# 의존성으로 MemberService를 주입
def get_quiz_service() -> QuizService:
    return QuizService()


# 퀴즈 리스트 (HTML 렌더링)
@router.get("/list", response_class=HTMLResponse)
async def quiz_list_page(
    request: Request,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 생성 페이지"""
    # 퀴즈 목록 조회
    quizzes = quiz_service.get_all_quizzes_with_question_count(
        db
    )  # Updated service call
    # 퀴즈 목록을 템플릿에 전달
    template_path = get_template_path(base_path, "quiz_list")
    return templates.TemplateResponse(
        template_path, {"request": request, "quizzes": quizzes}
    )


# 퀴즈 생성 (HTML 렌더링)
@router.get("/create", response_class=HTMLResponse)
async def quiz_create_page(
    request: Request,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 생성 페이지"""
    # 퀴즈 목록 조회
    quizzes = quiz_service.get_all_quizzes(db)
    # 퀴즈 목록을 템플릿에 전달
    template_path = get_template_path(base_path, "quiz_create")
    return templates.TemplateResponse(
        template_path, {"request": request, "quizzes": quizzes}
    )


# 퀴즈 생성 API
@router.post("/create", response_model=QuizResponse)
async def create_quiz(
    quiz_data: QuizCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 생성 API"""
    try:
        new_quiz = quiz_service.create_quiz(quiz_data.title, db)
        return new_quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"퀴즈 생성 실패: {str(e)}")


# 퀴즈에 문제 추가 API
@router.post("/create/question")
async def add_question_to_quiz(
    question_data: QuestionCreate,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈에 문제 추가 API"""
    try:
        # 문제를 퀴즈에 추가
        quiz_service.add_question_to_quiz(
            quiz_id=question_data.quiz_id,
            question_data=question_data,
            db=db,
        )
        return {"message": "문제가 성공적으로 추가되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"문제 추가 실패: {str(e)}")


# 퀴즈 수정 (HTML 렌더링)
@router.get("/update/{quiz_id}", response_class=HTMLResponse)
async def quiz_update_page(
    request: Request,
    quiz_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 수정 페이지"""
    try:
        quiz = quiz_service.get_quiz_detail(quiz_id, db)
        template_path = get_template_path(base_path, "quiz_update")
        return templates.TemplateResponse(
            template_path, {"request": request, "quiz": quiz}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"퀴즈 조회 실패: {str(e)}")


# 퀴즈 제목 수정 API
@router.put("/update/{quiz_id}")
async def update_quiz_title(
    quiz_id: int,
    quiz_data: QuizUpdate,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 제목 수정 API"""
    try:
        quiz_service.update_quiz_title(quiz_id, quiz_data.title, db)
        return {"message": "퀴즈 제목이 성공적으로 수정되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"퀴즈 제목 수정 실패: {str(e)}")


# 문제 수정 API
@router.put("/update/question/{question_id}")
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """문제 수정 API"""
    try:
        quiz_service.update_question(question_id, question_data, db)
        return {"message": "문제가 성공적으로 수정되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"문제 수정 실패: {str(e)}")


# 퀴즈 삭제 API
@router.delete("/delete/{quiz_id}")
async def delete_quiz(
    quiz_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 삭제 API"""
    try:
        quiz_service.delete_quiz(quiz_id, db)
        return {"message": "퀴즈가 성공적으로 삭제되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"퀴즈 삭제 실패: {str(e)}")


# # 퀴즈 목록 조회 API
# @router.get("/", response_model=List[QuizResponse])
# async def get_quizzes(
#     page: int = Query(1, ge=1),
#     page_size: int = Query(10, ge=1, le=100),
#     quiz_service: QuizService = Depends(get_quiz_service),
# ):
#     """퀴즈 목록 조회 API"""
#     quizzes = quiz_service.get_quizzes(page, page_size)
#     return quizzes


# # 퀴즈 상세 조회 API
# @router.get("/{quiz_id}", response_model=QuizResponse)
# async def get_quiz_detail(
#     quiz_id: int,
#     quiz_service: QuizService = Depends(get_quiz_service),
# ):
#     """퀴즈 상세 조회 API"""
#     try:
#         quiz = quiz_service.get_quiz_detail(quiz_id)
#         return quiz
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=f"퀴즈 상세 조회 실패: {str(e)}")
