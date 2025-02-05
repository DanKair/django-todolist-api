from django.urls import path
from . import views
from .views import AuthCheck

urlpatterns = [
    path("task/create", views.TaskCreate.as_view(), name="task-view-create"),
    path("task/<int:pk>", views.TaskUpdateDelete.as_view(), name="task-view-update-delete"),
    path('auth_check', AuthCheck.as_view()),
]