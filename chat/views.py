from django.shortcuts import redirect, render
from task_manager.services import create_task

from .services import parse_message


def create_task_ai(request):
    if request.method == "GET":
        return render(request, "chat/create_task.html")

    if request.method == "POST":
        message = request.POST.get("user_message", "").strip()

        if not message:
            return render(
                request, "chat/create_task.html", {"error_text": "Please enter a task description."}
            )

        try:
            result = parse_message(message)
            new_task = create_task(
                title=result.task.title,
                priority=result.task.priority,
                due_date=result.task.due_date,
                estimated_duration=result.task.estimated_duration,
            )

            context = {
                "created": True,
                "task_id": str(new_task.id),
                "title": result.task.title,
                "priority": result.task.priority,
                "due_date": result.task.due_date,
                "duration": result.task.estimated_duration or "N/A",
            }
        except ValueError as e:
            return render(request, "chat/create_task.html", {"error_text": str(e)})
        except Exception as e:
            error_msg = f"Failed to process your message: {str(e)}"
            if hasattr(str, "msg") and hasattr(str, "reason"):
                error_msg += f" (Message: {err.msg}, Reason: {err.reason})"
            return render(request, "chat/create_task.html", {"error_text": error_msg})

        return render(request, "chat/create_task.html", context)
