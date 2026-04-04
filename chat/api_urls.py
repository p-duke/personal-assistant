"""
URL configuration for chat app - REST API endpoints only.
This includes DRF ViewSets and APIViews exposed via Django REST framework.
"""

from django.urls import path

from .api import ChatAPIView

urlpatterns = [
    path("chat/", ChatAPIView.as_view()),
]
