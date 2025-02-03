from django.urls import path
from . import views
from .views import UserDetailView, UserRegisterView

urlpatterns = [
    path('',UserDetailView.as_view()),
    path('register/', UserRegisterView.as_view()),
    #path('<int:pk>'),
]