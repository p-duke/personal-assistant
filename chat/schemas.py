from typing import Optional

from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    title: str
    priority: str
    due_date: Optional[str] = None
    estimated_duration: Optional[int] = None
    status: str = "open"

class CompleteTaskSchema(BaseModel):
    task_id: int

class ChatResponseSchema(BaseModel):
    intent: str
    task: Optional[CreateTaskSchema | CompleteTaskSchema] = None
    error: Optional[str] = None
