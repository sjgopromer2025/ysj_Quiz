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
