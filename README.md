# YSJ 퀴즈 시스템

YSJ 퀴즈 시스템은 퀴즈를 생성, 관리 및 응시할 수 있는 웹 기반 애플리케이션입니다. 사용자 인증, 퀴즈 제출 및 관리자 제어 기능을 지원합니다.

---

## 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [설치](#설치)
3. [사용법](#사용법)
4. [주요 기능](#주요-기능)
5. [API 문서](#api-문서)
6. [개발](#개발)
7. [라이선스](#라이선스)

---

## 프로젝트 개요

YSJ 퀴즈 시스템은 **FastAPI**와 **PostgreSQL**을 기반으로 구축되었습니다. 관리자와 일반 사용자가 퀴즈와 상호작용할 수 있는 사용자 친화적인 인터페이스를 제공합니다.

---

## 설치

### 사전 요구사항

- Python 3.13 이상
- PostgreSQL 데이터베이스

### 설치 방법

1. 저장소를 클론합니다:

   ```bash
   git clone https://github.com/your-repo/ysjquiz.git
   cd ysjquiz
   ```

2. 의존성을 설치합니다:

   ```bash
   poetry install
   ```

3. 환경 변수를 설정합니다:

   - 루트 디렉토리에 `.env` 파일을 생성합니다.
   - 아래와 같은 내용을 추가합니다:
     ```properties
     DATABASE_URL=postgresql://<사용자명>:<비밀번호>@<호스트>:<포트>/<데이터베이스>
     JWT_SECRET_KEY=<비밀 키>
     SECRET_KEY=<비밀 키>
     ```

4. 데이터베이스 마이그레이션을 적용합니다:

   ```bash
   alembic upgrade head
   ```

5. 개발 서버를 실행합니다:
   ```bash
   poetry run dev
   ```

---

## 사용법

### 애플리케이션 실행

- `http://127.0.0.1:8000`에서 애플리케이션에 접속할 수 있습니다.

### 주요 명령어

- Poetry 캐시 삭제:
  ```bash
  poetry cache clear --all pypi
  ```
- 의존성 설치:
  ```bash
  poetry install
  ```
- 서버 실행:
  ```bash
  poetry run dev
  ```

---

## 주요 기능

### 사용자 관리

- 사용자 회원가입 및 로그인
- 역할 기반 접근 제어 (관리자 및 일반 사용자)

### 퀴즈 관리

- 퀴즈 생성, 수정 및 삭제
- 문제와 선택지 추가, 수정 및 삭제
- 문제와 선택지 랜덤화

### 퀴즈 응시

- 퀴즈 진행 상태 저장
- 답안 제출 및 점수 계산
- 퀴즈 기록 및 점수 확인

---

## API 문서

### 인증

- **POST** `/member/login`: 사용자 로그인
- **DELETE** `/member/logout`: 사용자 로그아웃

### 퀴즈 관리

- **GET** `/quiz/list`: 모든 퀴즈 목록 조회
- **POST** `/quiz/create`: 새로운 퀴즈 생성
- **PUT** `/quiz/update/{quiz_id}`: 퀴즈 제목 수정
- **DELETE** `/quiz/delete/{quiz_id}`: 퀴즈 삭제

### 문제 관리

- **POST** `/quiz/create/question`: 퀴즈에 문제 추가
- **PUT** `/quiz/update/question/{question_id}`: 문제 수정
- **DELETE** `/quiz/delete/question/{question_id}`: 문제 삭제

### 퀴즈 응시

- **GET** `/quiz/detail/{quiz_id}`: 퀴즈 상세 조회
- **POST** `/quiz/submit/{quiz_id}`: 퀴즈 답안 제출

---

## 개발

### 폴더 구조

- `app/`: 메인 애플리케이션 폴더
  - `routers/`: API 라우트 정의
  - `services/`: 비즈니스 로직
  - `models/`: 데이터베이스 모델
  - `schemas/`: 요청/응답 검증용 Pydantic 모델
  - `utils/`: 유틸리티 함수
  - `templates/`: 프론트엔드 HTML 템플릿
- `alembic/`: 데이터베이스 마이그레이션
- `.env`: 환경 변수

### 테스트 실행

- `tests/` 폴더에 테스트 케이스를 추가합니다.
- 아래 명령어로 테스트를 실행합니다:
  ```bash
  pytest
  ```

---
