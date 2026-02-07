from .db.base import SessionLocal
from .db.models import Task

def transaction_test():
    db = SessionLocal()

    task = Task(title="커밋 전 데이터")
    db.add(task)

    print("commit 전:", db.query(Task).all())

    db.rollback()

    print("rollback 후:", db.query(Task).all())

    db.close()

if __name__ == "__main__":
    transaction_test()
