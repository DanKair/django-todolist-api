from django.urls import path
from . import views
from .views import UserDetailView, UserRegisterAPIView, UserLoginAPIView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('',UserDetailView.as_view()),
    path('register/', UserRegisterAPIView.as_view(), name="user-register-view"),
    path('login/', UserLoginAPIView.as_view(), name="user-login-view"),
    path('logout/', LogoutView.as_view(), name="User Logout"),
    path("<int:user_id>", views.UserUpdateDelete.as_view(), name="user-view-update-delete"),
    path('token/refresh', TokenRefreshView.as_view()),
]