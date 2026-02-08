# Mini_Task_Manager

## PJ Purpose
DB, API, 트랜잭션 개념 실습용 미니 프로젝트

## Required
- Python, FastAPI
- SQLAlchemy
- SQLite / PostgreSQL

## 핵심 기능
- 할 일 생성
- 할 일 목록 조회
- 할 일 상태 변경
- 할 일 삭제

## DB
- Task 테이블 중심 설계
- 조회가 잦을 것으로 예상되는 칼럼 기준으로 인덱스 적용 고려

## 실험 계획
- 인덱스 적용 전/후 조회 성능 비교
- 트랜잭션 실패 시 데이터 정합성 확인

## 향후 계획
- RDS 환경을 가장한 구조로 확장
- DynamoDB 사용 시 구조 차이 비교

## Day2
- SQLAlchemy ORM을 사용한 CRUD 및 트랜잭션 동작 실습
- 세션 단위 트랜잭션 격리와 commit 시점의 중요성 이해

## Day3
- FastAPI 기반 프로젝트 구조(app / api / db / schemas) 설계
- APIRouter를 활용한 엔드포인트 분리
- DB 세션 의존성(get_db)과 트랜잭션(commit / rollback) 흐름 이해
- GET /tasks, POST /tasks API 구현 및 Swagger 문서 확인