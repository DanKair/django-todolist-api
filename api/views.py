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

# Tasks Filtering Functionality

@api_view(['GET'])
def filter_tasks_by_priority(request):
    """
    Filter tasks based on priority passed as a query parameter.
    Example: /api/tasks/filter-by-priority/?priority=1
    Note: Query parameters accept input as strings
    """
    priority = request.query_params.get("priority")

    if priority not in ["1", "2", "3"]:
        return Response(
            {"error": "Invalid or missing priority. Must be 1 (High), 2 (Medium), or 3 (Low)."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Map for human-readable response key
    priority_map = {
        "1": "High Priority Tasks",
        "2": "Mid Priority Tasks",
        "3": "Low Priority Tasks"
    }

    tasks = Task.objects.filter(priority=priority)
    serializer = TaskSerializer(tasks, many=True)

    return Response({priority_map[priority]: serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def tasks_by_priority(request, priority_level: int):
    if priority_level > 0:
        if priority_level == 1:
            top_priority_tasks = Task.objects.filter(priority=1)
            serializer = TaskSerializer(top_priority_tasks, many=True)
            return Response({"High Priority Tasks": serializer.data})

        elif priority_level == 2:
            mid_priority_tasks = Task.objects.filter(priority=2)
            serializer = TaskSerializer(mid_priority_tasks, many=True)
            return Response({"Mid Priority Tasks": serializer.data})

        else:
            low_priority_tasks = Task.objects.filter(priority=1)
            serializer = TaskSerializer(low_priority_tasks, many=True)
            return Response({"Low Priority Tasks": serializer.data})

    return Response({"Error": "Specify Priority Level above 0"})



@api_view(['GET'])
def filter_tasks_by_status(request):
    """
    Filter tasks by their completion status (is_done).
    Example: ?is_done=true or ?is_done=false
    """
    is_done_param = request.query_params.get("is_done")

    if is_done_param is None:
        return Response(
            {"error": "Missing 'is_done' query parameter. Use true or false."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Convert string to boolean
    is_done_param = is_done_param.lower()
    if is_done_param == "true":
        is_done = True
    elif is_done_param == "false":
        is_done = False
    else:
        return Response(
            {"error": "'is_done' must be 'true' or 'false'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Filter tasks by is_done
    tasks = Task.objects.filter(is_done=is_done)
    serializer = TaskSerializer(tasks, many=True)

    label = "Completed Tasks" if is_done else "Uncompleted Tasks"
    return Response({label: serializer.data})



@api_view(['GET'])
def filter_tasks_by_deadline(request):
    """
    Filter tasks based on deadline.
    Supports:
    - ?before=YYYY-MM-DD
    - ?after=YYYY-MM-DD
    - ?on=YYYY-MM-DD
    - ?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    before = request.query_params.get('before')
    after = request.query_params.get('after')
    on = request.query_params.get('on')
    start = request.query_params.get('start')
    end = request.query_params.get('end')

    tasks = Task.objects.all()

    try:
        if on:
            date_obj = datetime.strptime(on, "%Y-%m-%d").date()
            tasks = tasks.filter(deadline__date=date_obj)

        elif before:
            date_obj = datetime.strptime(before, "%Y-%m-%d").date()
            tasks = tasks.filter(deadline__date__lt=date_obj)

        elif after:
            date_obj = datetime.strptime(after, "%Y-%m-%d").date()
            tasks = tasks.filter(deadline__date__gt=date_obj)

        elif start and end:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            tasks = tasks.filter(deadline__date__range=(start_date, end_date))

    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = TaskSerializer(tasks, many=True)
    return Response({"Filtered Tasks by Deadline": serializer.data})

