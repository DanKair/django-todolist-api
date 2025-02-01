from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
