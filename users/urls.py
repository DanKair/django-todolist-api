from django.urls import path
from . import views
from .views import UserDetailView, UserRegisterAPIView

urlpatterns = [
    path('',UserDetailView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path("<int:user_id>", views.UserUpdateDelete.as_view(), name="user-view-update-delete"),
]