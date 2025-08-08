from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    doing = "doing"
    done = "done"

class TaskPriority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class Task(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.todo)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    dueDate: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    # updatedAt 自動更新はアプリ層で行う
