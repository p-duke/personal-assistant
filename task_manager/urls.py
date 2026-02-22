from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, dashboard_view, create_task_view, complete_task_view

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")

# Template views
urlpatterns = [
    path('', dashboard_view, name='dashboard'),                        # /
    path('tasks/create/', create_task_view, name='create_task'),        # /tasks/create/
    path('tasks/<int:task_id>/complete/', complete_task_view, name='complete_task'),  # /tasks/1/complete/
]

# Add API URLs from router
urlpatterns += router.urls
