from typing import Optional

from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    priority: str
    due_date: Optional[str] = None
    estimated_duration: Optional[int] = None
    status: str = "open"


class ChatResponseSchema(BaseModel):
    intent: str
    task: TaskSchema
