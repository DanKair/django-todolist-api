from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task
from .serializers import TaskSerializer

# Responds for Create (POST) operation and has additional DELETE all Tasks functionality
class TaskCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)  # Show only user’s tasks
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        Task.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        # Automatically links the task with the user
        serializer.save(user=self.request.user)

class TaskUpdateDelete(generics.RetrieveUpdateDestroyAPIView): #RetrieveUpdateDestroy allow us to Update and Delete items
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # looking for primary key, which stands for item id
    lookup_field = "pk"

    def get_queryset(self):
        # Дает доступ только к задачам текущего пользователя
        return Task.objects.filter(user=self.request.user)

# JWT Authentication related, if user IsAuthenticated, then he gets the content message
class AuthCheck(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Welcome, you are authorized!'}
        return Response(content)
