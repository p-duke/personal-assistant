from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    title: str
    priority: str
    due_date: Optional[str] = None
    estimated_duration: Optional[int] = None
    status: str = 'open'


class CompleteTaskSchema(BaseModel):
    task_id: Optional[int] = None
    task_identifier: Optional[str] = None


class ChatResponseSchema(BaseModel):
    intent: str
    task: Optional[CreateTaskSchema | CompleteTaskSchema] = None
    # list_tasks
    status: Optional[str] = None
    # suggest_focus
    available_minutes: Optional[int] = None
    energy_level: Optional[str] = None
    location: Optional[str] = None
    error: Optional[str] = None
