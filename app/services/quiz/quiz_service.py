import random
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from typing import List
from app.models.quiz import Quiz, Question, Option
from app.schemas.quiz import QuizCreate, QuestionCreate, QuestionUpdate, QuizResponse
from app.models.quiz import (
    QuizSubmission,
    QuizSubmissionAnswer,
)


class QuizService:
    """퀴즈 관련 서비스 로직을 담당하는 클래스"""

    def create_quiz(self, title: str, db: Session) -> Quiz:
        """퀴즈 생성"""
        try:
            # Title 중복 체크
            existing_quiz = db.query(Quiz).filter(Quiz.title == title).first()
            if existing_quiz:
                raise ValueError(f"'{title}' 제목의 퀴즈가 이미 존재합니다.")

            # 새로운 퀴즈 생성
            new_quiz = Quiz(title=title)
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)
            return new_quiz
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def get_all_quizzes(self, db: Session) -> List[Quiz]:
        """모든 퀴즈 목록 조회"""
        try:
            quizzes = db.query(Quiz).all()
            return quizzes
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def get_all_quizzes_with_question_count(self, db: Session):
        """Fetch all quizzes with the count of questions in each quiz."""
        quizzes = db.query(Quiz).all()
        result = []
        for quiz in quizzes:
            question_count = (
                db.query(Question).filter(Question.quiz_id == quiz.id).count()
            )
            result.append(
                {"id": quiz.id, "title": quiz.title, "question_count": question_count}
            )
        return result

    def add_question_to_quiz(
        self, quiz_id: int, question_data: QuestionCreate, db: Session
    ) -> Question:
        """퀴즈에 문제 추가"""
        try:
            # 퀴즈 확인
            quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
            if not quiz:
                raise ValueError("퀴즈를 찾을 수 없습니다.")

            # 문제 생성
            new_question = Question(text=question_data.text, quiz_id=quiz_id)
            db.add(new_question)
            db.commit()
            db.refresh(new_question)

            # 선택지 생성
            for option_data in question_data.options:
                new_option = Option(
                    text=option_data.text,
                    is_correct=option_data.is_correct,
                    question_id=new_question.id,
                )
                db.add(new_option)
            db.commit()

            return new_question
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete_quiz(self, quiz_id: int, db: Session) -> None:
        """퀴즈 삭제 및 하위 문제 포함 전부 삭제"""
        try:
            quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
            if not quiz:
                raise ValueError("퀴즈를 찾을 수 없습니다.")

            # 관련된 문제와 선택지 삭제
            db.query(Option).filter(
                Option.question_id.in_(
                    db.query(Question.id).filter(Question.quiz_id == quiz_id)
                )
            ).delete(synchronize_session=False)
            db.query(Question).filter(Question.quiz_id == quiz_id).delete(
                synchronize_session=False
            )

            # 퀴즈 삭제
            db.delete(quiz)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete_question(self, question_id: int, db: Session):
        """문제 삭제 로직"""
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("삭제하려는 문제가 존재하지 않습니다.")
        db.delete(question)
        db.commit()
        return

    def get_quiz_detail(self, quiz_id: int, db: Session):
        """퀴즈 상세 정보 조회 (문제 랜덤 섞기)"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("해당 ID의 퀴즈를 찾을 수 없습니다.")

        # 문제와 선택지 구성
        questions = questions = self.setting_questions(quiz.questions)

        return QuizResponse(
            id=quiz.id,
            title=quiz.title,
            questions=questions,
        )

    # # 퀴즈 상세 정보 조회 (문제 랜덤 섞기)
    def get_quiz_detail_suffle(self, quiz_id: int, db: Session):
        """퀴즈 상세 정보 조회 (문제 랜덤 섞기)"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("해당 ID의 퀴즈를 찾을 수 없습니다.")

        # 문제와 선택지 구성
        questions = self.setting_questions(quiz.questions)
        # 문제를 랜덤으로 섞기
        random.shuffle(questions)

        return QuizResponse(
            id=quiz.id,
            title=quiz.title,
            questions=questions,
        )

    def setting_questions(self, questions: dict):
        # 문제와 선택지 구성
        questions = [
            {
                "id": question.id,
                "text": question.text,
                "options": [
                    {
                        "id": option.id,
                        "text": option.text,
                        "is_correct": option.is_correct,
                    }
                    for option in question.options
                ],
            }
            for question in questions
        ]
        return questions

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

    def update_quiz_title(self, quiz_id: int, title: str, db: Session) -> None:
        """퀴즈 제목 수정"""
        try:
            quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
            if not quiz:
                raise ValueError("퀴즈를 찾을 수 없습니다.")

            # 제목 중복 체크
            existing_quiz = db.query(Quiz).filter(Quiz.title == title).first()
            if existing_quiz and existing_quiz.id != quiz_id:
                raise ValueError(f"'{title}' 제목의 퀴즈가 이미 존재합니다.")

            quiz.title = title
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def update_question(
        self, question_id: int, question_data: QuestionUpdate, db: Session
    ) -> None:
        """문제 수정"""
        try:
            question = db.query(Question).filter(Question.id == question_id).first()
            if not question:
                raise ValueError("문제를 찾을 수 없습니다.")

            # 문제 내용 수정
            question.text = question_data.text

            # 기존 선택지 삭제 및 새 선택지 추가
            db.query(Option).filter(Option.question_id == question_id).delete()
            for option_data in question_data.options:
                new_option = Option(
                    text=option_data.text,
                    is_correct=option_data.is_correct,
                    question_id=question_id,
                )
                db.add(new_option)

            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def submit_quiz_answers(
        self,
        quiz_id: int,
        answers: List,  # Use forward reference if needed
        user: dict,
        db: Session,
    ) -> dict:
        from app.models.quiz import Question, Option  # Import inside the method

        """퀴즈 답안 제출 및 채점"""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("퀴즈를 찾을 수 없습니다.")

        # 정답 체크
        correct_count = 0
        total_questions = len(answers)

        for answer in answers:
            question = (
                db.query(Question).filter(Question.id == answer.question_id).first()
            )
            if not question:
                raise ValueError(f"문제를 찾을 수 없습니다: {answer.question_id}")

            correct_option = (
                db.query(Option)
                .filter(Option.question_id == question.id, Option.is_correct == True)
                .first()
            )
            if correct_option and correct_option.id == answer.selected_option_id:
                correct_count += 1

        # 점수 계산
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        return {
            "message": "퀴즈가 성공적으로 제출되었습니다.",
            "correct_count": correct_count,
            "total_questions": total_questions,
            "score": score,
        }

    def save_quiz_submission(
        self,
        quiz_id: int,
        user: dict,
        answers: List[dict],
        result: dict,
        db: Session,
    ) -> None:
        """퀴즈 제출 데이터 저장"""
        try:
            # 퀴즈 제출 데이터 생성
            submission = QuizSubmission(
                user_id=user.get("id"),
                quiz_id=quiz_id,
                score=result["score"],
            )
            db.add(submission)
            db.commit()
            db.refresh(submission)

            # 각 답안 저장
            for answer in answers:
                submission_answer = QuizSubmissionAnswer(
                    submission_id=submission.id,
                    question_id=answer["question_id"],
                    selected_option_id=answer["selected_option_id"],
                )
                db.add(submission_answer)

            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
