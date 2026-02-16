from django.utils import timezone
from .models import Task

def create_task(*, title: str, priority: str = Task.Priority.NORMAL, due_date=None, estimated_duration: int | None = None) -> Task:
    """
    Create a new task with optional priority, due date, and est duration
    """
    return Task.objects.create(
        title=title,
        priority=priority,
        due_date=due_date,
        estimated_duration=estimated_duration
    )

def complete_task(task_id: int) -> Task:
    """
    Mark a task as complete
    """
    task = Task.objects.get(id=task_id)
    if task.status == Task.Status.COMPLETE:
        return task
    task.status = Task.Status.COMPLETE
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at", "updated_at"])
    return task

def list_tasks(*, status: str | None = None, overdue: bool | None = None):
    """
    Return tasks filtered by status and/or overdue.
    """
    queryset = Task.objects.all()
    if status:
        queryset = queryset.filter(status=status)
    if overdue:
        queryset = queryset.filter(
            status=Task.Status.OPEN,
            due_date__lt=timezone.now()
        )
    return queryset


def daily_review():
    """
    Returns a summary of tasks:
    - completed today
    - open tasks
    - overdue tasks
    """
    today = timezone.now().date()
    completed_today = Task.objects.filter(
        status=Task.Status.COMPLETE,
        completed_at__date=today
    )
    open_tasks = Task.objects.filter(status=Task.Status.OPEN)
    overdue_tasks = Task.objects.filter(
        status=Task.Status.OPEN,
        due_date__lt=timezone.now()
    )
    return {
        "completed_today": completed_today,
        "open_tasks": open_tasks,
        "overdue_tasks": overdue_tasks
    }
