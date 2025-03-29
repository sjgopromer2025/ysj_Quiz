import re
from fastapi import HTTPException
from app.models.member import Member  # Member 모델 가져오기
from app.db.connetion import session  # SQLAlchemy 세션 가져오기
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
        username: str,
        password: str,
        user_type: str,
        master_key: str = None,
    ):
        # 회원가입 유효성 검사
        self.validate_registration(
            username=username,
            password=password,
            user_type=user_type,
            master_key=master_key,
        )

        # 회원 생성 로직
        new_member = Member(
            username=username,
            password=password,  # 비밀번호는 해싱하여 저장하는 것이 좋음
            user_type=user_type,
        )

        try:
            # 데이터베이스에 회원 정보 저장
            with session() as db_session:
                db_session.add(new_member)
                db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="이미 존재하는 사용자 이름입니다."
            )

        return {"message": "회원이 성공적으로 생성되었습니다."}

    def validate_registration(
        self,
        username: str,
        password: str,
        # email: str,
        user_type: str,
        master_key: str = None,
    ):
        """회원가입 유효성 검사"""

        # 1. 필수 필드 확인
        if not all([username, password, user_type]):
            raise HTTPException(status_code=400, detail="모든 필드를 입력해야 합니다.")

        # 2. 이메일 형식 검사
        # email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # if not re.match(email_regex, email):
        #     raise HTTPException(
        #         status_code=400, detail="올바른 이메일 형식이 아닙니다."
        #     )

        # 3. 비밀번호 길이 검사
        if len(password) < 6:
            raise HTTPException(
                status_code=400, detail="비밀번호는 최소 6자 이상이어야 합니다."
            )

        # 4. 관리자 선택 시 마스터키 검증
        if user_type == "admin":
            if not master_key or master_key != self.MASTER_KEY:
                raise HTTPException(
                    status_code=400, detail="마스터 키가 올바르지 않습니다."
                )

        return True
