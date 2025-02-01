from django.urls import path
from . import views
from .views import UserDetailView

urlpatterns = [
    path('',UserDetailView.as_view())
]