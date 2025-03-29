import re
import bcrypt
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.models.member import Member

from sqlalchemy.exc import IntegrityError


class MemberService:
    """회원 관련 서비스 로직을 담당하는 클래스"""

    MASTER_KEY = (
        "secret1234"  # 관리자 마스터키 (운영에서는 환경변수로 관리하는 것이 좋음)
    )

    def __init__(self):
        pass

    def create_member(
        self,
        request,
        username: str,
        password: str,
        user_type: str,
        master_key: str = None,
        db: Session = Depends(get_db),
    ):
        # 유효성 검사
        errors = self.validate_registration(
            username=username,
            password=password,
            user_type=user_type,
            master_key=master_key,
        )

        if errors:
            # 에러가 있으면 템플릿을 다시 렌더링
            return {
                "template": "register/register.html",
                "context": {
                    "request": request,
                    "username": username,
                    "password": password,
                    "user_type": user_type,
                    "master_key": master_key,
                    "errors": errors,
                },
            }

        # 비밀번호 해싱
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # 회원 생성 로직
        new_member = Member(
            username=username,
            password=hashed_password,
            user_type=user_type,
        )

        try:
            # 데이터베이스에 회원 정보 저장
            db.add(new_member)
            db.commit()
        except IntegrityError:
            return {
                "template": "register/register.html",
                "context": {
                    "request": request,
                    "username": username,
                    "password": password,
                    "user_type": user_type,
                    "master_key": master_key,
                    "errors": ["이미 존재하는 사용자 이름입니다."],
                },
            }

        return {"message": "회원이 성공적으로 생성되었습니다."}

    def validate_registration(
        self,
        username: str,
        password: str,
        user_type: str,
        master_key: str = None,
    ):
        """회원가입 유효성 검사"""
        errors = []

        # 1. 필수 필드 확인
        if not all([username, password, user_type]):
            errors.append("모든 필드를 입력해야 합니다.")

        # 2. 비밀번호 길이 검사
        if len(password) < 6:
            errors.append("비밀번호는 최소 6자 이상이어야 합니다.")

        # 3. 관리자 선택 시 마스터키 검증
        if user_type == "admin":
            if not master_key or master_key != self.MASTER_KEY:
                errors.append("마스터 키가 올바르지 않습니다.")

        return errors  # 에러 메시지 리스트 반환

    def login_member(self, username: str, password: str, db: Session = Depends(get_db)):
        """로그인 로직"""
        member = db.query(Member).filter(Member.username == username).first()

        if not member:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if not bcrypt.checkpw(
            password.encode("utf-8"), member.password.encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다.")
        return {
            "message": "로그인 성공",
            "user": {
                "username": member.username,
                "user_type": member.user_type,
            },
        }
