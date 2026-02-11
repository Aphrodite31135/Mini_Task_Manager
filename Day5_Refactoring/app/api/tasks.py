from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, TaskListResponse, APIResponse
from app.services import task_service

router=APIRouter(
    prefix= "/tasks", 
    tags= ["tasks"]
)

# HARD DELETE /task_id
@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int,db: Session=Depends(get_db)):
    deleted= task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

# PATCH /task_id
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session=Depends(get_db)):
    updated= task_service.update_task(db, task_id, task.is_done)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

# GET /tasks
@router.get("/", response_model=APIResponse[TaskListResponse])
def get_tasks(
    db: Session= Depends(get_db), 
    skip: int= Query(0, ge=0),
    # 기본값 0, 0 이상만 허용
    limit: int= Query(10, ge=1, le=100)
    # api 안전장치: 최소 1, 최대 100
    ):
    result= task_service.get_tasks(db, skip, limit)
    return APIResponse(
        success=True, 
        data=result, 
        message=None
    )
@router.get("/{task_id}", response_model=APIResponse[TaskResponse])
def get_task(task_id: int, db: Session= Depends(get_db)):
    task= task_service.get_tasks(db, task_id)
    return APIResponse(
        success=True, 
        data=task
    )


# POST /tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session= Depends(get_db)):
    return task_service.create_task(db, task.title)