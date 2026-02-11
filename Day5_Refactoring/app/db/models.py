from sqlalchemy import Column, Integer, String
from .base import Base

class Task(Base):
    __tablename__="tasks"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    is_done=Column(Integer, default=0)