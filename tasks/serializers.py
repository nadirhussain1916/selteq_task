from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    class Meta:
        model = Task
        fields = ['id', 'title', 'duration', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating the Task model (title only)."""
    class Meta:
        model = Task
        fields = ['id', 'title']
        read_only_fields = ['id']