# Design Document

## 1. 목적
DB 트랜잭션과 세션 격리를 직접 실험하고, 
단순 CRUD 구현을 넘어 데이터 정합성과 API 구조 설계를 이해하기 위한 프로젝트.

## 2. 핵심 기능
- 할 일 생성 (POST /tasks)
- 할 일 조회 (GET /tasks, Pagination 지원)
- 할 일 수정 (PATCH /tasks/{task_id})
- 할 일 삭제 (DELETE /tasks/{task_id})

### 3. 아키텍처 설계
### 3.1 계층 분리
- Router: HTTP 요청 / 응답 처리
- Service Layer: 비즈니스 로직 및 트랜잭션 제어
- DB Layer: ORM 모델 정의
→ HTTP 레벨과 비즈니스 로직 책임을 분리하여 유지보수성과 확장성을 고려

### 3.2 트랜잭션 경계
- commit은 비즈니스 로직 성공 시점에만 수행
- 실패시 rollback
- 요청 단위로 세션 생성 및 종료
→ 중간 상태 데이터 방지 및 데이터 정합성 유지

## 4. DB 설계
### 4.1 Task 테이블
- id(PK. 단조 증가, 재사용 금지)
- title
- is_done
- created_at (확장 고려)

### 4.2 설계 원칙
- id는 정렬 번호가 아닌 데이터 정체성
- 삭제 후 id 재정렬 금지
- Soft Delete 확장 가능성 고려

## 5. 인덱스 설계 계획
- 조회 패턴을 고려하여 다음 필드에 인덱스 적용 예정: 
> - created_at
> - is_done(status)
→ 실제 대량 데이터 환경에서 성능 비교 실험 예정