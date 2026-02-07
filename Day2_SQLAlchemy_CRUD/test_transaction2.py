from .db.base import SessionLocal
from .db.models import Task

def transaction_test():
    db1 = SessionLocal()
    db2 = SessionLocal()

    db1.add(Task(title="db1 only"))

    print("db2:", db2.query(Task).all())  # 안 보임

    db1.commit()

    print("db2 after commit:", db2.query(Task).all())

    db1.close()
    db2.close()

if __name__ == "__main__":
    transaction_test()
