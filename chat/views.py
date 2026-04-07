from django.shortcuts import render

from .services import handle_intent, parse_message
from task_manager.services import list_tasks, daily_review


def chat(request):
    if request.method == "GET":
        # Get open tasks
        open_tasks = list_tasks(status="open")

        # Get overdue tasks
        overdue_tasks = list_tasks(status="open", overdue=True)

        # Get completed today
        review = daily_review()
        completed_today = review["completed_today"]

        context = {
            "open_tasks": open_tasks,
            "overdue_tasks": overdue_tasks,
            "completed_today": completed_today,
        }
        return render(request, "chat/message.html", context)

    if request.method == "POST":
        message = request.POST.get("user_message", "").strip()

        if not message:
            return render(
                request, "chat/message.html", {"error_text": "Please enter a task description."}
            )

        try:
            parsed = parse_message(message)
            context = { "created": False }

            result = handle_intent(parsed)
            merged_result = context | result

            if parsed.error is not None:
                merged_result["error_text"] = parsed.error

        except ValueError as e:
            return render(request, "chat/message.html", {"error_text": str(e)})
        except Exception as e:
            error_msg = f"Failed to process your message: {str(e)}"
            return render(request, "chat/message.html", {"error_text": error_msg})

        print(f"merged_result {merged_result}")

        return render(request, "chat/message.html", merged_result)
