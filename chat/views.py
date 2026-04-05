from django.shortcuts import redirect, render
from task_manager.services import create_task

from .services import handle_intent, parse_message


def chat(request):
    if request.method == "GET":
        return render(request, "chat/message.html")

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

        return render(request, "chat/message.html", merged_result)
