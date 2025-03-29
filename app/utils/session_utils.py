import json
from fastapi import Request, Response


def get_session(request: Request, key: str):
    """세션에서 데이터를 가져옵니다."""
    session_data = request.session.get(key)
    if session_data:
        # JSON 문자열을 딕셔너리로 변환
        return json.loads(session_data)
    return None


def set_session(request: Request, response: Response, key: str, value: dict):
    """세션에 데이터를 설정합니다."""
    # 딕셔너리를 JSON 문자열로 변환하여 저장
    request.session[key] = json.dumps(value, ensure_ascii=False)


def delete_session(request: Request, key: str = None):
    """세션 데이터를 삭제합니다."""
    if key:
        # 특정 키의 세션 데이터 삭제
        if key in request.session:
            del request.session[key]
    else:
        # 모든 세션 데이터 삭제
        request.session.clear()
