from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# 요청용 Pydantic 모델
class MemberCreate(BaseModel):
    username: str = Field(..., max_length=150, description="사용자 이름")
    password: str = Field(..., min_length=6, max_length=20, description="비밀번호")
    user_type: str = Field(..., max_length=50, description="사용자 유형")
    master_key: Optional[str] = Field(None, description="관리자용 마스터 키")

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        user_type: str = Form(...),
        master_key: Optional[str] = Form(None),
    ):
        return cls(
            username=username,
            password=password,
            user_type=user_type,
            master_key=master_key,
        )


# 응답용 Pydantic 모델
class MemberResponse(BaseModel):
    id: UUID
    username: str
    user_type: str

    class Config:
        from_attributes = True  # SQLAlchemy 모델과 호환되도록 설정
