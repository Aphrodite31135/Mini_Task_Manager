from sqlalchemy.orm import Session
from .models import Task

def create_task(db: Session, title: str):
    try: 
        task = Task(title=title)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise e

def get_tasks(db:Session):
    return db.query(Task).all()