from django.urls import path, include
from rest_framework import routers

from .views import TaskListApiView, TaskRUDApiView, AttachmentViewSet, task_support

router = routers.DefaultRouter()
router.register(r'files', AttachmentViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
    path('my-tasks/', TaskListApiView.as_view(), name='my_tasks'),
    path('task-rud/<int:task_id>/', TaskRUDApiView.as_view(), name='task_rud'), # Read, Update, Delete
    path('task-support/<int:task_id>/', task_support, name='ai_generator'), # Suggestion generator to make task done
]