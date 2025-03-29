from pydantic import BaseModel, Field
from typing import List, Optional


class OptionCreate(BaseModel):
    """선택지 생성 요청"""

    text: str
    is_correct: bool


class QuestionCreate(BaseModel):
    """문제 생성 요청"""

    text: str
    options: List[OptionCreate] = Field(..., min_items=3)  # 최소 3개 이상의 선택지 필요

    # 정답 검증: 최소 1개의 정답이 존재해야 함
    @staticmethod
    def validate_options(options: List[OptionCreate]):
        if not any(option.is_correct for option in options):
            raise ValueError("각 문제에는 최소 1개의 정답이 포함되어야 합니다.")
        return options


class QuizCreate(BaseModel):
    """퀴즈 생성 요청"""

    title: str
    questions: List[QuestionCreate]


class QuizResponse(BaseModel):
    """퀴즈 응답 모델"""

    id: int
    title: str
    questions: List[QuestionCreate]

    class Config:
        orm_mode = True
