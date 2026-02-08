from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.db.models import Task
from app.schemas import TaskCreate, TaskResponse

router=APIRouter(
    prefix="/tasks", 
    tags=["tasks"]
)

# GET /tasks
@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session=Depends(get_db)):
    return db.query(Task).all()

# POST /tasks
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session= Depends(get_db)
):
    new_task=Task(
        title=task.title,
        is_done=False
    )

    try: 
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except:
        db.rollback()
        raise