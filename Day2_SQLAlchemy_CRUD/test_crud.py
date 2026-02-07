from .db.base import SessionLocal
from .db.crud import create_task

db=SessionLocal()
create_task(db, "Day2 트랜잭션 연습")
db.close()