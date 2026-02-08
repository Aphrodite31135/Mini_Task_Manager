from pydantic import BaseModel

# 입력용
class TaskCreate(BaseModel):
    title: str

# 출력용
class TaskResponse(BaseModel):
    id: int
    title: str
    is_done: bool

    # ORM 객체를 그대로 반환해도 schema가 읽을 수 있게
    class Config:
        # orm_mode = True
        from_attributes = True