from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer


# JWT Authentication related, if user IsAuthenticated, then he gets the content message
class AuthCheck(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Welcome, you are authorized!'}
        return Response(content)


@api_view(["GET"])
def get_tasks(request):
    # 1. retrieve the Task Objects
    # 2. Serialize them
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    return Response({"Tasks": serializer.data})


@api_view(["POST"])
def create_task(request):
    """
     CREATE Operation Algorithm:
     1. Accept input data from request.data
     2. Initialize serializer with raw data
     3. Validate data against model constraints
     4. If valid: save to database, return created object
     5. If invalid: return validation errors
     """
    user_data = request.data
    serializer = TaskSerializer(data=user_data)
    if serializer.is_valid():
        # Automatically links the task with the user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE", "PUT"])
def get_task_by_id(request, id):
    """
    CRUD Operations Algorithm:
    1. Retrieve object from database (or 404)
    2. Branch based on HTTP method
    3. Execute appropriate operation
    4. Return consistent response format
    """
    # Step 1.
    task = get_object_or_404(Task, pk=id)


    if request.method == "GET":
        """
        READ Operation:
        - Serialize existing object
        - Return data without modification
        """
        serializer = TaskSerializer(task)
        return Response({"data": serializer.data})

    elif request.method == "PUT":
        """
        UPDATE Operation Algorithm:
        1. Initialize serializer with existing instance + new data
        2. Validate new data
        3. If valid: update instance, return updated data
        4. If invalid: return validation errors
        """
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "msg": "Task Updated!",
                "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        task_data = TaskSerializer(task).data
        task_name = task_data.get("name")
        task.delete()
        return Response({"target": task_name, "deleted": True})



