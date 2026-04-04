"""
URL configuration for chat app - template/template-based routes only.
This includes the create_task view that loads our AI-powered chat interface.
"""

from django.urls import path

from .views import create_task_ai

urlpatterns = [
    path("create_task/", create_task_ai, name="create_task"),
]
