# Mini_Task_Manager

## PJ Purpose
DB, API, 트랜잭션 개념 실습용 미니 프로젝트

## Required
- Python
- FastAPI
- SQLAlchemy (ORM)
- SQLite (local)

## Features
- Task 생성 (POST /tasks)
- Task 목록 조회 (GET /tasks, Pagination 지원)
- Task 상태 변경 (PATCH /tasks/{id})
- Task 삭제 (DELETE /tasks/{id})

## DB
- Task(id, title, is_done, created_at)
- PK는 단조 증가, 재사용 X
- 조회 패턴을 고려한 인덱스 실험 진행

## Architecture
- app / api / db / schemas 구조 분리
- Roputer ↔ Service Layer 책임 분리
- 요청 1개 = DB Session 1개 구조
- commit / rollback을 API 레벨에서 직접 제어

## What I Practiced
- ORM → 실제 SQL 동작 확인
- 트랜잭션 격리 및 rollback 실험
- RESTful API 설계
- 상태코드(200 / 201 / 204 / 404) 기준 정리
- Pagination 및 응답 구조 표준화

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