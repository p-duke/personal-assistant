from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from . import services

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Tasks.
    Only orchestrates HTTP → services layer.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Optionally filter by status or overdue via query params:
        /api/tasks/?status=open
        /api/tasks/?overdue=true
        """
        status_param = self.request.query_params.get("status")
        overdue = self.request.query_params.get("overdue")
        overdue_flag = overdue == "true"

        return services.list_tasks(
            status=status_param,
            overdue=overdue_flag,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task = services.create_task(
            title=validated_data["title"],
            priority=validated_data["priority"],
            due_date=validated_data["due_date"],
            estimated_duration=validated_data["estimated_duration"]
        )
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        """
        PATCH /api/tasks/{id}/complete/
        Marks a task as complete using the service layer
        """
        task = services.complete_task(pk)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def daily_review(self, request):
        """
        GET /api/tasks/daily_review/
        Returns completed today, open, and overdue tasks
        """
        review = services.daily_review()
        return Response({
            "completed_today": TaskSerializer(review["completed_today"], many=True).data,
            "open_tasks": TaskSerializer(review["open_tasks"], many=True).data,
            "overdue_tasks": TaskSerializer(review["overdue_tasks"], many=True).data
        })
