from django.urls import path

from .api import ChatAPIView

urlpatterns = [
        path('chat/', ChatAPIView.as_view())
        ]
