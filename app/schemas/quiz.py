from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class OptionCreate(BaseModel):
    """선택지 생성 요청"""

    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    """문제 생성 요청"""

    quiz_id: int  # 문제를 추가할 퀴즈의 ID
    text: str
    options: List[OptionCreate] = Field(..., min_items=2)  # 최소 2개 이상의 선택지 필요

    # 정답 검증: 최소 1개의 정답이 존재해야 함
    @field_validator("options")
    @classmethod
    def validate_options(cls, options: List[OptionCreate]):
        if not any(option.is_correct for option in options):
            raise ValueError("각 문제에는 최소 1개의 정답이 포함되어야 합니다.")
        return options


class QuestionUpdate(BaseModel):
    """문제 수정 요청"""

    text: str
    options: List[OptionCreate] = Field(..., min_items=2)  # 최소 2개 이상의 선택지 필요

    # 정답 검증: 최소 1개의 정답이 존재해야 함
    @field_validator("options")
    @classmethod
    def validate_options(cls, options: List[OptionCreate]):
        if not any(option.is_correct for option in options):
            raise ValueError("각 문제에는 최소 1개의 정답이 포함되어야 합니다.")
        return options


class OptionResponse(BaseModel):
    """선택지 응답 모델"""

    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True  # 변경된 설정


class QuestionResponse(BaseModel):
    """문제 응답 모델"""

    id: int
    text: str
    options: List[OptionResponse]  # 문제에 포함된 선택지 목록

    class Config:
        from_attributes = True  # 변경된 설정


class QuizCreate(BaseModel):
    """퀴즈 생성 요청"""

    title: str
    questions: Optional[List[QuestionCreate]] = None  # 문제는 선택적으로 포함


class QuizUpdate(BaseModel):
    """퀴즈 수정 요청"""

    title: Optional[str] = None  # 제목은 선택적으로 수정 가능
    questions: Optional[List[QuestionUpdate]] = None  # 문제도 선택적으로 수정 가능


class QuizDelete(BaseModel):
    """퀴즈 삭제 요청"""

    id: int  # 삭제할 퀴즈의 ID


class QuizResponse(BaseModel):
    """퀴즈 응답 모델"""

    id: int
    title: str
    questions: Optional[List[QuestionResponse]] = None  # 응답에서 questions는 선택적

    class Config:
        from_attributes = True  # 변경된 설정


class QuizSubmissionAnswerRequest(BaseModel):
    """퀴즈 제출 답안 요청"""

    question_id: int  # 문제 ID
    selected_option_id: int  # 사용자가 선택한 옵션 ID


class QuizSubmissionRequest(BaseModel):
    """퀴즈 제출 요청"""

    answers: List[QuizSubmissionAnswerRequest]  # 제출된 답안 목록


class QuizSubmissionAnswerResponse(BaseModel):
    """퀴즈 제출 답안 응답"""

    question_id: int  # 문제 ID
    selected_option_id: int  # 사용자가 선택한 옵션 ID
    is_correct: bool  # 정답 여부


class QuizSubmissionResponse(BaseModel):
    """퀴즈 제출 응답"""

    message: str  # 응답 메시지
    correct_count: int  # 정답 개수
    total_questions: int  # 총 문제 수
    score: float  # 점수
    answers: Optional[List[QuizSubmissionAnswerResponse]] = None  # 각 문제의 답안 결과
