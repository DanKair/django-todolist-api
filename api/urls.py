from tkinter.font import names

from django.urls import path
from . import views
from .views import AuthCheck

urlpatterns = [
    path("tasks/", views.get_tasks, name="List All Tasks"),
    path("task/create", views.create_task, name="Task Create"),
    path("task/<int:id>", views.get_task_by_id, name="Access Task By ID"),
    path('auth_check', AuthCheck.as_view()),
]