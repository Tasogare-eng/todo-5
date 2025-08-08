from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from app.models.task import TaskStatus, TaskPriority

TITLE_MAX = 100
DESC_MAX = 1000

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    dueDate: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("title must not be empty")
        if len(v2) > TITLE_MAX:
            raise ValueError("title too long")
        return v2

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]):
        if v and len(v) > DESC_MAX:
            raise ValueError("description too long")
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    dueDate: Optional[datetime] = None

class TaskRead(TaskBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
