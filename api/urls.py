from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    path("task/", views.TaskCreate.as_view(), name="task-view-create"),
    path("task/<int:pk>", views.TaskUpdateDelete.as_view(), name="task-view-update-delete"),
    path('home', Home.as_view()),
]