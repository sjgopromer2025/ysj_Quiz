from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from typing import List
from app.models.quiz import Quiz, Question, Option  # Option으로 수정
from app.schemas.quiz import QuizCreate


class QuizService:
    """퀴즈 관련 서비스 로직을 담당하는 클래스"""

    def create_quiz(self, quiz_data: QuizCreate, db: Session) -> Quiz:
        """퀴즈 생성"""
        try:
            # 퀴즈 생성
            new_quiz = Quiz(title=quiz_data.title)
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)

            # 문제 및 선택지 생성
            for question_data in quiz_data.questions:
                new_question = Question(text=question_data.text, quiz_id=new_quiz.id)
                db.add(new_question)
                db.commit()
                db.refresh(new_question)

                for option_data in question_data.options:
                    new_option = Option(  # Option으로 수정
                        text=option_data.text,
                        is_correct=option_data.is_correct,
                        question_id=new_question.id,
                    )
                    db.add(new_option)
                db.commit()

            return new_quiz
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def get_quizzes(self, page: int, page_size: int, db: Session) -> List[Quiz]:
        """퀴즈 목록 조회"""
        offset = (page - 1) * page_size
        quizzes = db.query(Quiz).offset(offset).limit(page_size).all()
        return quizzes

    def get_quiz_detail(self, quiz_id: UUID, db: Session) -> Quiz:
        """퀴즈 상세 조회"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("퀴즈를 찾을 수 없습니다.")
        return quiz

    def attempt_quiz(self, quiz_id: UUID, db: Session) -> Quiz:
        """퀴즈 응시"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("퀴즈를 찾을 수 없습니다.")

        # 문제 랜덤화
        questions = quiz.questions
        if quiz.randomize_questions:
            import random

            random.shuffle(questions)

        # 선택지 랜덤화
        for question in questions:
            if quiz.randomize_choices:
                random.shuffle(question.options)

        return quiz
