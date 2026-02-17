# Mini_Task_Manager

## PJ Purpose
단순 CRUD 구현이 아닌,  
DB 트랜잭션과 세션 격리를 실험하며
데이터 정합성과 API 구조를 이해하기 위한 프로젝트.

## Tech Stack
- Python
- FastAPI (ASGI)
- SQLAlchemy (ORM)
- SQLite (local)

## Architecture
app/
├── api/               # Router (HTTP 처리)
├── services/          # 비즈니스 로직
├── db/                # DB 연결 및 모델
├── schemas.py         # 입력/출력 Schema
└── main.py            # FastAPI 엔트리포인트

### 구조 원칙
- Router는 HTTP 레벨 책임만 담당
- Service Layer에서 트랜잭션(commit / rollback) 제어
- 요청 1개 = DB Session 1개
- Schemas를 통해 API 스펙 명확화

## Example Response
```json
{
    "total": 0,
    "skip": 0,
    "limit": 0,
    "items": [...]
}
```

## What I Practiced

### 1. 트랜잭션 실험
- commit 전 / 후 데이터 가시성 확인
- rollback 시 중간 상태 데이터 제거
- 세션 단위 격리 실험

### 2. RESTful API 설계
- PATCH / DELETE 메서드의 의미 이해
- 상태 코드(200 / 201 / 204 / 404) 명확화
- Pagination(skip / limit) 적용

### 3. 설계 철학
- id는 정렬 번호가 아니라 정체성
- id 재사용 금지
- 트랜잭션 경계는 비즈니스 단위
- 동작하는 코드보다 데이터 무결성이 우선

## Day2
- SQLAlchemy ORM을 사용한 CRUD 및 트랜잭션 동작 실습
- 세션 단위 트랜잭션 격리와 commit 시점의 중요성 이해

## Day3
- FastAPI 기반 프로젝트 구조(app / api / db / schemas) 설계
- APIRouter를 활용한 엔드포인트 분리
- DB 세션 의존성(get_db)과 트랜잭션(commit / rollback) 흐름 이해
- GET /tasks, POST /tasks API 구현 및 Swagger 문서 확인

## Day4
- REST API 관점에서 Update / Delete 동작 정리
- PATCH / DELETE 메서드의 역할 차이 이해
- delete 시 id를 재정렬하거나 재사용하지 않는 이유 학습
- 트랜잭션 책임 분리 (조회 → 검증 → commit / rollback)
- 404, 204 등 상태 코드의 의미와 사용 기준 정리
- API 레벨에서 예외 처리가 왜 중요한지 체감

## Day5
- Router와 비즈니스 로직 분리를 위한 Service Layer 도입
- HTTP 처리와 DB 로직의 책임 분리
- Pagination(skip / limit) 구현
- total / skip / limit / items 형태의 응답 구조 표준화
- API 확장성을 고려한 응답 설계 경험

## Future Extension
- SQLite → RDS 확장
- EC2 배포
- JWT 인증 도입
- 인덱스 성능 실험