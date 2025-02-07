from rest_framework import permissions, status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer, UserRegisterationSerializer


# Old User registration View at /users/register endpoint
# class UserRegisterView(generics.CreateAPIView):
    # queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = [AllowAny]

# User Register View
class UserRegisterAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterationSerializer

    # After passing the data, user gets his refresh / access tokens
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

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
    # looking for primary key, which stands for user id
    lookup_url_kwarg = "user_id"

