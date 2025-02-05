from django.shortcuts import render
from rest_framework import permissions, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser
from .serializers import UserSerializer


# User registration View at /users/register endpoint
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# All Users Detail view ( sure you can't see the password)
class UserDetailView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class UserUpdateDelete(generics.RetrieveUpdateDestroyAPIView): #RetrieveUpdateDestroy allow us to Update and Delete items
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    # looking for primary key, which stands for item id
    lookup_url_kwarg = "user_id"

