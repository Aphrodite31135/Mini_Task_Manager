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