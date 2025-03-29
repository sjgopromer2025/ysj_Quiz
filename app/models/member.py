from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.connection import Base  # 기존 Base를 가져옴


# 멤버 모델 클래스 정의
class Member(Base):
    __tablename__ = "member"

    # UUID를 기본 키로 사용
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    user_type = Column(String(50), nullable=False)
    # email = Column(String(255), unique=True, nullable=True)  # 이메일 필드 추가

    def __repr__(self):
        return f"<Member(username={self.username}, user_type={self.user_type})>"
