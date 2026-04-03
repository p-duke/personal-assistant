from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.services import create_task

from .services import parse_message


class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")

        if not message or not isinstance(message, str) or not message.strip():
            return Response(
                {"error": "Invalid message. Must be a non-empty string"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Parse the natural language message using your service layer
            result = parse_message(message)
            task = result.task

            new_task = create_task(
                    title=task.title,
                    priority=task.priority,
                    due_date=task.due_date,
                    estimated_duration=task.estimated_duration
            )

            # Return the structured response
            return Response(
                {
                    "intent": result.intent,
                    "task_id": new_task.id,
                    "task": {
                        "title": task.title,
                        "priority": task.priority,
                        "due_date": task.due_date,
                        "estimated_duration": task.estimated_duration,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            # Handle any errors from the service layer
            return Response(
                {"error": str(e), "suggest": "try again"},
                status=status.HTTP_400_BAD_REQUEST
            )
