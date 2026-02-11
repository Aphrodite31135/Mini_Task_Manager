from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, List
from pydantic.generics import GenericModel

# 입력용
class TaskCreate(BaseModel):
    title: str

# 교체용
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None

# 출력용
class TaskResponse(BaseModel):
    id: int
    title: str
    is_done: bool

    # ORM 객체를 그대로 반환해도 schema가 읽을 수 있게
    class Config:
        # orm_mode = True
        from_attributes = True

T= TypeVar("T")
class APIResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T]= None
    message: Optional[str]= None

class TaskListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[TaskResponse]

    class Config:
        from_attributs = True

