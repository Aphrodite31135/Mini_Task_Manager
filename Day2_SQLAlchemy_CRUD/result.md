## test_crud.py
### 요약
INSERT 트랜잭션을 열고 데이터를 저장한 뒤 커밋하고, 새 트랜잭션을 열어 저장된 데이터를 다시 조회한 후 읽기 트랜잭션을 종료했다.
### 로그
```html
BEGIN (implicit)
<!-- 트랜잭션 시작 (모든 DB 작업은 트랜잭션 안에서 시작) -->
INSERT INTO tasks (title, is_done) VALUES (?, ?)
<!-- db.add(task)가 SQL INSERT로 변환 (?는 바인딩 변수) -->
[generated in 0.00015s] ('Day2 트랜잭션 연습', 0) 
<!-- INSERT에 실제로 들어간 값들, SQL 생성 + 실행에 걸린 시간 출력
    (ORM → SQL → DB 전달 과정이 여기 보임)" -->
COMMIT
<!-- 트랜잭션 확정 / DB 파일에 기록 -->

BEGIN (implicit)
<!-- 새로운 트랜잭션 시작-->
SELECT tasks.id, tasks.title, tasks.is_done FROM tasks
<!-- db.SELECT도 트랜잭션 안에서 처리됨
    db.refresh(task) -->
WHERE tasks.id = ?
<!-- 방금 INSERT된 row를 다시 조회 (DB에서 자동 생성된 id를 가져오기 위함) -->
[generated in 0.00013s] (4,)
<!-- WHERE tasks.id = 4 (DB가 id를 만들어서 ORM에게 다시 알려주는 과정) -->
ROLLBACK
<!-- 트랜잭션 종료 / 데이터를 되돌린게 아님 -->
```

## test_transaction.py
### 요약
같은 세션에서는 commit 전 데이터도 조회되지만, rollback 이후에는 DB에 반영되지 않은 데이터는 사라진다. 
### 로그
```html
BEGIN (implicit)
<!-- 새로운 트랜잭션 시작-->
SELECT tasks.id AS tasks_id, tasks.title AS tasks_title, tasks.is_done AS tasks_is_done FROM tasks
<!-- db.query(Task).all() 실행 (ORM → SELECT SQL로 변환)  -->
[generated in 0.00015s] ()
<!-- 전체 테이블 조회 -->
commit 전: [<Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D790>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D760>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D730>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D220>]
<!-- commit을 안했는데 보이는 이유: 같은 세션(DB) 안에서는 commit 전 데이터도 보임
    SQLAlchemy 세션: DB + 메모리 상태 함께 관리
    → 아직 commit 안 된 객체도 '내가 알고 있는 상태'로 보여줌 -->
ROLLBACK
<!-- 트랜잭션 종료 / commit 안 된 변경사항 전부 취소
    → 메모리에 있던 task: DB에 반영 안 된 상태 → 전부 날아감 -->

BEGIN (implicit)
<!-- 새로운 트랜잭션 시작-->
SELECT tasks.id AS tasks_id, tasks.title AS tasks_title, tasks.is_done AS tasks_is_done FROM tasks
<!-- 전체 테이블 조회 -->
[cached since 0.001351s ago] ()
rollback 후: [<Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D8E0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D8B0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D880>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x000001A89A74D940>]
<!-- 이전 실험에서 commit된 데이터들 / 이번에 add한 task X
    → 전체 테이블 비우기 X / 이번 트랜잭션에서 한 변경만 취소 -->
ROLLBACK
```

## test_transaction2.py
### 요약
서로 다른 세션에서는 commit 전에는 절대 데이터가 공유되지 않지만, commit 후에는 즉시 데이터가 보인다. 
### 로그
```html
BEGIN (implicit)
SELECT tasks.id AS tasks_id, tasks.title AS tasks_title, tasks.is_done AS tasks_is_done FROM tasks
[generated in 0.00011s] ()
db2: [<Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D217C0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21790>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21760>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D211C0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21820>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21880>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D218E0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21940>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D219A0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21A00>]
<!-- db2 세션 SELECT / 작업한 것이 없으므로 기존 데이터들(10개)만 보임 -->

BEGIN (implicit)
INSERT INTO tasks (title, is_done) VALUES (?, ?)
[generated in 0.00010s] ('db1 only', 0)
COMMIT
<!-- db1 세션 내부 / commit을 했으므로 DB에 영구 반영, 다른 세션에서도 볼 수 있음 -->

SELECT tasks.id AS tasks_id, tasks.title AS tasks_title, tasks.is_done AS tasks_is_done FROM tasks
[cached since 0.006674s ago] ()
<!-- SQL 문자열 컴파일 결과만 캐시 / 데이터는 DB에서 다시 가져옴 -->
db2 after commit: [<Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21E50>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21E20>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21DF0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21DC0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21E80>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21EE0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21F10>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21EB0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D21FA0>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D22000>, <Day2_SQLAlchemy_CRUD.db.models.Task object at 0x0000019D14D22060>]
<!-- 데이터 개수 10개 → 11개 / db1 only가 이제 db2에서도 보임 -->
ROLLBACK
```