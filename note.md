## Day1
- 상대 import / 패키지 import 충돌 발생
- 상대 import는 패키지로 실행해야 한다 ~반드시~

## Day2
### test_crud
1. 트랜잭션은 자동으로 시작된다
2. ORM은 결국 SQL로 변환된다
3. COMMIT이 있어야 DB에 남는다
4. SELECT도 트랜잭션이다
5. ROLLBACK ≠ 항상 되돌림
<!-- SQLAlchemy의 echo 로그를 통해 트랜잭션이 언제 시작되고 커밋되는지, ORM 코드가 실제 SQL로 어떻게 변환되는지 확인했습니다. -->
### test_transaction
1. 같은 세션에서는 commit 전 데이터가 보인다
2. commit이 없으면 DB에는 안 남는다
3. rollback은 “이번 작업만” 되돌린다
4. SELECT도 항상 트랜잭션 안에서 일어난다
<!-- SQLAlchemy 세션은 DB 상태와 메모리 상태를 함께 관리하기 때문에, 같은 세션에서는 commit 전 데이터도 조회되지만, rollback 이후에는 실제 DB에 반영되지 않은 데이터가 사라지는 것을 확인했습니다. -->
### test_transaction2
1. db1, db2 세션은 완전히 다른 세계다
2. commit 전에는 절대 공유 X
3. commit 이후에는 db2에서도 즉시 보인다
4. ORM 객체 주소가 다른 이유는 같은 row라도 세션마다 다른 Python 객체이기 때문이다

## Day3
### 핵심
- FastAPI는 그냥 껍데기고 진짜 중요한 건 세션, 트랜잭션, 모델, 스키마의 역할 분리이다
### FastAPI 기본 구조
1. FastAPI는 main.py에서 시작하고, 실제 기능은 router로 분리한다
2. app 폴더를 기준으로 absolute import(ex: app.xxx)를 사용해야 한다
3. uvicorn은 프로젝트 루트에서 실행해야 모듈 경로가 꼬이지 않는다
4. uvicorn은 ASGI 기반 비동기 서버이다
### DB 세션 의존성
1. get_db는 요청 단위로 세션을 생성 / 종료 한다
2. commit / rollback은 의존성이 아니라 API 함수 내부 책임이다
3. Day2에서 실험한 트랜잭션 개념이 FastAPI 흐름과 정확히 연결된다
### Schema 도입
1. 입력용(TaskCreate)과 출력용(TaskResponse)은 역할이 다르다
2. response_model은 ORM 객체를 JSON으로 안전하게 변환한다
3. schema를 쓰지 않으면 API 스펙이 흐려진다
### 기타
Pydantic v2에서는 orm_mode → from_attributes 경고 발생
- ImportError 대부분은 실행 위치 or 모듈 경로 문제
- main.py는 실행 대상 X, 앱을 켜는 곳
- tasks.py는 '/tasks' 세계의 규칙을 적는 곳
### result.md 의미
1. FastAPI 라우터 정상 연결
2. get_db() 의존성 주입 성공
3. 요청 1개 = Session 1개
4. ORM → SQL → 실제 DB 조회
5. Day2에서 만든 데이터가 API로 노출됨

## Day4
### 요약
- update_task 과정에서 SELECT를 먼저 하는 이유: '없는 리소스'를 구분하는 것이 선행돼야 함. 
- id는 '순서'가 아니라 '존재 증명'이다
> - 실제 서버에서는 절대 id를 당겨서 정렬하지 않는다
> - id를 재사용하지 않는 건 '성능'이 아니라 '의미적 안정성' 때문이다
### 궁금했던 부분: DELETE 후 task_id 정렬 / id 재사용 X 이유
- 할 수 없어서 안 하는 게 아니라 하면 안 되기 때문에 안 하는 것
#### 1. DB의 id: 한 번 부여되면 절대 변하지 않는 정체성
- 만약 id를 당긴다면 생기는 문제들
1) 외부 참조 전부 깨짐: 다른 테이블의 FK, 로그테이블, 캐시(Redis), 클라이언트가 기억한 id, URL /tasks/3
2) 시간 순서가 뒤틀림: id는 보통 생성 시점의 단조 증가를 의미
3) 트랜잭션 / 동시성 지옥 : 데이터 무결성 붕괴
> (ex: A 요청 id=5 / B 요청 DELETE 후 재정렬 → A는 다른 row를 보고 있음)
#### 2. 리소스를 많이 사용하기 때문 ← 부차적인 이유
- 비싸고 느림
1) UPDATE로 PK를 전부 바꿔야 함
2) 인덱스 재구성
3) FK cascade 재설정
4) 락 장시간 점유
#### 3. id를 재사용하지 않는 이유
1.  전혀 다른 task가 과거 기록을 상속
> ex:
> - 로그: task_id=5 completed
> - 통계: task_id=5
> - 캐시: task:5
2.  정보 노출
> ex:
> - 사용자가 /tasks/5 기억
> - 삭제됨
> - 다른 사람의 task가 새로 id=5를 받음
#### 4. 실무
1. DB id의 원칙
- 단조 증가
- 재사용 안함
- 의미 없음
- 외부 노출 가능하지만 신뢰하지 않음
2. 정렬
- 항상 쿼리 레벨에서
3. Soft Delete 선호
- Hard Delete: 존재 자체를 지운다
> 1) 특징
> - DB에서 완전히 사라짐
> - 복구 불가
> - 참조 관계 있으면 에러 or cascasde
> 2) 용도
> - 로그 필요 없음
> - 테스트 데이터
> - 임시 데이터
> - GDPR 같은 '완전 삭제' 요구
- Soft Delete: 삭제했다고 표시만 한다
> 1) 특징
> - 데이터는 남아 있음
> - 조회에서만 제외
> - 복구 가능
> - 통계 / 로그 / 감사에 유리
- Soft Delete가 기본인 이유
> 1) 복구 요청은 무조건 온다
> 2) 로그 / 감사 / 통계
> - 누가 언제 삭제했는지
> - 삭제된 데이터 포함한 통계
> - 히스토리 추적 (Hard Delete = 증거 인멸)
> 3) FK 지옥 회피
> - Task 삭제 시:
> > - Hard Delete → 전부 연쇄 삭제 or 에러
> > - Soft Delete → 안전
> 4) id 재사용 문제와도 연결됨
> - Soft Delete를 쓰면:
> > - id는 계속 증가
> > - 삭제 ≠ 소멸
> > - 과거 기록과 충돌 없음
#### 5. 사용자에게 보여주는 번호 : 따로 만들기 / 절대 DB PK를 '예쁜 번호'로 쓰지 않음
- UI row number
- 페이지 번호
- display_id
- created_at 기반 순서