from sqlalchemy.orm import Session
from app.db.models import Task

def get_tasks(db:Session, skip: int= 0, limit: int= 10):
    query= db.query(Task).order_by(Task.id.desc())
    total= query.count()
    items= (
        query
        .offset(skip)
        .limit(limit)
        .all()
        )
    return total, items

def create_task(db: Session, title: str):
    new_task= Task(title=title, is_done=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task(db: Session, task_id: int, is_done: bool):
    task= db.query(Task).filter(Task.id==task_id).first()
    if not task:
        return None
    
    task.is_done=is_done
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task= db.query(Task).filter(Task.id==task_id).first()
    if not task:
        return None
    
    db.delete(task)
    db.commit()
    return task