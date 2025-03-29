from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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


class QuizSubmission(Base):
    """퀴즈 제출 모델"""

    __tablename__ = "quiz_submission"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(
        String(150), ForeignKey("member.username", ondelete="CASCADE")
    )  # 사용자 username 참조
    quiz_id = Column(Integer, ForeignKey("quiz.id", ondelete="CASCADE"))
    score = Column(Float, nullable=False)  # 점수
    submitted_at = Column(DateTime, server_default=func.now())  # 제출 시간

    # 관계 설정 (퀴즈 제출 - 퀴즈 / 퀴즈 제출 - 답안)
    quiz = relationship("Quiz", backref="submissions")
    answers = relationship(
        "QuizSubmissionAnswer", back_populates="submission", cascade="all, delete"
    )
    member = relationship("Member", backref="submissions")  # Member와 관계 설정


class QuizSubmissionAnswer(Base):
    """퀴즈 제출 답안 모델"""

    __tablename__ = "quiz_submission_answer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(
        Integer, ForeignKey("quiz_submission.id", ondelete="CASCADE")
    )
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"))
    selected_option_id = Column(Integer, ForeignKey("option.id", ondelete="CASCADE"))

    # 관계 설정 (퀴즈 제출 답안 - 제출 / 문제 / 선택지)
    submission = relationship("QuizSubmission", back_populates="answers")
    question = relationship("Question", backref="submission_answers")
    selected_option = relationship("Option", backref="submission_answers")
