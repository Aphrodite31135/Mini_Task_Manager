from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.db.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router=APIRouter(
    prefix="/tasks", 
    tags=["tasks"]
)

# HARD DELETE /task_id
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session=Depends(get_db)
):
    # 대상 조회
    db_task=db.query(Task).filter(Task.id==task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 삭제
    try:
        db.delete(db_task)
        db.commit()
    except:
        db.rollback()
        raise

# PATCH /task_id
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task: TaskUpdate, 
    db: Session=Depends(get_db)
):
    # 대상 조회
    db_task=db.query(Task).filter(Task.id==task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 상태 변경 (task.is_done이 None일 경우? / Patch처럼 보이는 강제 업데이트)
    # db_task.is_done=task.is_done
    # 상태 변경
    if task.title is not None:
        db_task.title=task.title

    if task.is_done is not None:
        db_task.is_done=task.is_done

    # 트랜잭션 처리
    try:
        db.commit()
        db.refresh(db_task)
        return db_task
    except:
        db.rollback()
        raise

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