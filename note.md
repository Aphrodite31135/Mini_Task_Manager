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