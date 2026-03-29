from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")

        if not message or not isinstance(message, str) or not message.strip():
            return Response(
                {"error": "Invalid message. Must be a non-empty string"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "intent": "create_task",
                "task": {
                    "title": "Placeholder task",
                    "priority": "normal",
                    "due_date": None,
                    "estimated_duration": None,
                },
            },
            status=status.HTTP_200_OK,
        )
