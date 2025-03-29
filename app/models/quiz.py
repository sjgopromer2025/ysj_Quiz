from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.connection import Base


class Quiz(Base):
    """퀴즈 모델"""

    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)  # 퀴즈 제목

    # 관계 설정 (퀴즈 - 문제)
    questions = relationship("Question", back_populates="quiz", cascade="all, delete")


class Question(Base):
    """문제 모델"""

    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quiz.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)  # 문제 내용

    # 관계 설정 (문제 - 퀴즈 / 문제 - 선택지)
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete")


class Option(Base):
    """선택지 모델"""

    __tablename__ = "option"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"))
    text = Column(String, nullable=False)  # 선택지 내용
    is_correct = Column(Boolean, default=False)  # 정답 여부

    # 관계 설정 (선택지 - 문제)
    question = relationship("Question", back_populates="options")
