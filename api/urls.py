from tkinter.font import names

from django.urls import path
from . import views
from .views import AuthCheck

urlpatterns = [
    path("tasks/", views.get_tasks, name="List All Tasks"),
    path("task/create", views.create_task, name="Task Create"),
    path("task/<int:id>", views.get_task_by_id, name="Access Task By ID"),
    path("tasks/filter-by-priority/", views.filter_tasks_by_priority, name="filter-tasks-by-priority"),
    path("tasks/priority/<int:priority_level>", views.tasks_by_priority),
    path("tasks/filter-by-deadline/", views.filter_tasks_by_deadline, name="filter-tasks-by-deadline"),
    path("tasks/filter-by-status/", views.filter_tasks_by_status, name="filter-tasks-by-status"),
    path('auth_check', AuthCheck.as_view()),
]
