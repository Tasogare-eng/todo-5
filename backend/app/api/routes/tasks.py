from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import select
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.db.session import get_session
from sqlmodel import Session
from datetime import datetime

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskRead])
def list_tasks(status: Optional[TaskStatus] = Query(None), session: Session = Depends(get_session)):
    statement = select(Task)
    if status:
        statement = statement.where(Task.status == status)
    statement = statement.order_by(Task.createdAt.desc())
    return session.exec(statement).all()

@router.post("", response_model=TaskRead, status_code=201)
def create_task(data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**data.dict())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: str, data: TaskCreate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for k, v in data.dict().items():
        setattr(task, k, v)
    task.updatedAt = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}", response_model=TaskRead)
def patch_task(task_id: str, data: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = data.dict(exclude_unset=True)
    for k, v in update_data.items():
        setattr(task, k, v)
    task.updatedAt = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return None
