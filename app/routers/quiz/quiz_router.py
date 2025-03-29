from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Path,
    Request,
    Response,
    Body,
)
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse
from app.schemas.quiz import QuizCreate, QuizResponse, QuestionCreate, QuestionResponse
from app.schemas.quiz import (
    QuizUpdate,
    QuestionUpdate,
)
from app.services.quiz.quiz_service import QuizService
from app.db.connection import get_db
from app.utils.template_loader import templates, get_template_path
from app.utils.session_utils import get_session, set_session, delete_session
from app.schemas.quiz import QuizSubmissionRequest, QuizSubmissionResponse

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


@router.delete("/delete/question/{question_id}")
async def delete_question(
    question_id: int,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """문제 삭제 API"""
    try:
        quiz_service.delete_question(question_id, db)
        return {"message": "문제가 성공적으로 삭제되었습니다."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"문제 삭제 실패: {str(e)}")


# 퀴즈 응시 API
@router.get("/detail/{quiz_id}", response_class=HTMLResponse)
async def get_quiz_detail(
    request: Request,
    quiz_id: int,
    response: Response,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 상세 조회 및 세션 데이터 활용"""
    try:
        # 세션 키 생성
        user = request.state.user
        if not user:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
        session_key = f"{user['username']}_quiz_{quiz_id}_state"

        # 세션 데이터 확인
        quiz_state = get_session(request, session_key)
        if not quiz_state or quiz_state.quiz_id is None:
            # 세션에 데이터가 없으면 새로 생성
            quiz = quiz_service.get_quiz_detail_suffle(quiz_id, db)
            quiz_state = {
                "quiz_id": quiz.id,
                "quiz_title": quiz.title,
                "questions": [question.model_dump() for question in quiz.questions],
                "selected_options": {},  # 초기 선택 상태
            }
            set_session(request, response, session_key, quiz_state)

        # 템플릿에 전달할 데이터 구성
        return templates.TemplateResponse(
            get_template_path(base_path, "quiz_detail"),
            {
                "request": request,
                "quiz_id": quiz_state["quiz_id"],
                "quiz_title": quiz_state["quiz_title"],
                "questions": quiz_state["questions"],
                "selected_options": quiz_state["selected_options"],
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"퀴즈 상세 조회 실패: {str(e)}")


@router.post("/attempt/{quiz_id}/save")
async def save_quiz_state(
    quiz_id: int,
    request: Request,
    response: Response,
    quiz_state: dict = Body(...),  # Explicitly parse the incoming JSON
):
    """사용자가 풀고 있는 문제 상태를 세션에 저장"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # 세션 키 생성
    session_key = f"{user['username']}_quiz_{quiz_id}_state"

    # 세션 데이터 가져오기
    session_data = get_session(request, session_key) or {}
    # print("기존 세션 데이터:", session_data)  # 디버깅용 출력

    # 세션 데이터가 없으면 기본값 설정
    if "quiz_id" not in session_data:
        session_data["quiz_id"] = quiz_id
        session_data["selected_options"] = {}

    # 선택 상태 업데이트
    selected_options = quiz_state.get("selected_options", {})
    # print("클라이언트에서 전달된 선택 상태:", selected_options)  # 디버깅용 출력

    # 기존 선택 상태와 병합
    session_data["selected_options"].update(selected_options)
    # print("업데이트된 세션 데이터:", session_data)  # 디버깅용 출력

    # 세션에 저장
    set_session(request, response, session_key, session_data)

    return {"message": "퀴즈 상태가 성공적으로 저장되었습니다."}


@router.post("/submit/{quiz_id}", response_model=QuizSubmissionResponse)
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmissionRequest,
    request: Request,
    response: Response,
    quiz_service: QuizService = Depends(get_quiz_service),
    db: Session = Depends(get_db),
):
    """퀴즈 답안 제출 및 채점 API"""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    # 세션에서 퀴즈 상태 가져오기
    session_key = f"{user['username']}_quiz_{quiz_id}_state"
    quiz_state = get_session(request, session_key)
    if not quiz_state:
        raise HTTPException(status_code=400, detail="퀴즈 상태가 유효하지 않습니다.")
    # 답안 제출 및 결과 계산
    result = quiz_service.submit_quiz_answers(quiz_id, submission.answers, user, db)
    # print("제출 결과:", result)

    # 제출 데이터를 저장
    try:
        quiz_service.save_quiz_submission(quiz_id, user, submission.answers, result, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"퀴즈 제출 저장 실패: {str(e)}")

    # 제출 후 세션 데이터 삭제

    # 세션 데이터 삭제
    delete_session(request, key=session_key)
    # print("Session after deletion:", get_session(request, session_key))  # 디버깅용 출력

    return result
