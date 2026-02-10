from pydantic import BaseModel
from typing import Optional

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