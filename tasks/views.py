import jwt
import datetime
from django.db import connection
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from .authentication import JWTAuthentication

@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    """Generates a JWT token for the user."""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    expiration = datetime.datetime.now() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_TIME)

    payload = {
        'user_id': user.id,
        'exp': expiration.timestamp(),
        'iat': datetime.datetime.now().timestamp()
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

    return Response({'token': token})

class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tasks."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskSerializer

    def get_queryset(self):
        """Returns the last 4 tasks of the logged-in user."""
        return Task.objects.filter(user=self.request.user).order_by('-created_at')[:4]

    def perform_create(self, serializer):
        """Saves a new task for the logged-in user."""
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        user_id = request.user.id
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, duration, created_at, updated_at FROM tasks_task WHERE id = %s AND user_id = %s",
                [task_id, user_id]
            )
            row = cursor.fetchone()
            
            if not row:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            task_data = {
                "id": row[0],
                "title": row[1],
                "duration": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }
            
            return Response(task_data)

    def update(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        user_id = request.user.id
        title = request.data.get('title')
        
        if not title:
            return Response({"detail": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM tasks_task WHERE id = %s AND user_id = %s",
                [task_id, user_id]
            )
            count = cursor.fetchone()[0]
            
            if count == 0:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            cursor.execute(
                "UPDATE tasks_task SET title = %s, updated_at = GETDATE() WHERE id = %s AND user_id = %s",
                [title, task_id, user_id]
            )
            
            cursor.execute(
                "SELECT id, title, duration, created_at, updated_at FROM tasks_task WHERE id = %s",
                [task_id]
            )
            row = cursor.fetchone()
            
            task_data = {
                "id": row[0],
                "title": row[1],
                "duration": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }
            
            return Response(task_data)
    
    def destroy(self, request, *args, **kwargs):
        """Deletes a task created by the logged-in user."""
        task_id = kwargs.get('pk')
        user_id = request.user.id

        try:
            task = Task.objects.get(id=task_id, user=user_id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)